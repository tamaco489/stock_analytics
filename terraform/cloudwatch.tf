# ---------------------------
# CloudWatch
# ---------------------------
resource "aws_cloudwatch_log_group" "cloudwatch-logs" {
    name              = "/aws/lambda/${var.project}-${var.environment}-${var.action}"
    retention_in_days = 30

    tags = {
        Name    = "${var.project}-${var.environment}-${var.action}-cloudwatch-logs"
        Project = var.project
        Env     = var.environment
    }
}