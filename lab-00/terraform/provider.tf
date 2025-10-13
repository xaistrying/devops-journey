terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.42.0"
    }
  }
  cloud {
    organization = "xaistrying-org"
    workspaces {
      name = "workspace-xaistrying"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
