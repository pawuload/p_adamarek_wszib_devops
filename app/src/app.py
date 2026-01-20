"""Główny plik aplikacji Flask."""
from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .models import db
from .routes import api


def create_app(config_class=Config):
    """Factory function do tworzenia instancji aplikacji Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicjalizacja rozszerzeń
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Rejestracja blueprintów
    app.register_blueprint(api, url_prefix='/api')
    
    # Endpoint główny
    @app.route('/')
    def index():
        return {
            'message': 'DevOps Project API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'users': '/api/users',
                'tasks': '/api/tasks',
                'products': '/api/products'
            }
        }
    
    return app


# Dla uruchomienia bezpośrednio (development)
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
