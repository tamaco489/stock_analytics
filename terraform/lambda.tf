# ---------------------------
# Lambda
# ---------------------------
resource "aws_lambda_function" "lambda-function" {
    function_name    = "${var.project}-${var.environment}-${var.action}"
    description      = "Lambda function create by aws terraform."
    runtime          = "go1.x"
    handler          = "main"

    role             = aws_iam_role.lambda-iam-role.arn
    filename         = data.archive_file.function-source.output_path
    source_code_hash = data.archive_file.function-source.output_base64sha256

    memory_size      = 512
    timeout          = 15

    environment {
        variables = {
            SAMPLE_SECRET = "abcdefghijklmnopqrstuvwxyz0123456789"
        }
    }

    tags = {
        Name    = "${var.project}-${var.environment}-${var.action}"
        Project = var.project
        Env     = var.environment
    }
}

# Policy Statement
resource "aws_lambda_permission" "lambda-permission" {
    statement_id  = "AllowExecutionFromAPIGateway"
    function_name = aws_lambda_function.lambda-function.arn
    principal     = "apigateway.amazonaws.com"
    action        = "lambda:InvokeFunction"
    source_arn    = "${aws_apigatewayv2_api.api-gateway.execution_arn}/*/$default"
}