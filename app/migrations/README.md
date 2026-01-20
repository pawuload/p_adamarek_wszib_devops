# Migracje bazy danych

Ten katalog zawiera migracje bazy danych zarządzane przez Flask-Migrate i Alembic.

## Uruchomienie migracji

Migracje są automatycznie uruchamiane przez kontener `migration_runner` w Docker Compose.

W przypadku ręcznego uruchomienia:

```bash
# Inicjalizacja (tylko raz)
flask db init

# Utworzenie migracji
flask db migrate -m "Description"

# Zastosowanie migracji
flask db upgrade
```
