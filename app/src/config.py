"""Konfiguracja aplikacji Flask."""
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config:
    """Podstawowa konfiguracja aplikacji."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Konfiguracja bazy danych PostgreSQL
    DB_HOST = os.environ.get('DB_HOST', 'db')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'devops_db')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Konfiguracja aplikacji
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
