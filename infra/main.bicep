// Azure Infrastructure as Code - Bicep
// Tworzy Resource Group i Azure Container Registry (ACR)

@description('Nazwa projektu - używana do nazewnictwa zasobów')
param projectName string = 'devops'

@description('Lokalizacja zasobów Azure')
param location string = resourceGroup().location

@description('Nazwa Resource Group')
param resourceGroupName string = 'rg-${projectName}'

@description('Nazwa Azure Container Registry')
param acrName string = 'acr${projectName}${uniqueString(resourceGroup().id)}'

@description('SKU dla Azure Container Registry (Basic, Standard, Premium)')
param acrSku string = 'Basic'

@description('Czy włączyć admin user dla ACR')
param acrAdminEnabled bool = true

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
}

// Azure Container Registry
resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: acrName
  location: location
  sku: {
    name: acrSku
  }
  properties: {
    adminUserEnabled: acrAdminEnabled
    publicNetworkAccess: 'Enabled'
  }
}

// Outputs
output resourceGroupName string = rg.name
output acrName string = acr.name
output acrLoginServer string = acr.properties.loginServer
output acrAdminUsername string = acr.listCredentials().username
output acrAdminPassword string = acr.listCredentials().passwords[0].value
