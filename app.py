import os
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import text

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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    favorited_by = db.relationship('Favorites', backref='movie', lazy=True)

class Favorites(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
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
                demo_user = User(
                    username='demo',
                    email='demo@example.com',
                    password_hash='$2b$12$IOWaGAooEVVOg5IjCTOIAexFY227N2fY30KVDq8sWKGPNHwcrspO.',
                    role='user'
                )
                db.session.add(demo_user)

                demo_movies = [
                    Movie(title='Inception', description='A skilled thief who steals corporate secrets through the use of dream-sharing technology.', director='Christopher Nolan', genre='Sci-Fi', release_date='2010-07-16', duration_minutes=148, rating=8.8, poster_url='https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300'),
                    Movie(title='The Matrix', description='A hacker learns about the true nature of his reality and his role in the war against its controllers.', director='The Wachowskis', genre='Sci-Fi', release_date='1999-03-31', duration_minutes=136, rating=8.7, poster_url='https://images.unsplash.com/photo-1485095329183-d0daf68471ca?w=300')
                ]
                db.session.add_all(demo_movies)
                db.session.commit()
                print("Base de datos inicial creada con datos básicos")
        else:
            print("Base de datos ya contiene datos; no es necesario sembrar de nuevo.")

        # Asegurar que el usuario demo tenga la contraseña esperada
        demo_password_hash = '$2b$12$IOWaGAooEVVOg5IjCTOIAexFY227N2fY30KVDq8sWKGPNHwcrspO.'
        demo_user = User.query.filter_by(email='demo@example.com').first()
        if demo_user and demo_user.password_hash != demo_password_hash:
            demo_user.password_hash = demo_password_hash
            db.session.commit()

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
            'video_url': p.video_url
        } for p in peliculas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:id>', methods=['GET'])
@cors_enabled
def obtener_pelicula(id):
    try:
        pelicula = Movie.query.get_or_404(id)
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
            'video_url': pelicula.video_url
        }), 200
    except Exception as e:
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
        movie = Movie.query.get(movie_id)
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

# Inicializar base de datos siempre que se cargue la aplicación
init_db()

# ==================== INICIAR SERVIDOR ====================
if __name__ == '__main__':
    print("STREAMFLIX corriendo en http://localhost:5000")
    print("Frontend disponible en http://localhost:8000")
    app.run(debug=True, host='0.0.0.0', port=5000)
