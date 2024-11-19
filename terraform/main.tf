# ---------------------------
# Terraform Configure
# ---------------------------
terraform {
    required_version = ">=0.13" # Specify version 0.13 or higher.
    required_providers {
        aws = {
        source  = "hashicorp/aws" # Specify the module name.
        version = "~>3.0"         # 3.0 or higher (ignore minor versions).
        }
    }
}

# ---------------------------
# Provider
# ---------------------------
provider "aws" {
    access_key = var.access_key
    secret_key = var.secret_key
    region     = var.region
}
