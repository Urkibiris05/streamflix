import os
import unicodedata
import requests
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import text, or_
from datetime import datetime, timezone

# ==================== CONFIGURACIÓN ====================
basedir = os.path.abspath(os.path.dirname(__file__))


def _load_env_file(env_path):
    if not os.path.exists(env_path):
        return

    with open(env_path, 'r', encoding='utf-8') as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue

            if line.startswith('export '):
                line = line[len('export '):].strip()

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Soporta comentarios inline: KEY=value # comentario
            if value and value[0] not in ('"', "'") and ' #' in value:
                value = value.split(' #', 1)[0].strip()

            value = value.strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


_load_env_file(os.path.join(basedir, '.env'))
app = Flask(__name__, static_url_path='', static_folder='.')
app.config['SECRET_KEY'] = 'tu_clave_secreta'

# Configuración de base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'streamflix.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==================== CONFIGURACIÓN DE SINCRONIZACIÓN EXTERNA ====================
MOVIES_PROVIDER_SOURCE = os.getenv('MOVIES_PROVIDER_SOURCE', 'tmdb')
TMDB_BASE_URL = os.getenv('TMDB_BASE_URL', 'https://api.themoviedb.org/3')
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
TMDB_LANGUAGE = os.getenv('TMDB_LANGUAGE', 'es-ES')
TMDB_MAX_PAGES = int(os.getenv('TMDB_MAX_PAGES', '3'))
TMDB_IMAGE_BASE_URL = os.getenv('TMDB_IMAGE_BASE_URL', 'https://image.tmdb.org/t/p/w500')
OMDB_PROVIDER_URL = os.getenv('OMDB_PROVIDER_URL', 'https://www.omdbapi.com/')
OMDB_API_KEY = os.getenv('OMDB_API_KEY', 'thewdb')
OMDB_RECENT_YEARS = int(os.getenv('OMDB_RECENT_YEARS', '3'))
OMDB_MAX_PAGES_PER_QUERY = int(os.getenv('OMDB_MAX_PAGES_PER_QUERY', '2'))
OMDB_MAX_TITLES = int(os.getenv('OMDB_MAX_TITLES', '120'))
GHIBLI_PROVIDER_URL = os.getenv('GHIBLI_PROVIDER_URL', 'https://ghibliapi.vercel.app/films')
MOVIES_PROVIDER_TIMEOUT_SECONDS = int(os.getenv('MOVIES_PROVIDER_TIMEOUT_SECONDS', '8'))
MOVIES_SYNC_INTERVAL_MINUTES = int(os.getenv('MOVIES_SYNC_INTERVAL_MINUTES', '60'))
MOVIES_SYNC_MAX_PAGES = int(os.getenv('MOVIES_SYNC_MAX_PAGES', '2'))
MOVIES_SYNC_PAGE_LIMIT = int(os.getenv('MOVIES_SYNC_PAGE_LIMIT', '50'))
MOVIES_AUTO_SYNC_ON_READ = os.getenv('MOVIES_AUTO_SYNC_ON_READ', 'true').lower() == 'true'

TITLE_ALIASES = {
    'spirited away': 'spirited away',
    'el viaje de chihiro': 'spirited away',
    'sen to chihiro no kamikakushi': 'spirited away',
}

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
    external_id = db.Column(db.String(120), nullable=True)
    source = db.Column(db.String(50), default='local')
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    favorited_by = db.relationship('Favorites', backref='movie', lazy=True)

