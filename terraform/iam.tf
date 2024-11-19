# ---------------------------
# IAM
# ---------------------------
resource "aws_iam_role" "lambda-iam-role" {
    name = "${var.project}-${var.environment}-${var.action}"
    assume_role_policy = file("./iam_list/lambda-iam-role.json")

    tags = {
        Name    = "${var.project}-${var.environment}-${var.action}"
        Project = var.project
        Env     = var.environment
    }
}

resource "aws_iam_policy" "lambda-execution-policy" {
    name   = "${var.project}-${var.environment}-${var.action}-execution-policy"
    policy = file("./iam_list/lambda-execution-policy.json")
    tags = {
        Name    = "${var.project}-${var.environment}-${var.action}-execution-policy"
        Project = var.project
        Env     = var.environment
    }
}

resource "aws_iam_policy" "lambda-lambroll-policy" {
    name   = "${var.project}-${var.environment}-${var.action}-lambroll-policy"
    policy = file("./iam_list/lambda-lambroll.json")
    tags = {
        Name    = "${var.project}-${var.environment}-${var.action}-lambroll-policy"
        Project = var.project
        Env     = var.environment
    }
}

resource "aws_iam_policy" "dynamodb-policy" {
    name   = "${var.project}-${var.environment}-${var.action}-dynamodb-policy"
    policy = file("./iam_list/dynamodb-access.json")
    tags = {
        Name    = "${var.project}-${var.environment}-${var.action}-dynamodb-policy"
        Project = var.project
        Env     = var.environment
    }
}

resource "aws_iam_role_policy_attachment" "lambda-policy-attachment" {
    role       = aws_iam_role.lambda-iam-role.name
    policy_arn = aws_iam_policy.lambda-execution-policy.arn
}

resource "aws_iam_role_policy_attachment" "lambroll-policy-attachment" {
    role       = aws_iam_role.lambda-iam-role.name
    policy_arn = aws_iam_policy.lambda-lambroll-policy.arn
}

resource "aws_iam_role_policy_attachment" "dynamodb-policy-attachment" {
    role       = aws_iam_role.lambda-iam-role.name
    policy_arn = aws_iam_policy.dynamodb-policy.arn
}