# Function App Resources
resource "azurerm_storage_account" "sa" {
  name                     = "${var.project_name}${terraform.workspace}sa"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Application Insights for logging (Free tier: 1GB/month)
resource "azurerm_application_insights" "appinsights" {
  name                = "${var.project_name}-${terraform.workspace}-insights"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"
  
  # Free tier configuration
  daily_data_cap_in_gb                  = 1
  daily_data_cap_notifications_disabled = false
  retention_in_days                     = 30  # Minimum retention for free tier
  
  tags = {
    Environment = terraform.workspace
  }
}

resource "azurerm_service_plan" "plan" {
  name                = "${var.project_name}-${terraform.workspace}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  os_type            = "Linux"
  sku_name           = "Y1"

}

resource "azurerm_linux_function_app" "appname_function_app" {
  name                       = "${var.project_name}-${terraform.workspace}-func"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = var.location
  service_plan_id           = azurerm_service_plan.plan.id
  storage_account_name      = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key
  

  site_config {
    application_stack {
      python_version = "3.11"
    }
    
    # Enable Application Insights
    application_insights_key               = azurerm_application_insights.appinsights.instrumentation_key
    application_insights_connection_string = azurerm_application_insights.appinsights.connection_string
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
    "PYTHON_VERSION" = "3.11"
    "TELEGRAM_BOT_TOKEN"       = var.telegram_bot_token
    "OPENAI_API_KEY"          = var.openai_api_key
    
    # Application Insights settings
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.appinsights.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.appinsights.connection_string
    
    # Enhanced logging settings (free tier friendly)
    "AzureWebJobsDisableHomepage"          = "true"
    "FUNCTIONS_EXTENSION_VERSION"          = "~4"
    "WEBSITE_ENABLE_SYNC_UPDATE_SITE"      = "true"
    
    # Logging configuration
    "logging__logLevel__default" = "Information"
    "logging__logLevel__Host"    = "Error"
    "logging__logLevel__Function" = "Information"
  }
}

# Function App Outputs
output "function_app_name" {
  description = "The name of the function app"
  value       = azurerm_linux_function_app.appname_function_app.name
}

output "function_app_default_hostname" {
  description = "The default hostname of the function app"
  value       = azurerm_linux_function_app.appname_function_app.default_hostname
}

output "application_insights_name" {
  description = "The name of the Application Insights resource"
  value       = azurerm_application_insights.appinsights.name
}

output "application_insights_instrumentation_key" {
  description = "The instrumentation key for Application Insights"
  value       = azurerm_application_insights.appinsights.instrumentation_key
  sensitive   = true
}

output "get_publish_profile_command" {
  description = "Command to get the function app publish profile"
  value       = "az functionapp deployment list-publishing-profiles --name ${azurerm_linux_function_app.appname_function_app.name} --resource-group ${azurerm_resource_group.main.name} --xml"
}