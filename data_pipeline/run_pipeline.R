# Main script to manage data pipeline

library(survivoR)
library(digest)
library(arrow)
library(aws.s3)

source("data_pipeline/process_tables.R")
source("data_pipeline/process_metadata.R")

# S3 settings
s3_bucket <- "survivorpy-data"
s3_prefix_parquet <- "tables/"
s3_prefix_metadata <- "metadata/"

# Load previous state from S3
previous_tables <- download_s3_json("table_names.json", s3_bucket, s3_prefix_metadata)
previous_metadata <- download_last_updated()

# Current state from survivoR
current_table_names <- get_survivor_table_names()

# Diff
added_tables <- setdiff(current_table_names, previous_tables)
deleted_tables <- setdiff(previous_tables, current_table_names)
common_tables <- intersect(current_table_names, previous_tables)

# Process table changes
parquet_dir <- tempdir()
delete_tables(deleted_tables, s3_bucket, s3_prefix_parquet)
add_info <- add_new_tables(added_tables, parquet_dir, s3_bucket, s3_prefix_parquet)
mod_info <- process_common_tables(
  table_names = common_tables,
  old_hashes = previous_metadata$metadata$hashes,
  output_dir = parquet_dir,
  bucket = s3_bucket,
  prefix = s3_prefix_parquet
)

# Update metadata and S3 if anything changed
full_hash_map <- c(add_info$hash_map, mod_info$hash_map)
updated <- update_metadata(
  added = add_info$added_tables,
  deleted = deleted_tables,
  modified = mod_info$modified_tables,
  current_table_names = current_table_names,
  hash_map = full_hash_map,
  bucket = s3_bucket,
  prefix_metadata = s3_prefix_metadata
)

# Output summary
if (updated) {
  cat("Updated tables:", mod_info$written_tables, "\n")
  cat("Added:", added_tables, "\nDeleted:", deleted_tables, "\nModified:", mod_info$modified_tables, "\n")
} else {
  cat("No changes detected. Nothing uploaded.\n")
}
