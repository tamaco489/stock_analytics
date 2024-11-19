# ---------------------------
# S3
# ---------------------------
resource "aws_s3_bucket" "s3-bucket" {
    bucket = "${var.project}-${var.environment}-${var.action}"

    tags = {
        Name    = "${var.project}-${var.environment}-${var.action}"
        Project = var.project
        Env     = var.environment
    }
}

resource "aws_s3_bucket_acl" "s3-bucket-acl" {
    bucket = aws_s3_bucket.s3-bucket.id
    acl    = "private"
}

resource "aws_s3_bucket_versioning" "s3-bucket-versioning" {
    bucket = aws_s3_bucket.s3-bucket.id
    versioning_configuration {
        status = "Enabled"
    }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "s3-bucket-encryption" {
    bucket = aws_s3_bucket.s3-bucket.bucket
    rule {
        apply_server_side_encryption_by_default {
            sse_algorithm = "AES256"
        }
    }
}