"""Skrypt do uruchamiania migracji bazy danych."""
import sys
import os
from flask_migrate import upgrade

# Dodanie ścieżki do modułów aplikacji
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import create_app

def run_migrations():
    """Uruchamia wszystkie oczekujące migracje."""
    from src.models import db
    
    app = create_app()
    
    with app.app_context():
        print("Rozpoczynanie migracji bazy danych...")
        try:
            # Próba użycia Flask-Migrate
            upgrade()
            print("Migracje zakończone pomyślnie!")
        except Exception as e:
            print(f"Flask-Migrate nie jest dostępny ({e}), używam db.create_all()...")
            # Fallback: tworzenie tabel bezpośrednio z modeli
            try:
                db.create_all()
                print("Tabele utworzone pomyślnie!")
            except Exception as create_error:
                print(f"Błąd podczas tworzenia tabel: {create_error}")
                sys.exit(1)

if __name__ == '__main__':
    run_migrations()
