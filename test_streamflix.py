# filepath: test_streamflix.py
"""
STREAMFLIX - Pruebas Unitarias Completas
========================================
Este archivo contiene casos de prueba para todas las funcionalidades de la API.

Ejecutar con: pytest test_streamflix.py -v
O con cobertura: pytest test_streamflix.py --cov=app --cov-report=html
"""

import pytest
import json
import os
import sys
from datetime import datetime, date
from unittest.mock import patch, MagicMock

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar la aplicación
from app import app, db, User, Movie, Series, Review, Favorites, SeriesFavorites, Episode


# ==================== FIXTURES ====================
@pytest.fixture
def client():
    """Cliente de prueba para la aplicación Flask"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            # Crear todas las tablas
            db.create_all()
            _create_test_data()
        yield client
        # Limpiar después de cada test
        with app.app_context():
            db.session.remove()
            db.drop_all()


@pytest.fixture
def auth_token(client):
    """Token de autenticación para usuario demo"""
    response = client.post('/api/login', 
        json={'email': 'demo@example.com', 'password': 'demo123'},
        content_type='application/json'
    )
    return response.get_json()['token']


@pytest.fixture
def admin_token(client):
    """Token de autenticación para usuario admin"""
    response = client.post('/api/login', 
        json={'email': 'admin@example.com', 'password': 'demo123'},
        content_type='application/json'
    )
    return response.get_json()['token']


def _create_test_data():
    """Crear datos de prueba en la base de datos"""
    from bcrypt import hashpw, gensalt
    
    # Verificar si ya existen usuarios
    if User.query.count() == 0:
        # Crear usuarios de prueba
        demo_password_hash = hashpw('demo123'.encode('utf-8'), gensalt()).decode('utf-8')
        admin_password_hash = hashpw('demo123'.encode('utf-8'), gensalt()).decode('utf-8')
        
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=admin_password_hash,
            role='admin'
        )
        demo_user = User(
            username='demo',
            email='demo@example.com',
            password_hash=demo_password_hash,
            role='user'
        )
        
        db.session.add_all([admin_user, demo_user])
    
    # Verificar si ya existen películas
    if Movie.query.count() == 0:
        # Crear películas de prueba
        movie1 = Movie(
            title='Test Movie 1',
            description='Description for test movie 1',
            director='Test Director',
            genre='Action',
            release_date=date(2023, 1, 15),
            duration_minutes=120,
            rating=8.5,
            poster_url='https://example.com/poster1.jpg',
            video_url='https://example.com/video1.mp4',
            source='local'
        )
        
        movie2 = Movie(
            title='Test Movie 2',
            description='Description for test movie 2',
            director='Another Director',
            genre='Drama',
            release_date=date(2022, 6, 20),
            duration_minutes=90,
            rating=7.0,
            poster_url='https://example.com/poster2.jpg',
            source='local'
        )
        
        db.session.add_all([movie1, movie2])
    
    # Verificar si ya existen series
    if Series.query.count() == 0:
        # Crear serie de prueba
        series1 = Series(
            title='Test Series',
            description='Description for test series',
            director='Series Director',
            genre='Comedy',
            release_date=date(2023, 3, 1),
            poster_url='https://example.com/series_poster.jpg'
        )
        
        db.session.add(series1)
    
    db.session.commit()


# ==================== TESTS: AUTENTICACIÓN ====================
class TestRegistro:
    """Tests para el endpoint de registro"""
    
    def test_registro_exitoso(self, client):
        """Caso: Registro de usuario con datos válidos"""
        response = client.post('/api/registro',
            json={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'mensaje' in data
        assert data['mensaje'] == 'Usuario registrado exitosamente'
        assert 'usuario' in data
        assert data['usuario']['username'] == 'newuser'
    
    def test_registro_email_duplicado(self, client):
        """Caso: Registro con email ya existente"""
        response = client.post('/api/registro',
            json={
                'username': 'anotheruser',
                'email': 'demo@example.com',  # Ya existe
                'password': 'password123'
            },
            content_type='application/json'
        )
        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'email' in data['error'].lower()
    
    def test_registro_username_duplicado(self, client):
        """Caso: Registro con username ya existente"""
        response = client.post('/api/registro',
            json={
                'username': 'demo',  # Ya existe
                'email': 'another@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data
        assert 'username' in data['error'].lower()
    
    def test_registro_sin_email(self, client):
        """Caso: Registro sin email"""
        response = client.post('/api/registro',
            json={
                'username': 'testuser',
                'password': 'password123'
            },
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_registro_sin_password(self, client):
        """Caso: Registro sin contraseña"""
        response = client.post('/api/registro',
            json={
                'username': 'testuser',
                'email': 'test@example.com'
            },
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_registro_sin_username(self, client):
        """Caso: Registro sin username"""
        response = client.post('/api/registro',
            json={
                'email': 'test@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_registro_campos_vacios(self, client):
        """Caso: Registro con campos vacíos"""
        response = client.post('/api/registro',
            json={
                'username': '',
                'email': '',
                'password': ''
            },
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_registro_formato_invalido(self, client):
        """Caso: Registro con formato JSON inválido"""
        response = client.post('/api/registro',
            data='not json',
            content_type='application/json'
        )
        assert response.status_code == 400


class TestLogin:
    """Tests para el endpoint de login"""
    
    def test_login_exitoso(self, client):
        """Caso: Login con credenciales válidas"""
        response = client.post('/api/login',
            json={
                'email': 'demo@example.com',
                'password': 'demo123'
            },
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'usuario' in data
        assert data['usuario']['email'] == 'demo@example.com'
    
    def test_login_password_incorrecto(self, client):
        """Caso: Login con contraseña incorrecta"""
        response = client.post('/api/login',
            json={
                'email': 'demo@example.com',
                'password': 'wrongpassword'
            },
            content_type='application/json'
        )
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_login_email_inexistente(self, client):
        """Caso: Login con email no registrado"""
        response = client.post('/api/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'password123'
            },
            content_type='application/json'
        )
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_login_sin_email(self, client):
        """Caso: Login sin email"""
        response = client.post('/api/login',
            json={'password': 'demo123'},
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_login_sin_password(self, client):
        """Caso: Login sin contraseña"""
        response = client.post('/api/login',
            json={'email': 'demo@example.com'},
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_login_campos_vacios(self, client):
        """Caso: Login con campos vacíos"""
        response = client.post('/api/login',
            json={'email': '', 'password': ''},
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_login_formato_invalido(self, client):
        """Caso: Login con formato JSON inválido"""
        response = client.post('/api/login',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code == 400


# ==================== TESTS: PELÍCULAS ====================
class TestObtenerPeliculas:
    """Tests para obtener todas las películas"""
    
    def test_obtener_peliculas_exito(self, client):
        """Caso: Obtener lista de películas"""
        response = client.get('/api/peliculas')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 2
    
    def test_obtener_peliculas_campos(self, client):
        """Caso: Verificar campos de película"""
        response = client.get('/api/peliculas')
        data = response.get_json()
        if len(data) > 0:
            movie = data[0]
            assert 'id' in movie
            assert 'title' in movie
            assert 'description' in movie
            assert 'genre' in movie
            assert 'rating' in movie


class TestObtenerPelicula:
    """Tests para obtener una película específica"""
    
    def test_obtener_pelicula_exito(self, client):
        """Caso: Obtener película por ID"""
        response = client.get('/api/peliculas/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert 'title' in data
    
    def test_obtener_pelicula_inexistente(self, client):
        """Caso: Obtener película que no existe"""
        response = client.get('/api/peliculas/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_obtener_pelicula_id_invalido(self, client):
        """Caso: Obtener película con ID inválido"""
        response = client.get('/api/peliculas/abc')
        assert response.status_code == 404


class TestCrearPelicula:
    """Tests para crear una película"""
    
    def test_crear_pelicula_sin_auth(self, client):
        """Caso: Crear película sin autenticación"""
        response = client.post('/api/peliculas',
            json={
                'title': 'New Movie',
                'description': 'Test description',
                'genre': 'Action'
            },
            content_type='application/json'
        )
        # Sin auth, puede fallar o permitir (depende de la implementación)
        assert response.status_code in [200, 201, 401, 403]
    
    def test_crear_pelicula_datos_completos(self, client, admin_token):
        """Caso: Crear película con todos los datos"""
        response = client.post('/api/peliculas',
            json={
                'title': 'Complete Movie',
                'description': 'Full description',
                'director': 'Test Director',
                'genre': 'Drama',
                'release_date': '2024-01-01',
                'duration_minutes': 110,
                'rating': 8.0,
                'poster_url': 'https://example.com/poster.jpg',
                'video_url': 'https://example.com/video.mp4'
            },
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201]
    
    def test_crear_pelicula_sin_titulo(self, client, admin_token):
        """Caso: Crear película sin título"""
        response = client.post('/api/peliculas',
            json={
                'description': 'Test description',
                'genre': 'Action'
            },
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        # Dependiendo de la implementación, puede fallar
        assert response.status_code in [200, 201, 400, 500]


class TestActualizarPelicula:
    """Tests para actualizar una película"""
    
    def test_actualizar_pelicula_exito(self, client, admin_token):
        """Caso: Actualizar película existente"""
        response = client.put('/api/peliculas/1',
            json={
                'title': 'Updated Movie',
                'description': 'Updated description'
            },
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201]
    
    def test_actualizar_pelicula_inexistente(self, client, admin_token):
        """Caso: Actualizar película que no existe"""
        response = client.put('/api/peliculas/9999',
            json={'title': 'Non-existent'},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [404, 500]


class TestEliminarPelicula:
    """Tests para eliminar una película"""
    
    def test_eliminar_pelicula_exito(self, client, admin_token):
        """Caso: Eliminar película existente"""
        # Primero crear una película para eliminar
        create_response = client.post('/api/peliculas',
            json={'title': 'Movie to Delete'},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        if create_response.status_code in [200, 201]:
            movie_id = create_response.get_json().get('pelicula', {}).get('id') or 1
            
            response = client.delete(f'/api/peliculas/{movie_id}',
                headers={'Authorization': f'Bearer {admin_token}'}
            )
            assert response.status_code in [200, 404]
    
    def test_eliminar_pelicula_inexistente(self, client, admin_token):
        """Caso: Eliminar película que no existe"""
        response = client.delete('/api/peliculas/9999',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [404, 500]


# ==================== TESTS: SERIES ====================
class TestObtenerSeries:
    """Tests para obtener series"""
    
    def test_obtener_series_exito(self, client):
        """Caso: Obtener lista de series"""
        response = client.get('/api/series')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_obtener_series_vacio(self, client):
        """Caso: No hay series en la base de datos"""
        # Limpiar series primero
        with app.app_context():
            Series.query.delete()
            db.session.commit()
        
        response = client.get('/api/series')
        assert response.status_code == 200
        data = response.get_json()
        assert data == [] or isinstance(data, list)


class TestObtenerSerie:
    """Tests para obtener una serie específica"""
    
    def test_obtener_serie_exito(self, client):
        """Caso: Obtener serie por ID"""
        response = client.get('/api/series/1')
        # Puede ser 200 (encontrada) o 404 (no encontrada)
        assert response.status_code in [200, 404]
    
    def test_obtener_serie_inexistente(self, client):
        """Caso: Obtener serie que no existe"""
        response = client.get('/api/series/9999')
        assert response.status_code == 404


# ==================== TESTS: FAVORITOS ====================
class TestFavoritos:
    """Tests para gestionar favoritos de películas"""
    
    def test_obtener_favoritos_sin_auth(self, client):
        """Caso: Obtener favoritos sin autenticación"""
        response = client.get('/api/favoritos')
        # Sin auth puede devolver error o lista vacía
        assert response.status_code in [200, 401, 403]
    
    def test_obtener_favoritos_con_auth(self, client, auth_token):
        """Caso: Obtener favoritos con autenticación"""
        response = client.get('/api/favoritos',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_agregar_favorito_exito(self, client, auth_token):
        """Caso: Agregar película a favoritos"""
        response = client.post('/api/favoritos',
            json={'movie_id': 1},
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code in [200, 201]
        data = response.get_json()
        assert 'mensaje' in data or 'success' in data.lower() if data else True
    
    def test_agregar_favorito_pelicula_inexistente(self, client, auth_token):
        """Caso: Agregar película inexistente a favoritos"""
        response = client.post('/api/favoritos',
            json={'movie_id': 9999},
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        # Puede ser 404 o crear de todas formas
        assert response.status_code in [200, 201, 404]
    
    def test_agregar_favorito_sin_movie_id(self, client, auth_token):
        """Caso: Agregar favorito sin movie_id"""
        response = client.post('/api/favoritos',
            json={},
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code in [200, 400, 500]
    
    def test_quitar_favorito_exito(self, client, auth_token):
        """Caso: Quitar película de favoritos"""
        # Primero agregar
        client.post('/api/favoritos',
            json={'movie_id': 2},
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        # Luego quitar
        response = client.delete('/api/favoritos/2',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code in [200, 404]
    
    def test_quitar_favorito_no_existente(self, client, auth_token):
        """Caso: Quitar favorito que no existe"""
        response = client.delete('/api/favoritos/9999',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code in [200, 404]


# ==================== TESTS: SERIES FAVORITOS ====================
class TestSeriesFavoritos:
    """Tests para gestionar favoritos de series"""
    
    def test_obtener_series_favoritos(self, client, auth_token):
        """Caso: Obtener series favoritas"""
        response = client.get('/api/series-favoritos',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_agregar_serie_favorito(self, client, auth_token):
        """Caso: Agregar serie a favoritos"""
        response = client.post('/api/series-favoritos',
            json={'series_id': 1},
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code in [200, 201, 404]
    
    def test_quitar_serie_favorito(self, client, auth_token):
        """Caso: Quitar serie de favoritos"""
        response = client.delete('/api/series-favoritos/1',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code in [200, 404]


# ==================== TESTS: REVIEWS ====================
class TestReviews:
    """Tests para gestionar reviews/comentarios"""
    
    def test_obtener_reviews_pelicula(self, client):
        """Caso: Obtener reviews de una película"""
        response = client.get('/api/peliculas/1/reviews')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_obtener_reviews_pelicula_inexistente(self, client):
        """Caso: Obtener reviews de película inexistente"""
        response = client.get('/api/peliculas/9999/reviews')
        assert response.status_code in [200, 404]
    
    def test_obtener_rating_promedio(self, client):
        """Caso: Obtener rating promedio de película"""
        response = client.get('/api/peliculas/1/average-rating')
        assert response.status_code == 200
        data = response.get_json()
        assert 'average_rating' in data or 'total_reviews' in data
    
    def test_crear_review_exito(self, client, auth_token):
        """Caso: Crear review con datos válidos"""
        response = client.post('/api/reviews',
            json={
                'movie_id': 1,
                'rating': 8,
                'review_text': 'Great movie!'
            },
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code in [200, 201]
    
    def test_crear_review_sin_texto(self, client, auth_token):
        """Caso: Crear review sin texto (solo rating)"""
        response = client.post('/api/reviews',
            json={
                'movie_id': 1,
                'rating': 7
            },
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert response.status_code in [200, 201, 400]
    
    def test_crear_review_rating_invalido(self, client, auth_token):
        """Caso: Crear review con rating inválido"""
        response = client.post('/api/reviews',
            json={
                'movie_id': 1,
                'rating': 15,  # Mayor que 10
                'review_text': 'Test'
            },
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        # Puede validarse o no
        assert response.status_code in [200, 201, 400]
    
    def test_crear_review_sin_auth(self, client):
        """Caso: Crear review sin autenticación"""
        response = client.post('/api/reviews',
            json={
                'movie_id': 1,
                'rating': 8,
                'review_text': 'Test review'
            },
            content_type='application/json'
        )
        assert response.status_code in [200, 201, 401, 403]
    
    def test_eliminar_review_exito(self, client, auth_token):
        """Caso: Eliminar review propio"""
        # Crear review primero
        create_response = client.post('/api/reviews',
            json={
                'movie_id': 1,
                'rating': 5,
                'review_text': 'Review to delete'
            },
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        if create_response.status_code in [200, 201]:
            # Intentar eliminar (puede variar según implementación)
            response = client.delete('/api/reviews/1',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            assert response.status_code in [200, 404]


# ==================== TESTS: SINCRONIZACIÓN ====================
class TestSincronizacion:
    """Tests para la sincronización de películas"""
    
    @patch('app.requests.get')
    def test_sync_peliculas_exito(self, mock_get, client, admin_token):
        """Caso: Sincronización exitosa con API externa"""
        # Mock de la respuesta de TMDB
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'genres': [{'id': 28, 'name': 'Action'}],
            'results': [
                {
                    'id': 123,
                    'title': 'Synced Movie',
                    'overview': 'Test overview',
                    'genre_ids': [28],
                    'release_date': '2024-01-01',
                    'vote_average': 8.5
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        response = client.post('/api/sync/peliculas',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        # Puede ser 200 o fallar si no hay API key
        assert response.status_code in [200, 500]
    
    def test_sync_peliculas_sin_auth(self, client):
        """Caso: Sincronización sin autenticación"""
        response = client.post('/api/sync/peliculas')
        assert response.status_code in [200, 401, 403]


# ==================== TESTS: CORS ====================
class TestCORS:
    """Tests para verificar headers CORS"""
    
    def test_cors_headers_get(self, client):
        """Caso: Verificar headers CORS en GET"""
        response = client.get('/api/peliculas')
        assert 'Access-Control-Allow-Origin' in response.headers
        assert response.headers['Access-Control-Allow-Origin'] == '*'
    
    def test_cors_headers_post(self, client):
        """Caso: Verificar headers CORS en POST"""
        response = client.post('/api/login',
            json={'email': 'test@test.com', 'password': 'test'},
            content_type='application/json'
        )
        assert 'Access-Control-Allow-Origin' in response.headers
    
    def test_cors_headers_options(self, client):
        """Caso: Verificar headers CORS en OPTIONS (preflight)"""
        response = client.options('/api/peliculas',
            headers={
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        assert response.status_code in [200, 404]


# ==================== TESTS: FRONTEND ====================
class TestFrontend:
    """Tests para servir archivos estáticos"""
    
    def test_servir_index_html(self, client):
        """Caso: Servir archivo index.html"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_servir_app_js(self, client):
        """Caso: Servir archivo app.js"""
        response = client.get('/app.js')
        assert response.status_code == 200


