output "lambda_function_name" {
  description = "The name of the deployed Lambda function"
  value       = aws_lambda_function.rate_limit_function.function_name
}

output "lambda_arn" {
  description = "The ARN of the deployed Lambda function"
  value       = aws_lambda_function.rate_limit_function.arn
}

output "dynamodb_table_name" {
  description = "The name of the deployed DynamoDB table"
  value       = aws_dynamodb_table.rate_limit.name
}

output "api_gateway_url" {
  description = "The URL of the deployed API Gateway"
  value       = "https://${aws_apigatewayv2_api.rate_limit_api.id}.execute-api.${var.aws_region}.amazonaws.com/prod/rate-limit"
}
