"""Konfiguracja pytest i fixtures."""
import pytest
from src.app import create_app
from src.models import db, User, Task, Product
from src.config import Config


class TestConfig(Config):
    """Konfiguracja testowa."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/test_db'
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
        return user


@pytest.fixture
def sample_task(app, sample_user):
    """Fixture tworząca przykładowe zadanie."""
    with app.app_context():
        task = Task(
            title='Test Task',
            description='Test Description',
            status='pending',
            user_id=sample_user.id
        )
        db.session.add(task)
        db.session.commit()
        return task
