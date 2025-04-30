# Functions for handling metadata files

#' Download a JSON file from S3 and parse into R
#' Returns an empty list if file is missing or invalid
download_s3_json <- function(filename, bucket, prefix) {
  key <- paste0(prefix, filename)
  obj <- aws.s3::get_object(object = key, bucket = bucket, region = "us-west-2")
  
  if (is.null(obj)) {
    warning(sprintf("File not found on S3: %s", key))
    return(list())
  }

  content <- rawToChar(obj)

  # Just try parsing, and give helpful error if it fails
  tryCatch(
    jsonlite::fromJSON(content),
    error = function(e) {
      stop(sprintf("Failed to parse JSON from '%s':\n%s", key, substr(content, 1, 200)))
    }
  )
}

#' Download metadata JSON from GitHub 
download_last_updated <- function() {
  metadata_url <- "https://api.github.com/repos/jonnycomes/survivorpy/contents/data_pipeline/metadata/data_last_updated.json"
  resp <- httr::GET(metadata_url)

  if (httr::status_code(resp) == 404) {
    warning("Metadata file not found on GitHub — starting fresh.")
    return(list(metadata = list(), sha = NULL))
  } else if (httr::status_code(resp) != 200) {
    stop("Failed to fetch metadata from GitHub: ", httr::content(resp, as = "text"))
  }

  remote <- jsonlite::fromJSON(httr::content(resp, as = "text", encoding = "UTF-8"))
  decoded <- jsonlite::fromJSON(rawToChar(jsonlite::base64_dec(remote$content)))

  return(list(metadata = decoded, sha = remote$sha))
}

#' Upload a list or dataframe as JSON to S3
upload_json_to_s3 <- function(data, filename, bucket, prefix) {
  key <- paste0(prefix, filename)
  tmp <- tempfile(fileext = ".json")
  jsonlite::write_json(data, tmp, pretty = TRUE, auto_unbox = TRUE)
  aws.s3::put_object(file = tmp, object = key, bucket = bucket, region = "us-west-2")
}

#' Upload updated data_last_updated.json to GitHub
upload_last_updated <- function(metadata, sha = NULL) {
  url <- "https://api.github.com/repos/jonnycomes/survivorpy/contents/data_pipeline/metadata/data_last_updated.json"
  new_content <- jsonlite::toJSON(metadata, auto_unbox = TRUE, pretty = TRUE)
  encoded <- jsonlite::base64_enc(charToRaw(new_content))

  # Construct body with or without sha depending on whether it's NULL
  body <- list(
    message = paste("Update data_last_updated.json", Sys.Date()),
    content = encoded,
    branch = "main"
  )

  if (!is.null(sha)) {
    body$sha <- sha
  }

  resp <- httr::PUT(
    url,
    body = body,
    encode = "json",
    httr::authenticate(Sys.getenv("GITHUB_USER"), Sys.getenv("GH_PAT"))
  )

  if (httr::status_code(resp) >= 300) {
    stop("Failed to upload updated metadata to GitHub: ", httr::content(resp, as = "text"))
  }
}

#' Update and upload metadata files
update_metadata <- function(added, deleted, modified,
                                   current_table_names, hash_map,
                                   bucket, prefix_metadata) {
  if (length(added) == 0 && length(deleted) == 0 && length(modified) == 0) {
    return(FALSE)
  }

  # Upload table names to S3
  upload_json_to_s3(sort(current_table_names), "table_names.json", bucket, prefix_metadata)

  # Download current GitHub metadata
  github_data <- download_last_updated()

  # Construct new metadata with more detail
  new_metadata <- list(
    hashes = hash_map,
    timestamp = format(Sys.time(), "%Y-%m-%dT%H:%M:%OS3Z", tz = "UTC"),
    added = added,
    deleted = deleted,
    modified = modified
  )

  # Upload updated metadata back to GitHub
  upload_last_updated(new_metadata, github_data$sha)

  return(TRUE)
}

