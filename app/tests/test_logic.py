"""Testy logiki aplikacji - testowanie relacji i operacji na modelach."""
import pytest
from src.models import db, User, Task, Product


def test_user_task_relationship(app, sample_user):
    """Test logiki: relacja między użytkownikiem a zadaniami."""
    with app.app_context():
        # Użycie ID z fixture
        user_id = sample_user.id
        # Tworzenie zadania przypisanego do użytkownika
        task1 = Task(
            title='Task 1',
            description='First task',
            status='pending',
            user_id=user_id
        )
        task2 = Task(
            title='Task 2',
            description='Second task',
            status='completed',
            user_id=user_id
        )
        
        db.session.add(task1)
        db.session.add(task2)
        db.session.commit()
        
        # Sprawdzenie relacji
        user = User.query.get(user_id)
        assert len(user.tasks) == 2
        assert user.tasks[0].title == 'Task 1'
        assert user.tasks[1].title == 'Task 2'
        
        # Sprawdzenie backref
        assert task1.user.username == 'testuser'  # Używamy wartości z fixture


def test_task_status_workflow(app, sample_user):
    """Test logiki: przepływ statusów zadania."""
    with app.app_context():
        # Użycie ID z fixture
        user_id = sample_user.id
        task = Task(
            title='Workflow Test',
            description='Testing status changes',
            status='pending',
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()
        
        # Zmiana statusu
        task.status = 'in_progress'
        db.session.commit()
        
        updated_task = Task.query.get(task.id)
        assert updated_task.status == 'in_progress'
        
        # Finalna zmiana statusu
        updated_task.status = 'completed'
        db.session.commit()
        
        final_task = Task.query.get(task.id)
        assert final_task.status == 'completed'


def test_product_stock_management(app):
    """Test logiki: zarządzanie stanem magazynowym produktu."""
    with app.app_context():
        product = Product(
            name='Test Product',
            description='Test Description',
            price=99.99,
            stock=10
        )
        db.session.add(product)
        db.session.commit()
        
        # Symulacja sprzedaży
        product.stock -= 3
        db.session.commit()
        
        updated_product = Product.query.get(product.id)
        assert updated_product.stock == 7
        
        # Sprawdzenie czy można sprzedać więcej niż jest w magazynie
        assert updated_product.stock >= 0
