# Azure Function App Terraform Configuration

This directory contains Terraform configuration for deploying the Telegram Bot Function App to Azure, using workspaces to manage different environments.

## Prerequisites

1. [Terraform](https://www.terraform.io/downloads.html) installed
2. Azure CLI installed and authenticated
3. Azure subscription

## Setup

1. Create the storage account for Terraform state:
```bash
az group create --name terraform-state-rg --location WestEurope
az storage account create --name tfstatetelegrambot --resource-group terraform-state-rg --location WestEurope --sku Standard_LRS
az storage container create --name tfstate --account-name tfstatetelegrambot
```

2. Create terraform.tfvars:
```bash
cp terraform.tfvars.example terraform.tfvars
```
Then edit `terraform.tfvars` with your actual subscription and tenant IDs.

## Usage

### Initialize Terraform
```bash
terraform init
```

### Development Environment
```bash
# Create and switch to dev workspace
terraform workspace new dev

# Plan and apply changes
terraform plan
terraform apply
```

### Production Environment
```bash
# Create and switch to prod workspace
terraform workspace new prod

# Plan and apply changes
terraform plan
terraform apply
```

### List Workspaces
```bash
terraform workspace list
```

### Switch Workspaces
```bash
terraform workspace select dev  # or prod
```

## Cleanup

To destroy resources in the current workspace:
```bash
terraform destroy
```

## Workspace State

Each workspace maintains its own state file in the Azure storage account:
- dev: `telegram-bot.tfstate/env:/dev`
- prod: `telegram-bot.tfstate/env:/prod` 