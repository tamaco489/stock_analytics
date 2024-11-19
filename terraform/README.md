## terraform setup and execute.
---

<br>

### setting environment variable.
---
```
touch ./config.tfvars
```
```
# [ profile ]
account_id = "0123456789"
access_key = "xxxxxxxxxx"
secret_key = "xxxxxxxxxxxxxxxxxxxx"
region     = "ap-northeast-1"
zone       = "ap-northeast-1a"

# [ General ]
project     = "xxx-project"
environment = "develop"
action      = ""
```

<br>

### terraform execution.
---
```
cd ./terraform
```
```
terraform init
```
```
terraform plan --var-file=./config.tfvars
```
```
terraform apply --var-file=./config.tfvars
```
```
terraform destroy --var-file=./config.tfvars
```