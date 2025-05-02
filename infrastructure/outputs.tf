output "lambda_function_name" {
  description = "The name of the deployed Lambda function"
  value       = aws_lambda_function.rate_limit_function.function_name
}

output "lambda_arn" {
  description = "The ARN of the deployed Lambda function"
  value       = aws_lambda_function.rate_limit_function.arn
}

output "bucket_name" {
  description = "The existing S3 bucket used by the Lambda function"
  value       = data.aws_s3_bucket.existing_bucket.bucket
}
