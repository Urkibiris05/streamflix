"""
Configuración de la aplicación Streamflix
"""

import os
from datetime import timedelta

# ==================== CONFIGURACIÓN DE BASE DE DATOS ====================
class Config:
    """Configuración base"""
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/streamflix'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # Seguridad
    SECRET_KEY = 'tu_clave_secreta_muy_segura_cambiar_en_produccion'
    
    # JWT
    JWT_SECRET_KEY = 'tu_jwt_secret_key_cambiar_en_produccion'
    JWT_EXPIRATION_DELTA = timedelta(hours=24)
    
    # CORS
    CORS_ORIGINS = ["http://localhost:8000", "http://localhost:3000", "http://127.0.0.1:8000"]
    
    # Configuración de la app
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', Config.SQLALCHEMY_DATABASE_URI)


class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Seleccionar configuración según el ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
