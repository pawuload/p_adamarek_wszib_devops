"""Testy jednostkowe - testowanie pojedynczych funkcji i metod."""
import pytest
from datetime import datetime
from src.models import User, Task, Product


def test_user_to_dict():
    """Test jednostkowy: konwersja modelu User do słownika."""
    user = User(
        id=1,
        username='john_doe',
        email='john@example.com',
        created_at=datetime(2024, 1, 1, 12, 0, 0)
    )
    
    result = user.to_dict()
    
    assert result['id'] == 1
    assert result['username'] == 'john_doe'
    assert result['email'] == 'john@example.com'
    assert result['created_at'] == '2024-01-01T12:00:00'
    assert isinstance(result, dict)


def test_task_to_dict():
    """Test jednostkowy: konwersja modelu Task do słownika."""
    task = Task(
        id=1,
        title='Complete project',
        description='Finish the DevOps project',
        status='in_progress',
        user_id=1,
        created_at=datetime(2024, 1, 1, 12, 0, 0)
    )
    
    result = task.to_dict()
    
    assert result['id'] == 1
    assert result['title'] == 'Complete project'
    assert result['status'] == 'in_progress'
    assert result['user_id'] == 1
    assert isinstance(result, dict)


def test_product_to_dict():
    """Test jednostkowy: konwersja modelu Product do słownika."""
    product = Product(
        id=1,
        name='Laptop',
        description='Gaming laptop',
        price=2999.99,
        stock=10
    )
    
    result = product.to_dict()
    
    assert result['id'] == 1
    assert result['name'] == 'Laptop'
    assert float(result['price']) == 2999.99
    assert result['stock'] == 10
    assert isinstance(result, dict)
