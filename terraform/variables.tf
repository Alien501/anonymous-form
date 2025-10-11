variable "environment" {
  description = "Environment name (dev or production)"
  type        = string
  validation {
    condition     = contains(["dev", "production"], var.environment)
    error_message = "Environment must be either 'dev' or 'production'."
  }
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "UAE North"
}

variable "app_service_sku" {
  description = "App Service Plan SKU"
  type        = string
  default     = "B1"
}

variable "db_sku_name" {
  description = "PostgreSQL SKU name"
  type        = string
  default     = "B_Standard_B1ms"
}

variable "db_storage_mb" {
  description = "PostgreSQL storage in MB"
  type        = number
  default     = 32768
}

variable "db_admin_username" {
  description = "PostgreSQL admin username"
  type        = string
  sensitive   = true
}

variable "db_admin_password" {
  description = "PostgreSQL admin password"
  type        = string
  sensitive   = true
}

variable "django_secret_key" {
  description = "Django SECRET_KEY"
  type        = string
  sensitive   = true
}

variable "jwt_key" {
  description = "JWT authentication key"
  type        = string
  sensitive   = true
}

variable "cookie_domain" {
  description = "Cookie domain"
  type        = string
}

variable "email_host_user" {
  description = "Email SMTP user"
  type        = string
  sensitive   = true
}

variable "email_host_password" {
  description = "Email SMTP password"
  type        = string
  sensitive   = true
}

variable "verification_url" {
  description = "Email verification URL"
  type        = string
}

variable "password_reset_url" {
  description = "Password reset URL"
  type        = string
}

variable "client_url" {
  description = "Client/Frontend URL"
  type        = string
}

