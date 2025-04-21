library(survivoR)
library(arrow)
library(aws.s3)
library(jsonlite)

# S3 settings
s3_bucket <- "survivorpy-data"
s3_prefix_parquet <- "tables/"
s3_prefix_metadata <- "metadata/"


# Temporary output directories
parquet_dir <- tempdir()
table_names_json <- file.path(tempdir(), "table_names.json")

# Get dataset names from the package
dataset_names <- data(package = "survivoR")$results[, "Item"]

# Collect written table names
written_tables <- c()

# Convert dataframes to parquet files and upload to S3
for (name in dataset_names) {
  df <- tryCatch(get(name, envir = asNamespace("survivoR")),
                 error = function(e) NULL)
  
  if (!is.null(df) && is.data.frame(df)) {
    file_path <- file.path(parquet_dir, paste0(name, ".parquet"))
    arrow::write_parquet(df, file_path)
    
    put_object(
      file = file_path,
      object = paste0(s3_prefix_parquet, name, ".parquet"),
      bucket = s3_bucket,
      region = "us-west-2"
    )
    
    written_tables <- c(written_tables, name)
  } else {
    message(sprintf("Skipping %s: not a valid dataframe", name))
  }
}

# Write table_names.json
write_json(written_tables, table_names_json, auto_unbox = TRUE, pretty = TRUE)

# Upload table_names.json to S3
put_object(
  file = table_names_json,
  object = paste0(s3_prefix_metadata, "table_names.json"),
  bucket = s3_bucket,
  region = "us-west-2"
)

cat("Done! Wrote", length(written_tables), "parquet files and table_names.py to S3\n")
