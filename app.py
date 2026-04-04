from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bcrypt import hashpw, gensalt

# ==================== CONFIGURACIÓN ====================
app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)  # Habilitar CORS para todas las rutas

# ==================== DATOS MOCK (SIN BD) ====================
peliculas_mock = [
    {"id": 1, "title": "Inception", "description": "A skilled thief who steals corporate secrets...", "genre": "Sci-Fi", "rating": 8.8, "poster_url": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300"},
    {"id": 2, "title": "The Matrix", "description": "A hacker learns about the true nature of his reality...", "genre": "Sci-Fi", "rating": 8.7, "poster_url": "https://images.unsplash.com/photo-1485095329183-d0daf68471ca?w=300"},
    {"id": 3, "title": "Interstellar", "description": "A team of explorers travel through a wormhole...", "genre": "Sci-Fi", "rating": 8.6, "poster_url": "https://images.unsplash.com/photo-1532274040911-5f82f72696c0?w=300"},
    {"id": 4, "title": "The Shawshank Redemption", "description": "Two imprisoned men bond over a number of years...", "genre": "Drama", "rating": 9.3, "poster_url": "https://images.unsplash.com/photo-1542040220-cd2b14c14a48?w=300"},
    {"id": 5, "title": "Forrest Gump", "description": "The presidencies of Kennedy and Johnson...", "genre": "Drama", "rating": 8.8, "poster_url": "https://images.unsplash.com/photo-1506399773649-6e0eb8cfb237?w=300"}
]

usuarios_mock = []
favoritos_mock = []

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
        if any(u['email'] == email for u in usuarios_mock):
            return jsonify({'error': 'El email ya está registrado'}), 409

        if any(u['username'] == username for u in usuarios_mock):
            return jsonify({'error': 'El username ya está registrado'}), 409

        # Hashear contraseña
        salt = gensalt()
        password_hash = hashpw(password.encode('utf-8'), salt)

        # Crear usuario
        usuario = {
            'id': len(usuarios_mock) + 1,
            'username': username,
            'email': email,
            'password_hash': password_hash.decode('utf-8'),
            'role': 'user'
        }
        usuarios_mock.append(usuario)

        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': {
                'id': usuario['id'],
                'username': usuario['username'],
                'email': usuario['email'],
                'role': usuario['role']
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- API: LOGIN ---
@app.route('/api/login', methods=['POST'])
def login():
    try:
        datos = request.get_json()
        if not datos or not datos.get('email') or not datos.get('password'):
            return jsonify({'error': 'Email y contraseña requeridos'}), 400

        email = datos['email']
        password = datos['password']

        # Buscar usuario
        usuario = next((u for u in usuarios_mock if u['email'] == email), None)
        if not usuario:
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401

        # Verificar contraseña
        if not hashpw(password.encode('utf-8'), usuario['password_hash'].encode('utf-8')):
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401

        # Generar token simple (no JWT por simplicidad)
        token = f"token_{usuario['id']}_{usuario['username']}"

        return jsonify({
            'token': token,
            'usuario': {
                'id': usuario['id'],
                'username': usuario['username'],
                'email': usuario['email'],
                'role': usuario['role']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- API: PELÍCULAS ---
@app.route('/api/peliculas', methods=['GET'])
def obtener_peliculas():
    return jsonify(peliculas_mock), 200

@app.route('/api/peliculas/<int:id>', methods=['GET'])
def obtener_pelicula(id):
    pelicula = next((p for p in peliculas_mock if p['id'] == id), None)
    if not pelicula:
        return jsonify({'error': 'Película no encontrada'}), 404
    return jsonify(pelicula), 200

# --- API: FAVORITOS ---
@app.route('/api/favoritos', methods=['GET'])
def obtener_favoritos():
    # Simular que el usuario 1 está logueado
    user_id = 1
    favoritos_usuario = [p for p in peliculas_mock if p['id'] in [f['movie_id'] for f in favoritos_mock if f['user_id'] == user_id]]
    return jsonify(favoritos_usuario), 200

@app.route('/api/favoritos', methods=['POST'])
def agregar_favorito():
    try:
        datos = request.get_json()
        movie_id = datos.get('movie_id')
        if not movie_id:
            return jsonify({'error': 'movie_id es requerido'}), 400

        # Verificar que la película existe
        if not any(p['id'] == movie_id for p in peliculas_mock):
            return jsonify({'error': 'Película no encontrada'}), 404

        # Simular usuario logueado
        user_id = 1

        # Verificar que no esté ya en favoritos
        if any(f['user_id'] == user_id and f['movie_id'] == movie_id for f in favoritos_mock):
            return jsonify({'error': 'La película ya está en favoritos'}), 409

        favorito = {'user_id': user_id, 'movie_id': movie_id}
        favoritos_mock.append(favorito)

        return jsonify({'mensaje': 'Película agregada a favoritos'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== INICIAR SERVIDOR ====================
if __name__ == '__main__':
    print("🚀 STREAMFLIX corriendo en http://localhost:5000")
    print("📱 Frontend disponible en http://localhost:8000")
    app.run(debug=True, port=5000)
def token_required(f):
    """Decorador para verificar token JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token faltante'}), 401
        
        try:
            token = token.split(' ')[1]  # Remover "Bearer "
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'Usuario no encontrado'}), 401
        except:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    """Decorador para verificar rol de admin"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'error': 'Acceso denegado. Solo administradores'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# ==================== RUTAS: AUTENTICACIÓN ====================
@app.route('/api/registro', methods=['POST'])
def registro():
    """Registrar nuevo usuario"""
    try:
        datos = request.get_json()
        
        if not datos or not datos.get('email') or not datos.get('password') or not datos.get('username'):
            return jsonify({'error': 'Email, username y contraseña son requeridos'}), 400
        
        if User.query.filter_by(email=datos['email']).first():
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        if User.query.filter_by(username=datos['username']).first():
            return jsonify({'error': 'El username ya está registrado'}), 409
        
        usuario = User(
            username=datos['username'],
            email=datos['email']
        )
        usuario.set_password(datos['password'])
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': usuario.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Iniciar sesión y obtener token JWT"""
    try:
        datos = request.get_json()
        
        if not datos or not datos.get('email') or not datos.get('password'):
            return jsonify({'error': 'Email y contraseña requeridos'}), 400
        
        usuario = User.query.filter_by(email=datos['email']).first()
        
        if not usuario or not usuario.verify_password(datos['password']):
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401
        
        token = jwt.encode({
            'user_id': usuario.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token,
            'usuario': usuario.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS: PELÍCULAS (CRUD) ====================
@app.route('/api/peliculas', methods=['GET'])
def obtener_peliculas():
    """Obtener todas las películas"""
    try:
        peliculas = Movie.query.all()
        return jsonify([pelicula.to_dict() for pelicula in peliculas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:id>', methods=['GET'])
def obtener_pelicula(id):
    """Obtener una película por ID"""
    try:
        pelicula = Movie.query.get(id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404
        return jsonify(pelicula.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas', methods=['POST'])
@token_required
@admin_required
def crear_pelicula(current_user):
    """Crear una nueva película (solo admin)"""
    try:
        datos = request.get_json()
        
        if not datos or not datos.get('title'):
            return jsonify({'error': 'El título es requerido'}), 400
        
        pelicula = Movie(
            title=datos['title'],
            description=datos.get('description'),
            director=datos.get('director'),
            genre=datos.get('genre'),
            release_date=datos.get('release_date'),
            duration_minutes=datos.get('duration_minutes'),
            rating=datos.get('rating'),
            poster_url=datos.get('poster_url'),
            video_url=datos.get('video_url')
        )
        
        db.session.add(pelicula)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Película creada exitosamente',
            'pelicula': pelicula.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:id>', methods=['PUT'])
@token_required
@admin_required
def actualizar_pelicula(current_user, id):
    """Actualizar una película (solo admin)"""
    try:
        pelicula = Movie.query.get(id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404
        
        datos = request.get_json()
        
        if 'title' in datos:
            pelicula.title = datos['title']
        if 'description' in datos:
            pelicula.description = datos['description']
        if 'director' in datos:
            pelicula.director = datos['director']
        if 'genre' in datos:
            pelicula.genre = datos['genre']
        if 'release_date' in datos:
            pelicula.release_date = datos['release_date']
        if 'duration_minutes' in datos:
            pelicula.duration_minutes = datos['duration_minutes']
        if 'rating' in datos:
            pelicula.rating = datos['rating']
        if 'poster_url' in datos:
            pelicula.poster_url = datos['poster_url']
        if 'video_url' in datos:
            pelicula.video_url = datos['video_url']
        
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Película actualizada exitosamente',
            'pelicula': pelicula.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def eliminar_pelicula(current_user, id):
    """Eliminar una película (solo admin)"""
    try:
        pelicula = Movie.query.get(id)
        if not pelicula:
            return jsonify({'error': 'Película no encontrada'}), 404
        
        db.session.delete(pelicula)
        db.session.commit()
        
        return jsonify({'mensaje': 'Película eliminada exitosamente'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS: FAVORITOS ====================
@app.route('/api/favoritos', methods=['POST'])
@token_required
def agregar_favorito(current_user):
    """Agregar película a favoritos"""
    try:
        datos = request.get_json()
        movie_id = datos.get('movie_id')
        
        if not movie_id:
            return jsonify({'error': 'movie_id es requerido'}), 400
        
        if not Movie.query.get(movie_id):
            return jsonify({'error': 'Película no encontrada'}), 404
        
        favorito = Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if favorito:
            return jsonify({'error': 'La película ya está en favoritos'}), 409
        
        favorito = Favorite(user_id=current_user.id, movie_id=movie_id)
        db.session.add(favorito)
        db.session.commit()
        
        return jsonify({'mensaje': 'Película agregada a favoritos'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/favoritos', methods=['GET'])
@token_required
def obtener_favoritos(current_user):
    """Obtener mis películas favoritas"""
    try:
        favoritos = Favorite.query.filter_by(user_id=current_user.id).all()
        movies = [Movie.query.get(fav.movie_id).to_dict() for fav in favoritos]
        return jsonify(movies), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/favoritos/<int:movie_id>', methods=['DELETE'])
@token_required
def eliminar_favorito(current_user, movie_id):
    """Eliminar película de favoritos"""
    try:
        favorito = Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if not favorito:
            return jsonify({'error': 'Favorito no encontrado'}), 404
        
        db.session.delete(favorito)
        db.session.commit()
        
        return jsonify({'mensaje': 'Película eliminada de favoritos'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== INICIAR SERVIDOR ====================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    app.run(debug=True)
#"""

from flask import Flask, request, jsonify, send_from_directory
from bcrypt import hashpw, gensalt

# static_folder='.' le dice a Flask que puede servir el index.html y app.js de esta misma carpeta
app = Flask(__name__, static_url_path='', static_folder='.')

# --- RUTA PARA EL FRONTEND ---
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# --- RUTA DE PRUEBA 3: API DE PELÍCULAS (MOCK DATA) ---
@app.route('/api/peliculas', methods=['GET'])
def obtener_peliculas():
    # Simulamos lo que devolvería la base de datos
    peliculas_falsas = [
        {"titulo": "El Señor de los Anillos", "año": 2001, "genero": "Fantasía", "descripcion": "Un anillo para gobernarlos a todos."},
        {"titulo": "Matrix", "año": 1999, "genero": "Ciencia Ficción", "descripcion": "Pastilla azul o pastilla roja."},
        {"titulo": "Ocho apellidos vascos", "año": 2014, "genero": "Comedia", "descripcion": "Un sevillano viaja a Euskadi."}
    ]
    return jsonify(peliculas_falsas)

# --- RUTA DE PRUEBA 2: EL CÓDIGO DE COPILOT ---
@app.route('/api/registro', methods=['POST'])
def registro():
    try:
        datos = request.get_json()
        if not datos: return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        email = datos.get('email')
        password = datos.get('password')
        if not email or not password: return jsonify({'error': 'Email y contraseña requeridos'}), 400
        
        salt = gensalt()
        password_hash = hashpw(password.encode('utf-8'), salt)
        
        # Devuelvo el hash en el JSON solo para que VEAS que funciona visualmente en la prueba
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'email': email,
            'hash_generado_por_bcrypt': password_hash.decode('utf-8')
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
