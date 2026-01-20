# Azure Infrastructure as Code

Ten katalog zawiera definicje infrastruktury Azure w formacie Bicep.

## Zasoby

Infrastruktura tworzy następujące zasoby:
- **Resource Group** - grupa zasobów zawierająca wszystkie komponenty
- **Azure Container Registry (ACR)** - rejestr kontenerów Docker do przechowywania obrazów

## Wymagania

- Azure CLI zainstalowane i skonfigurowane
- Uprawnienia do tworzenia zasobów w subskrypcji Azure

## Wdrożenie

### 1. Logowanie do Azure

```bash
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### 2. Utworzenie Resource Group (jeśli nie istnieje)

```bash
az group create --name rg-devops --location "West Europe"
```

### 3. Wdrożenie infrastruktury

```bash
# Z katalogu infra/
az deployment group create \
  --resource-group rg-devops \
  --template-file main.bicep \
  --parameters @parameters.json
```

### 4. Pobranie danych dostępowych do ACR

Po wdrożeniu, dane dostępowe do ACR są dostępne w outputach:

```bash
az deployment group show \
  --resource-group rg-devops \
  --name main \
  --query properties.outputs
```

### 5. Logowanie do ACR

```bash
az acr login --name <acr-name>
```

## Uwagi

- Aplikacja **nie działa w Azure** - Azure jest używany tylko jako IaC + registry
- Obrazy Docker są budowane lokalnie lub w GitHub Actions i pushowane do ACR
- Środowisko produkcyjne działa lokalnie w Docker Compose

## Struktura plików

- `main.bicep` - główny plik definicji infrastruktury
- `parameters.json` - parametry wdrożenia
- `README.md` - dokumentacja (ten plik)
