variable "aws_region" {
  description = "AWS region where infrastructure is deployed"
  type        = string
  default     = "us-west-2"  # Update if your S3 bucket is in a different region
}

variable "bucket_name" {
  description = "Name of the existing S3 bucket to be used for data storage"
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda function that handles rate limiting"
  type        = string
  default     = "rate-limit-handler"
}

variable "lambda_runtime" {
  description = "Runtime environment for Lambda"
  type        = string
  default     = "python3.11"
}

variable "lambda_handler" {
  description = "Handler entry point for Lambda function"
  type        = string
  default     = "index.handler"
}

variable "lambda_filename" {
  description = "Path to the ZIP file containing the Lambda code"
  type        = string
  default     = "lambda.zip"
}
