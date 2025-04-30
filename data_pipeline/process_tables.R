# Functions for processing added, deleted, and modified survivoR tables

#' Get the list of available data frames in the survivoR package
get_survivor_table_names <- function() {
  data(package = "survivoR")$results[, "Item"]
}

#' Delete specified tables from S3
delete_tables_from_s3 <- function(table_names, bucket, prefix) {
  for (name in table_names) {
    object_key <- paste0(prefix, name, ".parquet")
    aws.s3::delete_object(object = object_key, bucket = bucket)
    message(sprintf("Deleted %s from S3", object_key))
  }
}

#' Add new tables from survivoR and upload to S3 as parquet files
add_new_tables_to_s3 <- function(table_names, output_dir, bucket, prefix) {
  for (name in table_names) {
    df <- tryCatch(get(name, envir = asNamespace("survivoR")),
                   error = function(e) NULL)
    if (!is.null(df) && is.data.frame(df)) {
      file_path <- file.path(output_dir, paste0(name, ".parquet"))
      arrow::write_parquet(df, file_path)
      aws.s3::put_object(file = file_path,
                         object = paste0(prefix, name, ".parquet"),
                         bucket = bucket,
                         region = "us-west-2")
      message(sprintf("Added %s to S3", name))
    } else {
      message(sprintf("Skipping %s: not a valid dataframe", name))
    }
  }
}

#' Process common tables and upload only modified ones to S3
process_common_tables <- function(table_names, old_hashes, output_dir, bucket, prefix) {
  modified_tables <- c()
  hash_map <- list()
  written_tables <- c()
  
  for (name in table_names) {
    df <- tryCatch(get(name, envir = asNamespace("survivoR")),
                   error = function(e) NULL)
    if (!is.null(df) && is.data.frame(df)) {
      new_hash <- digest::digest(df, algo = "sha256")
      hash_map[[name]] <- new_hash
      
      if (is.null(old_hashes[[name]]) || old_hashes[[name]] != new_hash) {
        file_path <- file.path(output_dir, paste0(name, ".parquet"))
        arrow::write_parquet(df, file_path)
        aws.s3::put_object(file = file_path,
                           object = paste0(prefix, name, ".parquet"),
                           bucket = bucket,
                           region = "us-west-2")
        modified_tables <- c(modified_tables, name)
        written_tables <- c(written_tables, name)
        message(sprintf("Updated %s on S3", name))
      }
    } else {
      message(sprintf("Skipping %s: not a valid dataframe", name))
    }
  }
  
  list(
    modified_tables = modified_tables,
    hash_map = hash_map,
    written_tables = written_tables
  )
}
