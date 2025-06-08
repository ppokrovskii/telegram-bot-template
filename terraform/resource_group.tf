# Resource Group Resource
resource "azurerm_resource_group" "main" {
  # project_name-workspace_name-rg
  name     = "${var.project_name}-${terraform.workspace}-rg"
  location = var.location
}

# Resource Group Outputs
output "resource_group_name" {
  description = "The name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "resource_group_location" {
  description = "The location of the resource group"
  value       = azurerm_resource_group.main.location
} 