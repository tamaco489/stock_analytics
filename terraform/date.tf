# ---------------------------
# Terraform Date Resource
# ---------------------------
# Go file
data "archive_file" "function-source" {
    type        = "zip"
    source_dir  = "./go/cmd/lambda_function"
    output_path = "archive/lambda_function.zip"
}