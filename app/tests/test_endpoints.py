"""Testy endpointów HTTP."""
import pytest
import json
from src.models import db, User, Task, Product


def test_health_endpoint(client):
    """Test endpointu HTTP: /api/health."""
    response = client.get('/api/health')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'database' in data
    assert 'message' in data


def test_get_users_endpoint(client, sample_user):
    """Test endpointu HTTP: GET /api/users."""
    response = client.get('/api/users')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'users' in data
    assert 'count' in data
    assert data['count'] >= 1
    assert len(data['users']) >= 1


def test_get_user_by_id_endpoint(client, sample_user, app):
    """Test endpointu HTTP: GET /api/users/<id>."""
    # Użycie ID z fixture
    user_id = sample_user.id
    response = client.get(f'/api/users/{user_id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == user_id
    assert data['username'] == sample_user.username
    assert data['email'] == sample_user.email


def test_get_tasks_endpoint(client, sample_task):
    """Test endpointu HTTP: GET /api/tasks."""
    response = client.get('/api/tasks')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'tasks' in data
    assert 'count' in data
    assert data['count'] >= 1


def test_get_tasks_filtered_by_status(client, sample_task):
    """Test endpointu HTTP: GET /api/tasks?status=pending."""
    response = client.get('/api/tasks?status=pending')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'tasks' in data
    # Wszystkie zwrócone zadania powinny mieć status 'pending'
    for task in data['tasks']:
        assert task['status'] == 'pending'


def test_get_products_endpoint(client, app):
    """Test endpointu HTTP: GET /api/products."""
    with app.app_context():
        # Dodanie przykładowego produktu
        product = Product(
            name='Test Product',
            description='Test Description',
            price=99.99,
            stock=10
        )
        db.session.add(product)
        db.session.commit()
    
    response = client.get('/api/products')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'products' in data
    assert 'count' in data
    assert data['count'] >= 1
