resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    environment = var.env
  }
}

resource "azurerm_virtual_network" "vnet" {
  name                = var.virtual_network_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
  dns_servers         = ["10.0.0.4", "10.0.0.5"]

  subnet {
    name             = "web_subnet"
    address_prefixes = ["10.0.1.0/24"]
  }

  subnet {
    name             = "db-subnet"
    address_prefixes = ["10.0.2.0/24"]
  }

  tags = {
    environment = var.env
  }
}
