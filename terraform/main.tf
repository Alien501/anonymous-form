terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "AnomyFormResourceGroup"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "anonymous-form"
  }
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "anonymous-form-${var.environment}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = var.app_service_sku

  tags = {
    Environment = var.environment
    Project     = "anonymous-form"
  }
}

# App Service (Backend)
resource "azurerm_linux_web_app" "backend" {
  name                = "anonymous-form-backend-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    always_on = false
    
    application_stack {
      python_version = "3.12"
    }
  }

  app_settings = {
    "ENVIRONMENT"                = var.environment
    "SECRET_KEY"                 = var.django_secret_key
    "JWT_KEY"                    = var.jwt_key
    "DB_NAME"                    = azurerm_postgresql_flexible_server_database.main.name
    "DB_USER"                    = azurerm_postgresql_flexible_server.main.administrator_login
    "DB_PASSWORD"                = azurerm_postgresql_flexible_server.main.administrator_password
    "DB_HOST"                    = azurerm_postgresql_flexible_server.main.fqdn
    "DB_PORT"                    = "5432"
    "COOKIE_DOMAIN"              = var.cookie_domain
    "EMAIL_HOST_USER"            = var.email_host_user
    "EMAIL_HOST_PASSWORD"        = var.email_host_password
    "VERIFICATION_URL"           = var.verification_url
    "PASSWORD_RESET_URL"         = var.password_reset_url
    "CLIENT_URL"                 = var.client_url
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }

  tags = {
    Environment = var.environment
    Project     = "anonymous-form"
  }
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "anonymous-form-db-${var.environment}"
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = "14"
  administrator_login    = var.db_admin_username
  administrator_password = var.db_admin_password
  storage_mb             = var.db_storage_mb
  sku_name               = var.db_sku_name

  backup_retention_days = 7

  tags = {
    Environment = var.environment
    Project     = "anonymous-form"
  }
}

# PostgreSQL Database
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "anonymousform"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# PostgreSQL Firewall Rule - Allow Azure Services
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure" {
  name             = "allow-azure-services"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# PostgreSQL Firewall Rule - Allow All (for development only)
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_all" {
  count            = var.environment == "dev" ? 1 : 0
  name             = "allow-all"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
} 

