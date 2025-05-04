# DynamoDB table for rate limiting
resource "aws_dynamodb_table" "rate_limit" {
  name           = "rate-limit"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "ip_address"
  
  attribute {
    name = "ip_address"
    type = "S"
  }

  attribute {
    name = "last_reset"
    type = "N"
  }

  global_secondary_index {
    name               = "last_reset-index"
    hash_key           = "last_reset"
    projection_type    = "ALL"
  }
}

# IAM role for Lambda function execution
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect = "Allow",
      Sid    = ""
    }]
  })
}

# IAM role policy attachment for basic Lambda execution
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda function to handle rate limiting
resource "aws_lambda_function" "rate_limit_function" {
  function_name    = var.lambda_function_name
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = var.lambda_handler
  runtime          = var.lambda_runtime
  filename         = var.lambda_filename
  source_code_hash = filebase64sha256(var.lambda_filename)

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.rate_limit.name
      S3_BUCKET = var.bucket_name
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution
  ]
}

# Lambda function permissions to access DynamoDB
resource "aws_iam_role_policy" "lambda_dynamodb_access" {
  name = "lambda_dynamodb_policy"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ],
        Resource = aws_dynamodb_table.rate_limit.arn
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject"
        ],
        Resource = "arn:aws:s3:::survivorpy-data/survivor_data.zip"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket"
        ],
        Resource = "arn:aws:s3:::survivorpy-data"
      }
    ]
  })
}

# API Gateway to expose Lambda function
resource "aws_apigatewayv2_api" "rate_limit_api" {
  name          = "rate-limit-api"
  protocol_type = "HTTP"
}

# API Gateway route to invoke Lambda function
resource "aws_apigatewayv2_integration" "rate_limit_integration" {
  api_id             = aws_apigatewayv2_api.rate_limit_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.rate_limit_function.arn
  integration_method = "POST"
}

# API Gateway route (POST method)
resource "aws_apigatewayv2_route" "rate_limit_route" {
  api_id    = aws_apigatewayv2_api.rate_limit_api.id
  route_key = "POST /rate-limit"
  target    = "integrations/${aws_apigatewayv2_integration.rate_limit_integration.id}"
}

# Deploy API Gateway
resource "aws_apigatewayv2_deployment" "rate_limit_deployment" {
  api_id = aws_apigatewayv2_api.rate_limit_api.id

  depends_on = [
    aws_apigatewayv2_route.rate_limit_route,
    aws_apigatewayv2_integration.rate_limit_integration
  ]
}

# Create a stage for the API
resource "aws_apigatewayv2_stage" "rate_limit_stage" {
  api_id        = aws_apigatewayv2_api.rate_limit_api.id
  name          = "prod"
  deployment_id = aws_apigatewayv2_deployment.rate_limit_deployment.id
}

