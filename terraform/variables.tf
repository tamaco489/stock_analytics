# ---------------------------
# Variables
# ---------------------------
# [ terraform access information ]
variable "account_id" {
    type = number
}

variable "access_key" {
    type = string
}

variable "secret_key" {
    type = string
}

variable "region" {
    type = string
}

variable "zone" {
    type = string
}

# [ General ]
variable "project" {
    type = string
}

variable "environment" {
    type = string
}

variable "action" {
    type = string
}