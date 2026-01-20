"""Skrypt seedowania bazy danych - wypełnia bazę testowymi danymi."""
import sys
import os
import json
import csv
import logging
from datetime import datetime

# Dodanie ścieżki do modułów aplikacji
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import create_app
from src.models import db, User, Task, Product

# Konfiguracja logowania
LOG_DIR = '/seed_output'
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'seed.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def seed_database():
    """Główna funkcja seedowania bazy danych."""
    app = create_app()
    
    with app.app_context():
        logger.info("Rozpoczynanie seedowania bazy danych...")
        
        try:
            # Sprawdzenie czy baza jest dostępna
            db.session.execute(db.text('SELECT 1'))
            logger.info("Połączenie z bazą danych nawiązane pomyślnie")
            
            # Upewnienie się, że tabele istnieją
            try:
                db.session.execute(db.text('SELECT 1 FROM users LIMIT 1'))
                logger.info("Tabele istnieją w bazie danych")
            except Exception:
                logger.info("Tabele nie istnieją, tworzenie tabel z modeli...")
                db.create_all()
                logger.info("Tabele utworzone pomyślnie")
            
            # Czyszczenie istniejących danych (opcjonalne - dla czystego seedowania)
            logger.info("Czyszczenie istniejących danych...")
            try:
                Task.query.delete()
                Product.query.delete()
                User.query.delete()
                db.session.commit()
            except Exception as e:
                logger.warning(f"Nie można wyczyścić danych (może tabele są puste): {e}")
                db.session.rollback()
            
            # Tworzenie użytkowników
            logger.info("Tworzenie użytkowników...")
            users_data = [
                {'username': 'jan_kowalski', 'email': 'jan.kowalski@example.com'},
                {'username': 'anna_nowak', 'email': 'anna.nowak@example.com'},
                {'username': 'piotr_wisniewski', 'email': 'piotr.wisniewski@example.com'},
                {'username': 'maria_wojcik', 'email': 'maria.wojcik@example.com'},
                {'username': 'tomasz_kowalczyk', 'email': 'tomasz.kowalczyk@example.com'},
            ]
            
            users = []
            for user_data in users_data:
                user = User(**user_data)
                db.session.add(user)
                users.append(user)
            
            db.session.commit()
            logger.info(f"Utworzono {len(users)} użytkowników")
            
            # Tworzenie zadań
            logger.info("Tworzenie zadań...")
            tasks_data = [
                {'title': 'Zaimplementować endpoint /health', 'description': 'Stworzyć endpoint sprawdzający stan aplikacji', 'status': 'completed', 'user_id': users[0].id},
                {'title': 'Napisać testy jednostkowe', 'description': 'Utworzyć testy dla modeli danych', 'status': 'completed', 'user_id': users[0].id},
                {'title': 'Skonfigurować Docker Compose', 'description': 'Przygotować docker-compose.yml z wszystkimi serwisami', 'status': 'in_progress', 'user_id': users[1].id},
                {'title': 'Utworzyć migracje bazy danych', 'description': 'Skonfigurować Flask-Migrate i utworzyć migracje', 'status': 'completed', 'user_id': users[1].id},
                {'title': 'Zaimplementować seeder', 'description': 'Stworzyć skrypt seedujący bazę danych', 'status': 'completed', 'user_id': users[2].id},
                {'title': 'Skonfigurować Nginx', 'description': 'Przygotować konfigurację reverse proxy', 'status': 'pending', 'user_id': users[2].id},
            ]
            
            tasks = []
            for task_data in tasks_data:
                task = Task(**task_data)
                db.session.add(task)
                tasks.append(task)
            
            db.session.commit()
            logger.info(f"Utworzono {len(tasks)} zadań")
            
            # Tworzenie produktów
            logger.info("Tworzenie produktów...")
            products_data = [
                {'name': 'Laptop Dell XPS 15', 'description': 'Wydajny laptop do pracy i rozrywki', 'price': 4999.99, 'stock': 15},
                {'name': 'Mysz Logitech MX Master 3', 'description': 'Ergonomiczna mysz bezprzewodowa', 'price': 399.99, 'stock': 30},
                {'name': 'Klawiatura mechaniczna', 'description': 'Klawiatura z przełącznikami Cherry MX', 'price': 599.99, 'stock': 20},
                {'name': 'Monitor 27 cali 4K', 'description': 'Monitor z rozdzielczością 4K UHD', 'price': 2499.99, 'stock': 10},
                {'name': 'Słuchawki bezprzewodowe', 'description': 'Słuchawki z redukcją szumów', 'price': 899.99, 'stock': 25},
            ]
            
            products = []
            for product_data in products_data:
                product = Product(**product_data)
                db.session.add(product)
                products.append(product)
            
            db.session.commit()
            logger.info(f"Utworzono {len(products)} produktów")
            
            # Generowanie plików wyjściowych
            logger.info("Generowanie plików wyjściowych...")
            
            # 1. Zapisywanie users.csv
            csv_path = os.path.join(LOG_DIR, 'users.csv')
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'username', 'email', 'created_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for user in users:
                    writer.writerow({
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'created_at': user.created_at.isoformat() if user.created_at else ''
                    })
            logger.info(f"Zapisano plik users.csv: {csv_path}")
            
            # 2. Zapisywanie data.json
            json_data = {
                'seed_timestamp': datetime.utcnow().isoformat(),
                'summary': {
                    'users_count': len(users),
                    'tasks_count': len(tasks),
                    'products_count': len(products)
                },
                'users': [user.to_dict() for user in users],
                'tasks': [task.to_dict() for task in tasks],
                'products': [product.to_dict() for product in products]
            }
            
            json_path = os.path.join(LOG_DIR, 'data.json')
            with open(json_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(json_data, jsonfile, indent=2, ensure_ascii=False)
            logger.info(f"Zapisano plik data.json: {json_path}")
            
            logger.info("Seedowanie zakończone pomyślnie!")
            logger.info(f"Utworzono łącznie: {len(users)} użytkowników, {len(tasks)} zadań, {len(products)} produktów")
            
        except Exception as e:
            logger.error(f"Błąd podczas seedowania: {e}", exc_info=True)
            db.session.rollback()
            sys.exit(1)


if __name__ == '__main__':
    seed_database()
