# ---------------------------
# API Gateway
# ---------------------------
resource "aws_apigatewayv2_api" "api-gateway" {
    name          = "${var.project}-${var.environment}-${var.action}"
    description   = "API gateway create by aws terraform."
    protocol_type = "HTTP"
    tags = {
        Name    = "${var.project}-${var.environment}-${var.action}"
        Project = var.project
        Env     = var.environment
    }
}

resource "aws_apigatewayv2_route" "api-gw-route" {
    api_id    = aws_apigatewayv2_api.api-gateway.id
    route_key = "$default"
    target    = "integrations/${aws_apigatewayv2_integration.api-gw-integration.id}"
}

resource "aws_apigatewayv2_stage" "api-gw-stage" {
    api_id      = aws_apigatewayv2_api.api-gateway.id
    name        = "$default"
    description = "Lambda function deployment create by aws terraform."
    auto_deploy = true
}

resource "aws_apigatewayv2_integration" "api-gw-integration" {
    api_id                 = aws_apigatewayv2_api.api-gateway.id
    description            = "Lambda function integration create by aws terraform."

    integration_type       = "AWS_PROXY"
    connection_type        = "INTERNET"
    integration_method     = "POST"
    integration_uri        = aws_lambda_function.lambda-function.invoke_arn

    payload_format_version = "1.0"
    timeout_milliseconds   = "30000"
}