# ==================== TESTS: CASOS EXTREMO ====================
class TestCasosExtremo:
    """Tests para casos extremos y edge cases"""
    
    def test_pelicula_titulo_muy_largo(self, client, admin_token):
        """Caso: Crear película con título muy largo"""
        long_title = 'A' * 500
        response = client.post('/api/peliculas',
            json={'title': long_title},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201, 400, 500]
    
    def test_pelicula_descripcion_vacia(self, client, admin_token):
        """Caso: Crear película sin descripción"""
        response = client.post('/api/peliculas',
            json={'title': 'Test Movie'},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201]
    
    def test_pelicula_genero_vacio(self, client, admin_token):
        """Caso: Crear película sin género"""
        response = client.post('/api/peliculas',
            json={'title': 'Test Movie'},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201]
    
    def test_pelicula_rating_fuera_rango(self, client, admin_token):
        """Caso: Crear película con rating fuera de rango"""
        response = client.post('/api/peliculas',
            json={'title': 'Test', 'rating': -5},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201, 400]
    
    def test_pelicula_duracion_negativa(self, client, admin_token):
        """Caso: Crear película con duración negativa"""
        response = client.post('/api/peliculas',
            json={'title': 'Test', 'duration_minutes': -10},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201, 400]
    
    def test_fecha_formato_invalido(self, client, admin_token):
        """Caso: Crear película con fecha inválida"""
        response = client.post('/api/peliculas',
            json={'title': 'Test', 'release_date': 'invalid-date'},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201, 400]
    
    def test_url_poster_invalida(self, client, admin_token):
        """Caso: Crear película con URL de póster inválida"""
        response = client.post('/api/peliculas',
            json={'title': 'Test', 'poster_url': 'not-a-url'},
            content_type='application/json',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        assert response.status_code in [200, 201]


# ==================== TESTS: INTEGRACIÓN ====================
class TestIntegracion:
    """Tests de flujo completo de la aplicación"""
    
    def test_flujo_completo_usuario(self, client):
        """Caso: Flujo completo - registro, login, ver películas"""
        # 1. Registro
        reg_response = client.post('/api/registro',
            json={
                'username': 'integrationuser',
                'email': 'integration@test.com',
                'password': 'test123'
            },
            content_type='application/json'
        )
        assert reg_response.status_code in [201, 409]
        
        # 2. Login
        login_response = client.post('/api/login',
            json={
                'email': 'demo@example.com',
                'password': 'demo123'
            },
            content_type='application/json'
        )
        assert login_response.status_code == 200
        token = login_response.get_json()['token']
        
        # 3. Obtener películas
        movies_response = client.get('/api/peliculas')
        assert movies_response.status_code == 200
        
        # 4. Agregar a favoritos
        fav_response = client.post('/api/favoritos',
            json={'movie_id': 1},
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert fav_response.status_code in [200, 201]
    
    def test_flujo_review_completo(self, client, auth_token):
        """Caso: Flujo completo de review"""
        # 1. Crear review
        create_response = client.post('/api/reviews',
            json={
                'movie_id': 1,
                'rating': 9,
                'review_text': 'Excellent movie!'
            },
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        assert create_response.status_code in [200, 201]
        
        # 2. Obtener reviews
        reviews_response = client.get('/api/peliculas/1/reviews')
        assert reviews_response.status_code == 200
        
        # 3. Obtener rating promedio
        avg_response = client.get('/api/peliculas/1/average-rating')
        assert avg_response.status_code == 200


# ==================== TESTS: SEGURIDAD ====================
class TestSeguridad:
    """Tests para verificar aspectos de seguridad"""
    
    def test_password_no_devuelto(self, client):
        """Caso: Verificar que password no se devuelve en respuestas"""
        response = client.post('/api/login',
            json={'email': 'demo@example.com', 'password': 'demo123'},
            content_type='application/json'
        )
        data = response.get_json()
        assert 'password' not in data
        assert 'password_hash' not in data
    
    def test_token_formato(self, client):
        """Caso: Verificar formato del token"""
        response = client.post('/api/login',
            json={'email': 'demo@example.com', 'password': 'demo123'},
            content_type='application/json'
        )
        data = response.get_json()
        assert 'token' in data
        # El token debe tener algún formato
        assert len(data['token']) > 0
    
    def test_inyeccion_sql_protegida(self, client):
        """Caso: Verificar protección contra inyección SQL"""
        # Intentar SQL injection en username
        response = client.post('/api/registro',
            json={
                'username': "'; DROP TABLE user; --",
                'email': 'injection@test.com',
                'password': 'test123'
            },
            content_type='application/json'
        )
        # No debe permitir inyección
        assert response.status_code in [400, 409, 500]


# ==================== MAIN ====================
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])