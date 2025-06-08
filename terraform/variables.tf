# Common Variables
variable "subscription_id" {
  description = "The subscription ID where resources will be created"
  type        = string
}


variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "West Europe"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "appname"
}

variable "telegram_bot_token" {
  description = "The Telegram Bot Token"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "The OpenAI API Key"
  type        = string
  sensitive   = true
}