class Favorites(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class SyncState(db.Model):
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


def _now_utc():
    return datetime.now(timezone.utc)


def _normalize_title_key(title):
    if not title:
        return ''

    text_value = title.strip().lower()
    text_value = ''.join(
        c for c in unicodedata.normalize('NFKD', text_value)
        if not unicodedata.combining(c)
    )
    return ' '.join(text_value.split())


def _canonical_title_key(title):
    normalized = _normalize_title_key(title)
    return TITLE_ALIASES.get(normalized, normalized)


def _movie_data_score(movie):
    fields = [
        movie.description,
        movie.director,
        movie.genre,
        movie.poster_url,
        movie.video_url,
        movie.rating,
        movie.duration_minutes,
        movie.external_id,
    ]
    return sum(1 for value in fields if value not in (None, ''))


def ensure_schema_compatibility():
    """Agregar columnas/índices faltantes en instalaciones existentes sin migraciones formales."""
    with db.engine.begin() as conn:
        movie_columns = {row[1] for row in conn.execute(text('PRAGMA table_info(movie)')).fetchall()}

        if 'external_id' not in movie_columns:
            conn.execute(text('ALTER TABLE movie ADD COLUMN external_id VARCHAR(120)'))
        if 'source' not in movie_columns:
            conn.execute(text("ALTER TABLE movie ADD COLUMN source VARCHAR(50) DEFAULT 'local'"))

        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_movie_source_external_id ON movie (source, external_id)"))


def _get_sync_state(key):
    return db.session.get(SyncState, key)


def _set_sync_state(key, value):
    state = _get_sync_state(key)
    if state:
        state.value = value
        state.updated_at = _now_utc()
    else:
        db.session.add(SyncState(key=key, value=value, updated_at=_now_utc()))


def purge_non_tmdb_movies():
    """Eliminar películas y favoritos que no provengan de TMDB."""
    movies_to_delete = Movie.query.filter(
        or_(
            Movie.source != 'tmdb',
            Movie.source.is_(None),
            Movie.source == '',
        )
    ).all()
    if not movies_to_delete:
        return 0

    movie_ids = [movie.id for movie in movies_to_delete]
    Favorites.query.filter(Favorites.movie_id.in_(movie_ids)).delete(synchronize_session=False)
    Movie.query.filter(Movie.id.in_(movie_ids)).delete(synchronize_session=False)
    db.session.commit()
    return len(movie_ids)


def _bootstrap_default_users():
    """Crear usuarios demo/admin si la tabla está vacía."""
    if User.query.count() > 0:
        return

    demo_password_hash = hashpw('demo123'.encode('utf-8'), gensalt()).decode('utf-8')
    users = [
        User(username='admin', email='admin@example.com', password_hash=demo_password_hash, role='admin'),
        User(username='demo', email='demo@example.com', password_hash=demo_password_hash, role='user'),
    ]
    db.session.add_all(users)
    db.session.commit()


def _find_existing_movie_for_merge(mapped):
    if mapped.get('external_id'):
        movie = Movie.query.filter_by(source=mapped['source'], external_id=mapped['external_id']).first()
        if movie:
            return movie

    canonical_incoming = _canonical_title_key(mapped.get('title'))
    if not canonical_incoming:
        return None

    candidate_query = Movie.query
    if mapped.get('release_date'):
        candidate_query = candidate_query.filter(Movie.release_date == mapped['release_date'])

    candidates = candidate_query.all()
    for candidate in candidates:
        if _canonical_title_key(candidate.title) == canonical_incoming:
            return candidate

    return None


def deduplicate_movies_by_aliases():
    movies = Movie.query.all()
    groups = {}

    for movie in movies:
        release_year = movie.release_date.year if movie.release_date else None
        group_key = (_canonical_title_key(movie.title), release_year)
        groups.setdefault(group_key, []).append(movie)

    merged_count = 0
    for _, group in groups.items():
        if len(group) < 2:
            continue

        keeper = max(group, key=lambda m: (_movie_data_score(m), -m.id))
        duplicates = [movie for movie in group if movie.id != keeper.id]

        for duplicate in duplicates:
            dup_favorites = Favorites.query.filter_by(movie_id=duplicate.id).all()
            for fav in dup_favorites:
                existing_fav = Favorites.query.filter_by(movie_id=keeper.id, user_id=fav.user_id).first()
                if not existing_fav:
                    db.session.add(Favorites(movie_id=keeper.id, user_id=fav.user_id, created_at=fav.created_at))
                db.session.delete(fav)

            db.session.delete(duplicate)
            merged_count += 1

    if merged_count > 0:
        db.session.commit()

    return merged_count


def _should_sync_movies(force=False):
    if force:
        return True

    state = _get_sync_state('movies_last_sync')
    if not state:
        return True

    try:
        last_sync = datetime.fromisoformat(state.value)
    except ValueError:
        return True

    elapsed_seconds = (_now_utc() - last_sync).total_seconds()
    return elapsed_seconds >= (MOVIES_SYNC_INTERVAL_MINUTES * 60)


def _extract_provider_movies(payload):
    # Ghibli devuelve lista directa. YTS devuelve objeto con data.movies.
    if isinstance(payload, list):
        return payload

    return payload.get('data', {}).get('movies', [])


def _parse_omdb_release_date(raw_date):
    if not raw_date or raw_date == 'N/A':
        return None

    try:
        return datetime.strptime(raw_date, '%d %b %Y').date()
    except ValueError:
        return None


def _parse_omdb_runtime(runtime_text):
    if not runtime_text or runtime_text == 'N/A':
        return None

    parts = runtime_text.split()
    if not parts:
        return None

    try:
        return int(parts[0])
    except (ValueError, TypeError):
        return None


def _parse_omdb_rating(rating_text):
    if not rating_text or rating_text == 'N/A':
        return None

    try:
        return float(rating_text)
    except (TypeError, ValueError):
        return None


def _parse_tmdb_release_date(raw_date):
    if not raw_date:
        return None

    try:
        return datetime.strptime(raw_date, '%Y-%m-%d').date()
    except ValueError:
        return None


def _fetch_tmdb_movies():
    if not TMDB_API_KEY:
        raise ValueError('TMDB_API_KEY no configurada')

    genre_response = requests.get(
        f"{TMDB_BASE_URL}/genre/movie/list",
        params={
            'api_key': TMDB_API_KEY,
            'language': TMDB_LANGUAGE,
        },
        timeout=MOVIES_PROVIDER_TIMEOUT_SECONDS,
    )
    genre_response.raise_for_status()
    genre_payload = genre_response.json()
    genre_map = {g['id']: g['name'] for g in genre_payload.get('genres', [])}

    collected = []
    seen_ids = set()
    endpoints = ['now_playing', 'popular']

    for endpoint in endpoints:
        for page in range(1, TMDB_MAX_PAGES + 1):
            response = requests.get(
                f"{TMDB_BASE_URL}/movie/{endpoint}",
                params={
                    'api_key': TMDB_API_KEY,
                    'language': TMDB_LANGUAGE,
                    'page': page,
                },
                timeout=MOVIES_PROVIDER_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            payload = response.json()

            for movie in payload.get('results', []):
                movie_id = movie.get('id')
                if movie_id in seen_ids:
                    continue

                seen_ids.add(movie_id)
                movie['genre_names'] = [genre_map.get(gid) for gid in movie.get('genre_ids', []) if genre_map.get(gid)]
                collected.append(movie)

    return collected


def _fetch_omdb_movies():
    current_year = datetime.now().year
    years = [str(current_year - i) for i in range(OMDB_RECENT_YEARS)]

    # Términos amplios para capturar catálogo variado y reciente
    search_terms = ['action', 'drama', 'comedy', 'horror', 'thriller', 'adventure', 'romance', 'science']

    imdb_ids = []
    seen_ids = set()

    for year in years:
        for term in search_terms:
            for page in range(1, OMDB_MAX_PAGES_PER_QUERY + 1):
                response = requests.get(
                    OMDB_PROVIDER_URL,
                    params={
                        'apikey': OMDB_API_KEY,
                        's': term,
                        'type': 'movie',
                        'y': year,
                        'page': page,
                    },
                    timeout=MOVIES_PROVIDER_TIMEOUT_SECONDS,
                )
                response.raise_for_status()
                payload = response.json()

                if payload.get('Response') != 'True':
                    break

                for item in payload.get('Search', []):
                    imdb_id = item.get('imdbID')
                    if imdb_id and imdb_id not in seen_ids:
                        seen_ids.add(imdb_id)
                        imdb_ids.append(imdb_id)

                if len(imdb_ids) >= OMDB_MAX_TITLES:
                    break

            if len(imdb_ids) >= OMDB_MAX_TITLES:
                break
        if len(imdb_ids) >= OMDB_MAX_TITLES:
            break

    detailed_movies = []
    for imdb_id in imdb_ids[:OMDB_MAX_TITLES]:
        detail_response = requests.get(
            OMDB_PROVIDER_URL,
            params={
                'apikey': OMDB_API_KEY,
                'i': imdb_id,
                'plot': 'short',
            },
            timeout=MOVIES_PROVIDER_TIMEOUT_SECONDS,
        )
        detail_response.raise_for_status()
        detail_payload = detail_response.json()

        if detail_payload.get('Response') == 'True':
            detailed_movies.append(detail_payload)

    return detailed_movies


def _map_provider_movie(raw_movie, provider_source=None):
    source = provider_source or MOVIES_PROVIDER_SOURCE

    if source == 'tmdb':
        title = raw_movie.get('title') or raw_movie.get('name')
        if not title:
            return None

        genre_names = raw_movie.get('genre_names', [])
        poster_path = raw_movie.get('poster_path')

        return {
            'external_id': str(raw_movie.get('id')) if raw_movie.get('id') is not None else None,
            'source': source,
            'title': title,
            'description': raw_movie.get('overview') or None,
            'director': None,
            'genre': ', '.join(genre_names) if genre_names else None,
            'release_date': _parse_tmdb_release_date(raw_movie.get('release_date')),
            'duration_minutes': None,
            'rating': float(raw_movie.get('vote_average')) if raw_movie.get('vote_average') is not None else None,
            'poster_url': f"{TMDB_IMAGE_BASE_URL}{poster_path}" if poster_path else None,
            'video_url': None,
        }

    if source == 'omdb':
        title = raw_movie.get('Title')
        if not title:
            return None

        imdb_id = raw_movie.get('imdbID')
        release_date = _parse_omdb_release_date(raw_movie.get('Released'))
        if not release_date:
            year = raw_movie.get('Year')
            if year and year.isdigit():
                release_date = datetime(int(year), 1, 1).date()

        return {
            'external_id': imdb_id,
            'source': source,
            'title': title,
            'description': raw_movie.get('Plot') if raw_movie.get('Plot') != 'N/A' else None,
            'director': raw_movie.get('Director') if raw_movie.get('Director') != 'N/A' else None,
            'genre': raw_movie.get('Genre') if raw_movie.get('Genre') != 'N/A' else None,
            'release_date': release_date,
            'duration_minutes': _parse_omdb_runtime(raw_movie.get('Runtime')),
            'rating': _parse_omdb_rating(raw_movie.get('imdbRating')),
            'poster_url': raw_movie.get('Poster') if raw_movie.get('Poster') != 'N/A' else None,
            'video_url': f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None,
        }

    if source == 'ghibli':
        release_date = None
        year = raw_movie.get('release_date')
        if year:
            try:
                release_date = datetime(int(year), 1, 1).date()
            except (TypeError, ValueError):
                release_date = None

        title = raw_movie.get('title')
        if not title:
            return None

        return {
            'external_id': str(raw_movie.get('id')) if raw_movie.get('id') is not None else None,
            'source': source,
            'title': title,
            'description': raw_movie.get('description') or None,
            'director': raw_movie.get('director') or None,
            'genre': 'Animacion',
            'release_date': release_date,
            'duration_minutes': int(raw_movie.get('running_time')) if str(raw_movie.get('running_time', '')).isdigit() else None,
            'rating': None,
            'poster_url': raw_movie.get('image') or None,
            'video_url': raw_movie.get('url') or None,
        }

    # Mapeo YTS
    title = raw_movie.get('title')
    if not title:
        return None

    year = raw_movie.get('year')
    release_date = None
    if year:
        try:
            release_date = datetime(int(year), 1, 1).date()
        except (TypeError, ValueError):
            release_date = None

    genres = raw_movie.get('genres') or []

    return {
        'external_id': str(raw_movie.get('id')) if raw_movie.get('id') is not None else None,
        'source': source,
        'title': title,
        'description': raw_movie.get('description_full') or raw_movie.get('summary') or raw_movie.get('description_intro') or None,
        'director': None,
        'genre': ', '.join(genres) if genres else None,
        'release_date': release_date,
        'duration_minutes': raw_movie.get('runtime'),
        'rating': raw_movie.get('rating'),
        'poster_url': raw_movie.get('large_cover_image') or raw_movie.get('medium_cover_image') or None,
        'video_url': raw_movie.get('url') or None,
    }


def sync_movies_from_api(force=False):
    """Sincroniza películas desde API externa hacia la BD local con inserción/actualización incremental."""
    if not _should_sync_movies(force=force):
        return {'skipped': True, 'reason': 'sync_interval_not_reached'}

    created = 0
    updated = 0
    processed = 0

    try:
        source_in_use = 'tmdb'
        pages_to_process = [_fetch_tmdb_movies()]

        for provider_movies in pages_to_process:
            if not provider_movies:
                continue

            for raw_movie in provider_movies:
                mapped = _map_provider_movie(raw_movie, provider_source=source_in_use)
                if not mapped:
                    continue

                processed += 1

                mapped['source'] = source_in_use

                movie = _find_existing_movie_for_merge(mapped)

                if movie:
                    movie.title = mapped['title']
                    movie.description = mapped['description']
                    movie.director = mapped['director']
                    movie.genre = mapped['genre']
                    movie.release_date = mapped['release_date']
                    movie.duration_minutes = mapped['duration_minutes']
                    movie.rating = mapped['rating']
                    movie.poster_url = mapped['poster_url']
                    movie.video_url = mapped['video_url']
                    movie.external_id = mapped['external_id']
                    movie.source = mapped['source']
                    movie.updated_at = _now_utc()
                    updated += 1
                else:
                    db.session.add(Movie(
                        title=mapped['title'],
                        description=mapped['description'],
                        director=mapped['director'],
                        genre=mapped['genre'],
                        release_date=mapped['release_date'],
                        duration_minutes=mapped['duration_minutes'],
                        rating=mapped['rating'],
                        poster_url=mapped['poster_url'],
                        video_url=mapped['video_url'],
                        external_id=mapped['external_id'],
                        source=mapped['source'],
                        created_at=_now_utc(),
                        updated_at=_now_utc(),
                    ))
                    created += 1

        _set_sync_state('movies_last_sync', _now_utc().isoformat())
        db.session.commit()

        total_movies = Movie.query.count()
        tmdb_movies = Movie.query.filter_by(source='tmdb').count()

        return {
            'ok': True,
            'processed': processed,
            'created': created,
            'updated': updated,
            'total_movies': total_movies,
            'tmdb_movies': tmdb_movies,
            'source': source_in_use,
            'url': TMDB_BASE_URL,
        }
    except Exception as e:
        db.session.rollback()
        return {
            'ok': False,
            'error': str(e),
            'source': 'tmdb',
            'url': TMDB_BASE_URL,
        }

# ==================== FUNCIONES DE INICIALIZACIÓN ====================
def init_db():
    """Inicializar base de datos y crear tablas"""
    with app.app_context():
        db.create_all()
        ensure_schema_compatibility()

        removed = purge_non_tmdb_movies()
        if removed > 0:
            print(f"Películas no-TMDB eliminadas de la BD: {removed}")

        # Ejecutar seed data si no hay datos
        if User.query.count() == 0 or Movie.query.count() == 0:
            print("Base de datos vacía o sin películas TMDB; esperando sincronización TMDB...")
        else:
            print("Base de datos preparada para TMDB; se eliminaron datos de otras fuentes si existían.")

        # Sincronización incremental desde API externa (si falla, la app continúa con datos locales)
        sync_result = sync_movies_from_api(force=False)
        if sync_result.get('ok'):
            print(f"Sincronización API OK. Creadas: {sync_result.get('created', 0)} | Actualizadas: {sync_result.get('updated', 0)}")
        elif sync_result.get('skipped'):
            print("Sincronización API omitida por intervalo configurado")
        else:
            print(f"Sincronización API falló: {sync_result.get('error')}")

        merged = deduplicate_movies_by_aliases()
        if merged > 0:
            print(f"Deduplicación aplicada. Películas fusionadas: {merged}")


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
        if MOVIES_AUTO_SYNC_ON_READ:
            sync_movies_from_api(force=False)

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
            'source': p.source,
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
            'source': pelicula.source,
            'created_at': pelicula.created_at.isoformat() if pelicula.created_at else None,
            'updated_at': pelicula.updated_at.isoformat() if pelicula.updated_at else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas', methods=['POST'])
@cors_enabled
def crear_pelicula():
    try:
        return jsonify({'error': 'La creación manual de películas está deshabilitada. Solo se aceptan películas sincronizadas desde TMDB.'}), 403

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/peliculas/<int:id>', methods=['PUT'])
@cors_enabled
def editar_pelicula(id):
    try:
        return jsonify({'error': 'La edición manual de películas está deshabilitada. Solo se persisten datos sincronizados desde TMDB.'}), 403

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


@app.route('/api/sync/peliculas', methods=['POST'])
@cors_enabled
def sincronizar_peliculas_api():
    try:
        # Obtener user_id del token y verificar rol admin
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token requerido'}), 401

        token = auth_header.split(' ')[1]
        try:
            user_id = int(token.split('_')[1])
        except Exception:
            return jsonify({'error': 'Token inválido'}), 401

        usuario = db.session.get(User, user_id)
        if not usuario or usuario.role != 'admin':
            return jsonify({'error': 'Acceso denegado. Solo administradores pueden sincronizar películas.'}), 403

        sync_result = sync_movies_from_api(force=True)
        if sync_result.get('ok'):
            return jsonify({
                'mensaje': 'Sincronización completada',
                'resultado': sync_result,
            }), 200

        return jsonify({
            'error': 'No se pudo completar la sincronización',
            'detalle': sync_result,
        }), 502
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

# Inicializar base de datos siempre que se cargue la aplicación
init_db()

# ==================== INICIAR SERVIDOR ====================
if __name__ == '__main__':
    print("STREAMFLIX corriendo en http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
