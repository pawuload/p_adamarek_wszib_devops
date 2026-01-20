"""Endpointy API aplikacji Flask."""
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from .models import db, User, Task, Product

api = Blueprint('api', __name__)


@api.route('/health', methods=['GET'])
def health_check():
    """Endpoint sprawdzający stan aplikacji."""
    try:
        # Sprawdzenie połączenia z bazą danych
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'message': 'Aplikacja działa poprawnie'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 503


@api.route('/users', methods=['GET'])
def get_users():
    """Pobranie listy wszystkich użytkowników."""
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Błąd bazy danych: {str(e)}'}), 500


@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Pobranie pojedynczego użytkownika."""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Błąd bazy danych: {str(e)}'}), 500


@api.route('/tasks', methods=['GET'])
def get_tasks():
    """Pobranie listy wszystkich zadań."""
    try:
        # Opcjonalne filtrowanie po statusie
        status = request.args.get('status')
        query = Task.query
        if status:
            query = query.filter_by(status=status)
        
        tasks = query.all()
        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Błąd bazy danych: {str(e)}'}), 500


@api.route('/products', methods=['GET'])
def get_products():
    """Pobranie listy wszystkich produktów."""
    try:
        products = Product.query.all()
        return jsonify({
            'products': [product.to_dict() for product in products],
            'count': len(products)
        }), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Błąd bazy danych: {str(e)}'}), 500


@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Pobranie pojedynczego produktu."""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Błąd bazy danych: {str(e)}'}), 500
