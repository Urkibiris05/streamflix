"""
Actúa como un desarrollador backend senior. Crea los modelos de base de datos usando Python y Flask-SQLAlchemy 
para una aplicación llamada Streamflix. 
Necesito: 
    1. Una tabla para 'Usuarios' que incluya diferenciación entre rol estándar y administrador. 
    2. Una tabla para 'Películas'. 
    3. La relación necesaria (tabla intermedia) para que los usuarios puedan guardar películas en su lista 
    personal de favoritos (relación muchos a muchos).
"""

from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime

db = SQLAlchemy()


class RoleEnum(Enum):
    """Enumeración de roles de usuario"""
    STANDARD = "standard"
    ADMIN = "admin"


# Tabla asociativa para la relación muchos a muchos entre usuarios y películas favoritas
favorites = db.Table(
    'favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class User(db.Model):
    """Modelo para la tabla de Usuarios"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.STANDARD, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relación muchos a muchos con películas favoritas
    favorite_movies = db.relationship(
        'Movie',
        secondary=favorites,
        backref=db.backref('favorited_by', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_admin(self):
        """Verifica si el usuario tiene rol de administrador"""
        return self.role == RoleEnum.ADMIN


class Movie(db.Model):
    """Modelo para la tabla de Películas"""
    __tablename__ = 'movie'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    director = db.Column(db.String(255), nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    poster_url = db.Column(db.String(500), nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Movie {self.title}>'


