"""Konfiguracja pytest i fixtures."""
import pytest
from src.app import create_app
from src.models import db, User, Task, Product
from src.config import Config


class TestConfig(Config):
    """Konfiguracja testowa."""
    TESTING = True
    # Używamy SQLite w pamięci dla testów - działa bez zewnętrznej bazy danych
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    """Fixture tworząca aplikację Flask dla testów."""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Fixture tworząca klienta testowego."""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Fixture tworząca przykładowego użytkownika."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        # Pobranie ID przed wyjściem z kontekstu - ID jest dostępne nawet po expunge
        user_id = user.id
        # Odłączenie obiektu od sesji, ale ID pozostanie dostępne
        db.session.expunge(user)
        # Ustawienie ID bezpośrednio na obiekcie
        user.id = user_id
        return user


@pytest.fixture
def sample_task(app, sample_user):
    """Fixture tworząca przykładowe zadanie."""
    with app.app_context():
        # Użycie ID z fixture sample_user (dostępne nawet po expunge)
        user_id = sample_user.id
        task = Task(
            title='Test Task',
            description='Test Description',
            status='pending',
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()
        # Pobranie ID przed wyjściem z kontekstu
        task_id = task.id
        # Odłączenie obiektu od sesji
        db.session.expunge(task)
        # Ustawienie ID bezpośrednio
        task.id = task_id
        task.user_id = user_id
        return task
