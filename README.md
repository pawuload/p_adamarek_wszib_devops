# DevOps Project: Flask + Nginx + PostgreSQL w Dockerze

Projekt demonstracyjny środowiska DevOps z wykorzystaniem Docker, Azure IaC oraz GitHub Actions CI/CD.

## Architektura

- **Backend**: Flask (Python)
- **Reverse Proxy**: Nginx
- **Baza danych**: PostgreSQL
- **Orkiestracja**: Docker Compose
- **Infrastruktura**: Azure (Resource Group + ACR)
- **CI/CD**: GitHub Actions

## Struktura projektu

```
.
├── app/
│   ├── src/           # Kod aplikacji Flask
│   ├── tests/         # Testy pytest
│   ├── seed/          # Skrypt seedowania bazy
│   ├── migrations/    # Migracje bazy danych
│   └── requirements.txt
├── docker/
│   └── nginx.conf     # Konfiguracja Nginx
├── infra/
│   ├── main.bicep     # Azure IaC (Bicep)
│   ├── parameters.json
│   └── README.md
├── .github/workflows/
│   ├── ci.yml         # Pipeline CI
│   └── cd.yml         # Pipeline CD
├── Dockerfile         # Wielostopniowy Dockerfile
└── docker-compose.yml
```

## Uruchomienie

```bash
# Budowanie i uruchomienie wszystkich serwisów
docker-compose up --build

# Aplikacja dostępna pod adresem:
# http://localhost
```

## Funkcjonalności

- Wielostopniowy Dockerfile (builder → test → final)
- Izolacja sieciowa (front_net dla publicznego ruchu, back_net dla bazy)
- Trwałe wolumeny dla danych, logów i outputu seedera
- Automatyczne migracje i seedowanie bazy
- Testy pytest w etapie build
- CI/CD z GitHub Actions
