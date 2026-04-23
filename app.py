import os
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import text
from datetime import datetime, timezone

# ==================== CONFIGURACIÓN ====================
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_url_path='', static_folder='.')
app.config['SECRET_KEY'] = 'tu_clave_secreta'

# Configuración de base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'streamflix.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==================== MODELOS DE BASE DE DATOS ====================
class User(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

    favorites = db.relationship('Favorites', backref='user', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    director = db.Column(db.String(255))
    genre = db.Column(db.String(100))
    release_date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    rating = db.Column(db.Float)
    poster_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    favorited_by = db.relationship('Favorites', backref='movie', lazy=True)

class Favorites(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Puntuación del 1 al 10
    review_text = db.Column(db.Text, nullable=True)  # Crítica del usuario
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    user = db.relationship('User', backref='reviews')
    movie = db.relationship('Movie', backref='reviews')

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    director = db.Column(db.String(255))
    genre = db.Column(db.String(100))
    release_date = db.Column(db.Date)
    poster_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    episodes = db.relationship('Episode', backref='series', lazy=True, cascade='all, delete-orphan')
    favorited_by = db.relationship('SeriesFavorites', backref='series', lazy=True)

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    season = db.Column(db.Integer, nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    air_date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    video_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class SeriesFavorites(db.Model):
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# ==================== FUNCIONES DE INICIALIZACIÓN ====================
def init_db():
    """Inicializar base de datos y crear tablas"""
    with app.app_context():
        db.create_all()

        # Ejecutar seed data si no hay datos
        if User.query.count() == 0 or Movie.query.count() == 0:
            print("Poblando base de datos con datos iniciales...")
            seed_path = os.path.join(basedir, 'seed.sql')
            try:
                # Usar sqlite3 directamente para ejecutar el seed.sql
                # porque SQLAlchemy no maneja bien los comandos multi-línea
                import sqlite3
                sql_conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
                sql_conn.isolation_level = None
                
                with open(seed_path, 'r', encoding='utf-8') as f:
                    sql_commands = f.read()
                    sql_conn.executescript(sql_commands)
                
                sql_conn.close()
                db.session.commit()
                print("Base de datos poblada correctamente")
            except FileNotFoundError:
                print("Archivo seed.sql no encontrado, creando datos básicos...")

                demo_movies = [
                    Movie(title='Inception', description='A skilled thief who steals corporate secrets through the use of dream-sharing technology.', director='Christopher Nolan', genre='Sci-Fi', release_date='2010-07-16', duration_minutes=148, rating=8.8, poster_url='https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300'),
                    Movie(title='The Matrix', description='A hacker learns about the true nature of his reality and his role in the war against its controllers.', director='The Wachowskis', genre='Sci-Fi', release_date='1999-03-31', duration_minutes=136, rating=8.7, poster_url='https://images.unsplash.com/photo-1485095329183-d0daf68471ca?w=300')
                ]
                db.session.add_all(demo_movies)
                db.session.commit()
                print("Base de datos inicial creada con datos básicos")
        else:
            print("Base de datos ya contiene datos; no es necesario sembrar de nuevo.")


# ==================== FUNCIÓN CORS MANUAL ====================
def add_cors_headers(response):
    """Agregar headers CORS manualmente"""
    # Si es un tuple (data, status), convertir a Response
    if isinstance(response, tuple):
        data, status = response
        response = make_response(data, status)
    elif not hasattr(response, 'headers'):
        # Si no es Response, convertirlo
        response = make_response(response)
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# ==================== DECORADOR CORS ====================
def cors_enabled(f):
    """Decorador para habilitar CORS en rutas específicas"""
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            # Responder a preflight requests
            response = make_response()
            return add_cors_headers(response)
        response = f(*args, **kwargs)
        return add_cors_headers(response)
    wrapper.__name__ = f.__name__
    return wrapper

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

@app.after_request
def apply_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# ==================== RUTAS ====================

# --- SERVIR FRONTEND ---
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/app.js')
def serve_js():
    return send_from_directory('.', 'app.js')

# --- API: REGISTRO ---
@app.route('/api/registro', methods=['POST'])
@cors_enabled
def registro():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        email = datos.get('email')
        password = datos.get('password')
        username = datos.get('username')

        if not email or not password or not username:
            return jsonify({'error': 'Email, username y contraseña son requeridos'}), 400

        # Verificar si email ya existe
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'El email ya está registrado'}), 409

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'El username ya está registrado'}), 409

        # Hashear contraseña
        salt = gensalt()
        password_hash = hashpw(password.encode('utf-8'), salt)

        # Crear usuario
        usuario = User(
            username=username,
            email=email,
            password_hash=password_hash.decode('utf-8'),
            role='user'
        )
        db.session.add(usuario)
        db.session.commit()

        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'role': usuario.role
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- API: LOGIN ---
@app.route('/api/login', methods=['POST'])
@cors_enabled
def login():
    try:
        datos = request.get_json()
        if not datos or not datos.get('email') or not datos.get('password'):
            return jsonify({'error': 'Email y contraseña requeridos'}), 400

        email = datos['email']
        password = datos['password']

        # Buscar usuario
        usuario = User.query.filter_by(email=email).first()
        if not usuario:
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401

        # Verificar contraseña
        if not checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401

        # Generar token simple (no JWT por simplicidad)
        token = f"token_{usuario.id}_{usuario.username}"

        return jsonify({
            'token': token,
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'role': usuario.role
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- API: PELÍCULAS ---
@app.route('/api/peliculas', methods=['GET'])
@cors_enabled
def obtener_peliculas():
    try:
        peliculas = Movie.query.all()
        return jsonify([{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'director': p.director,
            'genre': p.genre,
            'release_date': p.release_date.isoformat() if p.release_date else None,
            'duration_minutes': p.duration_minutes,
            'rating': p.rating,
            'poster_url': p.poster_url,
            'video_url': p.video_url,
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'updated_at': p.updated_at.isoformat() if p.updated_at else None
        } for p in peliculas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:id>', methods=['GET'])
@cors_enabled
def obtener_pelicula(id):
    try:
        pelicula = db.session.get(Movie, id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404
        return jsonify({
            'id': pelicula.id,
            'title': pelicula.title,
            'description': pelicula.description,
            'director': pelicula.director,
            'genre': pelicula.genre,
            'release_date': pelicula.release_date.isoformat() if pelicula.release_date else None,
            'duration_minutes': pelicula.duration_minutes,
            'rating': pelicula.rating,
            'poster_url': pelicula.poster_url,
            'video_url': pelicula.video_url,
            'created_at': pelicula.created_at.isoformat() if pelicula.created_at else None,
            'updated_at': pelicula.updated_at.isoformat() if pelicula.updated_at else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas', methods=['POST'])
@cors_enabled
def crear_pelicula():
    try:
        # Obtener user_id del token y verificar rol admin
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        usuario = db.session.get(User, user_id)
        if not usuario or usuario.role != 'admin':
            return jsonify({'error': 'Acceso denegado. Solo administradores pueden crear películas.'}), 403

        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Validar campos requeridos
        if not datos.get('title'):
            return jsonify({'error': 'El título es requerido'}), 400

        # Procesar y validar datos
        release_date_str = datos.get('release_date')
        if release_date_str and release_date_str != '':
            try:
                release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Fecha de lanzamiento inválida'}), 400
        else:
            release_date = None

        duration_minutes = datos.get('duration_minutes')
        if duration_minutes == '' or duration_minutes is None:
            duration_minutes = None
        else:
            try:
                duration_minutes = int(duration_minutes)
            except (ValueError, TypeError):
                return jsonify({'error': 'Duración debe ser un número entero'}), 400

        rating = datos.get('rating')
        if rating == '' or rating is None:
            rating = None
        else:
            try:
                rating = float(rating)
            except (ValueError, TypeError):
                return jsonify({'error': 'Calificación debe ser un número'}), 400

        # Crear película
        pelicula = Movie(
            title=datos['title'],
            description=datos.get('description') or None,
            director=datos.get('director') or None,
            genre=datos.get('genre') or None,
            release_date=release_date,
            duration_minutes=duration_minutes,
            rating=rating,
            poster_url=datos.get('poster_url') or None,
            video_url=datos.get('video_url') or None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        db.session.add(pelicula)
        db.session.commit()

        return jsonify({
            'mensaje': 'Película creada exitosamente',
            'pelicula': {
                'id': pelicula.id,
                'title': pelicula.title,
                'description': pelicula.description,
                'director': pelicula.director,
                'genre': pelicula.genre,
                'release_date': pelicula.release_date.isoformat() if pelicula.release_date else None,
                'duration_minutes': pelicula.duration_minutes,
                'rating': pelicula.rating,
                'poster_url': pelicula.poster_url,
                'video_url': pelicula.video_url,
                'created_at': pelicula.created_at.isoformat() if pelicula.created_at else None,
                'updated_at': pelicula.updated_at.isoformat() if pelicula.updated_at else None
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:id>', methods=['PUT'])
@cors_enabled
def editar_pelicula(id):
    try:
        # Obtener user_id del token y verificar rol admin
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        usuario = db.session.get(User, user_id)
        if not usuario or usuario.role != 'admin':
            return jsonify({'error': 'Acceso denegado. Solo administradores pueden editar películas.'}), 403

        pelicula = db.session.get(Movie, id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Actualizar campos
        if 'title' in datos:
            pelicula.title = datos['title']
        if 'description' in datos:
            pelicula.description = datos['description'] or None
        if 'director' in datos:
            pelicula.director = datos['director'] or None
        if 'genre' in datos:
            pelicula.genre = datos['genre'] or None
        if 'release_date' in datos:
            release_date_str = datos['release_date']
            if release_date_str and release_date_str != '':
                try:
                    pelicula.release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Fecha de lanzamiento inválida'}), 400
            else:
                pelicula.release_date = None
        if 'duration_minutes' in datos:
            duration_minutes = datos['duration_minutes']
            if duration_minutes == '' or duration_minutes is None:
                pelicula.duration_minutes = None
            else:
                try:
                    pelicula.duration_minutes = int(duration_minutes)
                except (ValueError, TypeError):
                    return jsonify({'error': 'Duración debe ser un número entero'}), 400
        if 'rating' in datos:
            rating = datos['rating']
            if rating == '' or rating is None:
                pelicula.rating = None
            else:
                try:
                    pelicula.rating = float(rating)
                except (ValueError, TypeError):
                    return jsonify({'error': 'Calificación debe ser un número'}), 400
        if 'poster_url' in datos:
            pelicula.poster_url = datos['poster_url'] or None
        if 'video_url' in datos:
            pelicula.video_url = datos['video_url'] or None

        # Forzar actualización de updated_at
        pelicula.updated_at = datetime.now(timezone.utc)

        db.session.commit()

        return jsonify({
            'mensaje': 'Película actualizada exitosamente',
            'pelicula': {
                'id': pelicula.id,
                'title': pelicula.title,
                'description': pelicula.description,
                'director': pelicula.director,
                'genre': pelicula.genre,
                'release_date': pelicula.release_date.isoformat() if pelicula.release_date else None,
                'duration_minutes': pelicula.duration_minutes,
                'rating': pelicula.rating,
                'poster_url': pelicula.poster_url,
                'video_url': pelicula.video_url,
                'created_at': pelicula.created_at.isoformat() if pelicula.created_at else None,
                'updated_at': pelicula.updated_at.isoformat() if pelicula.updated_at else None
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:id>', methods=['DELETE'])
@cors_enabled
def eliminar_pelicula(id):
    try:
        # Obtener user_id del token y verificar rol admin
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        usuario = db.session.get(User, user_id)
        if not usuario or usuario.role != 'admin':
            return jsonify({'error': 'Acceso denegado. Solo administradores pueden eliminar películas.'}), 403

        pelicula = db.session.get(Movie, id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404
        
        # Eliminar favoritos asociados primero
        Favorites.query.filter_by(movie_id=id).delete()
        
        db.session.delete(pelicula)
        db.session.commit()

        return jsonify({'mensaje': 'Película eliminada exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- API: FAVORITOS ---
@app.route('/api/favoritos', methods=['GET'])
@cors_enabled
def obtener_favoritos():
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        # Obtener películas favoritas
        # Usar JOIN explícito para asegurar que la relación se establece correctamente
        favoritos = db.session.query(Movie).join(
            Favorites, 
            Movie.id == Favorites.movie_id
        ).filter(Favorites.user_id == user_id).all()
        
        print(f"Favoritos encontrados para user_id {user_id}: {len(favoritos)}")
        
        return jsonify([{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'director': p.director,
            'genre': p.genre,
            'release_date': p.release_date.isoformat() if p.release_date else None,
            'duration_minutes': p.duration_minutes,
            'rating': p.rating,
            'poster_url': p.poster_url,
            'video_url': p.video_url
        } for p in favoritos]), 200

    except Exception as e:
        print(f"Error en obtener_favoritos: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/favoritos', methods=['POST'])
@cors_enabled
def agregar_favorito():
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        datos = request.get_json()
        movie_id = datos.get('movie_id')
        if not movie_id:
            return jsonify({'error': 'movie_id es requerido'}), 400

        print(f"Intentando agregar favorito: user_id={user_id}, movie_id={movie_id}")

        # Verificar que la película existe
        movie = db.session.get(Movie, movie_id)
        if not movie:
            print(f"Película con ID {movie_id} no encontrada")
            return jsonify({'error': 'Película no encontrada'}), 404

        # Verificar que no esté ya en favoritos
        existing = Favorites.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing:
            print(f"La película {movie_id} ya existe en favoritos para user {user_id}")
            return jsonify({'error': 'La película ya está en favoritos'}), 409

        favorito = Favorites(user_id=user_id, movie_id=movie_id)
        db.session.add(favorito)
        db.session.commit()

        print(f"Favorito agregado exitosamente: user_id={user_id}, movie_id={movie_id}")
        
        # Verificar que se guardó correctamente
        verificar = Favorites.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if verificar:
            print(f"✓ Verificación exitosa: Favorito guardado en BD")
        else:
            print(f"✗ ADVERTENCIA: Favorito NO fue guardado en BD")

        return jsonify({'mensaje': 'Película agregada a favoritos'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error en agregar_favorito: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/favoritos/<int:movie_id>', methods=['DELETE'])
@cors_enabled
def quitar_favorito(movie_id):
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        print(f"Intentando eliminar favorito: user_id={user_id}, movie_id={movie_id}")

        # Buscar y eliminar favorito
        favorito = Favorites.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if not favorito:
            print(f"Favorito no encontrado: user_id={user_id}, movie_id={movie_id}")
            return jsonify({'error': 'Película no está en favoritos'}), 404

        db.session.delete(favorito)
        db.session.commit()

        print(f"Favorito eliminado exitosamente: user_id={user_id}, movie_id={movie_id}")

        return jsonify({'mensaje': 'Película eliminada de favoritos'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error en quitar_favorito: {str(e)}")
        return jsonify({'error': str(e)}), 500

# --- API: SERIES ---
@app.route('/api/series', methods=['GET'])
@cors_enabled
def obtener_series():
    try:
        series = Series.query.all()
        return jsonify([{
            'id': s.id,
            'title': s.title,
            'description': s.description,
            'director': s.director,
            'genre': s.genre,
            'release_date': s.release_date.isoformat() if s.release_date else None,
            'poster_url': s.poster_url,
            'created_at': s.created_at.isoformat() if s.created_at else None,
            'updated_at': s.updated_at.isoformat() if s.updated_at else None
        } for s in series]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/series/<int:id>', methods=['GET'])
@cors_enabled
def obtener_serie(id):
    try:
        serie = db.session.get(Series, id)
        if not serie:
            return jsonify({'error': 'Serie no encontrada'}), 404
        
        # Obtener todos los episodios ordenados por temporada y número
        episodios = Episode.query.filter_by(series_id=id).order_by(Episode.season, Episode.episode_number).all()
        
        # Agrupar episodios por temporada
        episodes_by_season = {}
        for ep in episodios:
            season = ep.season
            if season not in episodes_by_season:
                episodes_by_season[season] = []
            episodes_by_season[season].append({
                'id': ep.id,
                'title': ep.title,
                'description': ep.description,
                'season': ep.season,
                'episode_number': ep.episode_number,
                'air_date': ep.air_date.isoformat() if ep.air_date else None,
                'duration_minutes': ep.duration_minutes,
                'video_url': ep.video_url,
                'created_at': ep.created_at.isoformat() if ep.created_at else None,
                'updated_at': ep.updated_at.isoformat() if ep.updated_at else None
            })
        
        return jsonify({
            'id': serie.id,
            'title': serie.title,
            'description': serie.description,
            'director': serie.director,
            'genre': serie.genre,
            'release_date': serie.release_date.isoformat() if serie.release_date else None,
            'poster_url': serie.poster_url,
            'episodes_by_season': episodes_by_season,
            'created_at': serie.created_at.isoformat() if serie.created_at else None,
            'updated_at': serie.updated_at.isoformat() if serie.updated_at else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/series/<int:series_id>/episodes', methods=['GET'])
@cors_enabled
def obtener_episodios_serie(series_id):
    try:
        serie = db.session.get(Series, series_id)
        if not serie:
            return jsonify({'error': 'Serie no encontrada'}), 404
        
        episodios = Episode.query.filter_by(series_id=series_id).order_by(Episode.season, Episode.episode_number).all()
        
        return jsonify([{
            'id': ep.id,
            'title': ep.title,
            'description': ep.description,
            'season': ep.season,
            'episode_number': ep.episode_number,
            'air_date': ep.air_date.isoformat() if ep.air_date else None,
            'duration_minutes': ep.duration_minutes,
            'video_url': ep.video_url,
            'created_at': ep.created_at.isoformat() if ep.created_at else None,
            'updated_at': ep.updated_at.isoformat() if ep.updated_at else None
        } for ep in episodios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/episodes/<int:id>', methods=['GET'])
@cors_enabled
def obtener_episodio(id):
    try:
        episodio = db.session.get(Episode, id)
        if not episodio:
            return jsonify({'error': 'Episodio no encontrado'}), 404
        
        return jsonify({
            'id': episodio.id,
            'series_id': episodio.series_id,
            'series_title': episodio.series.title,
            'title': episodio.title,
            'description': episodio.description,
            'season': episodio.season,
            'episode_number': episodio.episode_number,
            'air_date': episodio.air_date.isoformat() if episodio.air_date else None,
            'duration_minutes': episodio.duration_minutes,
            'video_url': episodio.video_url,
            'created_at': episodio.created_at.isoformat() if episodio.created_at else None,
            'updated_at': episodio.updated_at.isoformat() if episodio.updated_at else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- API: FAVORITOS DE SERIES ---
@app.route('/api/series-favoritos', methods=['GET'])
@cors_enabled
def obtener_series_favoritos():
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        # Obtener series favoritas
        series_fav = db.session.query(Series).join(
            SeriesFavorites, 
            Series.id == SeriesFavorites.series_id
        ).filter(SeriesFavorites.user_id == user_id).all()
        
        return jsonify([{
            'id': s.id,
            'title': s.title,
            'description': s.description,
            'director': s.director,
            'genre': s.genre,
            'release_date': s.release_date.isoformat() if s.release_date else None,
            'poster_url': s.poster_url
        } for s in series_fav]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/series-favoritos', methods=['POST'])
@cors_enabled
def agregar_serie_favorito():
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        datos = request.get_json()
        series_id = datos.get('series_id')
        if not series_id:
            return jsonify({'error': 'series_id es requerido'}), 400

        # Verificar que la serie existe
        serie = db.session.get(Series, series_id)
        if not serie:
            return jsonify({'error': 'Serie no encontrada'}), 404

        # Verificar que no esté ya en favoritos
        existing = SeriesFavorites.query.filter_by(user_id=user_id, series_id=series_id).first()
        if existing:
            return jsonify({'error': 'La serie ya está en favoritos'}), 409

        favorito = SeriesFavorites(user_id=user_id, series_id=series_id)
        db.session.add(favorito)
        db.session.commit()

        return jsonify({'mensaje': 'Serie agregada a favoritos'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/series-favoritos/<int:series_id>', methods=['DELETE'])
@cors_enabled
def quitar_serie_favorito(series_id):
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        # Buscar y eliminar favorito
        favorito = SeriesFavorites.query.filter_by(user_id=user_id, series_id=series_id).first()
        if not favorito:
            return jsonify({'error': 'Serie no está en favoritos'}), 404

        db.session.delete(favorito)
        db.session.commit()

        return jsonify({'mensaje': 'Serie eliminada de favoritos'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- API: CRÍTICAS Y RATINGS ---
@app.route('/api/peliculas/<int:movie_id>/reviews', methods=['GET'])
@cors_enabled
def obtener_reviews_pelicula(movie_id):
    try:
        pelicula = db.session.get(Movie, movie_id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404

        reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.created_at.desc()).all()
        
        return jsonify([{
            'id': r.id,
            'user_id': r.user_id,
            'username': r.user.username,
            'movie_id': r.movie_id,
            'rating': r.rating,
            'review_text': r.review_text,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'updated_at': r.updated_at.isoformat() if r.updated_at else None
        } for r in reviews]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:movie_id>/average-rating', methods=['GET'])
@cors_enabled
def obtener_rating_promedio(movie_id):
    try:
        from sqlalchemy import func
        
        pelicula = db.session.get(Movie, movie_id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404

        resultado = db.session.query(
            func.avg(Review.rating).label('average_rating'),
            func.count(Review.id).label('total_reviews')
        ).filter(Review.movie_id == movie_id).first()

        average_rating = float(resultado.average_rating) if resultado.average_rating else 0
        total_reviews = resultado.total_reviews or 0

        return jsonify({
            'movie_id': movie_id,
            'average_rating': round(average_rating, 2),
            'total_reviews': total_reviews
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reviews', methods=['GET'])
@cors_enabled
def obtener_todas_reviews():
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        # Obtener todas las críticas del usuario
        reviews = Review.query.filter_by(user_id=user_id).order_by(Review.created_at.desc()).all()
        
        return jsonify([{
            'id': r.id,
            'user_id': r.user_id,
            'movie_id': r.movie_id,
            'movie_title': r.movie.title,
            'rating': r.rating,
            'review_text': r.review_text,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'updated_at': r.updated_at.isoformat() if r.updated_at else None
        } for r in reviews]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reviews', methods=['POST'])
@cors_enabled
def crear_review():
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        movie_id = datos.get('movie_id')
        rating = datos.get('rating')
        review_text = datos.get('review_text', '')

        if not movie_id or rating is None:
            return jsonify({'error': 'movie_id y rating son requeridos'}), 400

        # Validar rating
        try:
            rating = int(rating)
            if rating < 1 or rating > 10:
                return jsonify({'error': 'El rating debe estar entre 1 y 10'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'El rating debe ser un número entre 1 y 10'}), 400

        # Verificar que la película existe
        movie = db.session.get(Movie, movie_id)
        if not movie:
            return jsonify({'error': 'Película no encontrada'}), 404

        # Verificar si el usuario ya tiene una crítica para esta película
        existing_review = Review.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing_review:
            return jsonify({'error': 'Ya tienes una crítica para esta película'}), 409

        # Crear la crítica
        review = Review(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating,
            review_text=review_text.strip() if review_text else None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        db.session.add(review)
        db.session.commit()

        return jsonify({
            'mensaje': 'Crítica creada exitosamente',
            'review': {
                'id': review.id,
                'user_id': review.user_id,
                'movie_id': review.movie_id,
                'rating': review.rating,
                'review_text': review.review_text,
                'created_at': review.created_at.isoformat() if review.created_at else None,
                'updated_at': review.updated_at.isoformat() if review.updated_at else None
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error en crear_review: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reviews/<int:review_id>', methods=['PUT'])
@cors_enabled
def editar_review(review_id):
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        review = db.session.get(Review, review_id)
        if not review:
            return jsonify({'error': 'Crítica no encontrada'}), 404

        # Verificar que el usuario sea el propietario de la crítica
        if review.user_id != user_id:
            return jsonify({'error': 'No tienes permiso para editar esta crítica'}), 403

        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        # Actualizar rating si se proporciona
        if 'rating' in datos:
            try:
                rating = int(datos['rating'])
                if rating < 1 or rating > 10:
                    return jsonify({'error': 'El rating debe estar entre 1 y 10'}), 400
                review.rating = rating
            except (ValueError, TypeError):
                return jsonify({'error': 'El rating debe ser un número entre 1 y 10'}), 400

        # Actualizar texto de crítica si se proporciona
        if 'review_text' in datos:
            review.review_text = datos['review_text'].strip() if datos['review_text'] else None

        review.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return jsonify({
            'mensaje': 'Crítica actualizada exitosamente',
            'review': {
                'id': review.id,
                'user_id': review.user_id,
                'movie_id': review.movie_id,
                'rating': review.rating,
                'review_text': review.review_text,
                'created_at': review.created_at.isoformat() if review.created_at else None,
                'updated_at': review.updated_at.isoformat() if review.updated_at else None
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error en editar_review: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
@cors_enabled
def eliminar_review(review_id):
    try:
        # Obtener user_id del token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except:
            return jsonify({'error': 'Token inválido'}), 401

        review = db.session.get(Review, review_id)
        if not review:
            return jsonify({'error': 'Crítica no encontrada'}), 404

        # Verificar que el usuario sea el propietario de la crítica
        if review.user_id != user_id:
            return jsonify({'error': 'No tienes permiso para eliminar esta crítica'}), 403

        db.session.delete(review)
        db.session.commit()

        return jsonify({'mensaje': 'Crítica eliminada exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error en eliminar_review: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Inicializar base de datos siempre que se cargue la aplicación
init_db()

# ==================== INICIAR SERVIDOR ====================
if __name__ == '__main__':
    print("STREAMFLIX corriendo en http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
