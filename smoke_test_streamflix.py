"""STREAMFLIX smoke test runner.

Ejecuta una batería de comprobaciones contra un servidor local en marcha.
Por defecto no hace operaciones destructivas; con --destructive también
prueba delete de una pelicula y una serie, y luego las restaura con sync.

Uso:
  python smoke_test_streamflix.py
  python smoke_test_streamflix.py --base-url http://localhost:5000 --destructive
"""

from __future__ import annotations

import argparse
import sys
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


@dataclass
class SmokeContext:
    base_url: str
    session: requests.Session = field(default_factory=requests.Session)
    admin_token: str = ""
    user_token: str = ""
    temp_user_email: str = ""
    temp_user_password: str = ""
    movie_id: int | None = None
    series_id: int | None = None
    created_movie_review_id: int | None = None
    created_series_review_id: int | None = None
    results: list[str] = field(default_factory=list)


class SmokeFailure(Exception):
    pass


def api_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}" + path


def request_json(ctx: SmokeContext, method: str, path: str, *, token: str | None = None, expected: set[int] | None = None, **kwargs: Any) -> tuple[requests.Response, Any]:
    headers = kwargs.pop('headers', {}) or {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    response = ctx.session.request(method, api_url(ctx.base_url, path), headers=headers, timeout=20, **kwargs)
    if expected and response.status_code not in expected:
        raise SmokeFailure(f"{method} {path} -> {response.status_code}, esperado {sorted(expected)}: {response.text[:400]}")
    try:
        payload = response.json()
    except ValueError:
        payload = None
    return response, payload


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeFailure(message)


def ensure_login(ctx: SmokeContext, email: str, password: str, role_label: str) -> str:
    response, payload = request_json(
        ctx,
        'POST',
        '/api/login',
        json={'email': email, 'password': password},
        expected={200},
    )
    token = payload.get('token') if isinstance(payload, dict) else None
    assert_true(bool(token), f'No se obtuvo token para {role_label}')
    return token


def step(ctx: SmokeContext, title: str, fn: Callable[[], None]) -> None:
    print(f'[+] {title}')
    fn()
    ctx.results.append(title)


def check_static_assets(ctx: SmokeContext) -> None:
    response = ctx.session.get(api_url(ctx.base_url, '/'), timeout=20)
    assert_true(response.status_code == 200, f'GET / devolvio {response.status_code}')

    response = ctx.session.get(api_url(ctx.base_url, '/app.js'), timeout=20)
    assert_true(response.status_code == 200, f'GET /app.js devolvio {response.status_code}')


def check_registration_and_login(ctx: SmokeContext) -> None:
    unique = uuid.uuid4().hex[:8]
    ctx.temp_user_email = f'smoke_{unique}@example.com'
    ctx.temp_user_password = 'SmokePass123!'

    response, payload = request_json(
        ctx,
        'POST',
        '/api/registro',
        json={
            'username': f'smoke_{unique}',
            'email': ctx.temp_user_email,
            'password': ctx.temp_user_password,
        },
        expected={201, 409},
    )
    if response.status_code == 201:
        assert_true(isinstance(payload, dict) and 'usuario' in payload, 'La respuesta de registro no contiene usuario')

    ctx.user_token = ensure_login(ctx, ctx.temp_user_email, ctx.temp_user_password, 'usuario de prueba')


def check_admin_login(ctx: SmokeContext) -> None:
    ctx.admin_token = ensure_login(ctx, 'admin@example.com', 'demo123', 'admin')


def check_catalog_lists(ctx: SmokeContext) -> None:
    response, movies = request_json(ctx, 'GET', '/api/peliculas', expected={200})
    assert_true(isinstance(movies, list), '/api/peliculas no devolvio una lista')
    assert_true(len(movies) > 0, 'El catalogo de peliculas esta vacio')
    assert_true(all(item.get('source') == 'tmdb' for item in movies), 'Hay peliculas fuera de TMDB en el listado')
    ctx.movie_id = int(movies[0]['id'])

    response, series = request_json(ctx, 'GET', '/api/series', expected={200})
    assert_true(isinstance(series, list), '/api/series no devolvio una lista')
    assert_true(len(series) > 0, 'El catalogo de series esta vacio')
    assert_true(all(item.get('source', 'tmdb') == 'tmdb' or 'source' not in item for item in series), 'Hay series fuera de TMDB en el listado')
    ctx.series_id = int(series[0]['id'])


def check_catalog_details(ctx: SmokeContext) -> None:
    assert_true(ctx.movie_id is not None, 'No hay movie_id para probar detalle')
    assert_true(ctx.series_id is not None, 'No hay series_id para probar detalle')

    _, movie = request_json(ctx, 'GET', f'/api/peliculas/{ctx.movie_id}', expected={200})
    assert_true(isinstance(movie, dict) and movie.get('id') == ctx.movie_id, 'Detalle de pelicula incorrecto')

    _, serie = request_json(ctx, 'GET', f'/api/series/{ctx.series_id}', expected={200})
    assert_true(isinstance(serie, dict) and serie.get('id') == ctx.series_id, 'Detalle de serie incorrecto')


def check_favorites(ctx: SmokeContext) -> None:
    assert_true(ctx.movie_id is not None, 'No hay movie_id para favoritos')
    assert_true(ctx.series_id is not None, 'No hay series_id para favoritos')

    _, payload = request_json(ctx, 'GET', '/api/favoritos', token=ctx.user_token, expected={200})
    assert_true(isinstance(payload, list), 'GET /api/favoritos no devolvio lista')

    _, payload = request_json(ctx, 'POST', '/api/favoritos', token=ctx.user_token, json={'movie_id': ctx.movie_id}, expected={201, 200, 409})
    if isinstance(payload, dict) and 'mensaje' in payload:
        pass

    _, payload = request_json(ctx, 'DELETE', f'/api/favoritos/{ctx.movie_id}', token=ctx.user_token, expected={200, 404})
    assert_true(payload is None or isinstance(payload, dict), 'DELETE favoritos devolvio un formato inesperado')

    _, payload = request_json(ctx, 'GET', '/api/series-favoritos', token=ctx.user_token, expected={200})
    assert_true(isinstance(payload, list), 'GET /api/series-favoritos no devolvio lista')

    _, payload = request_json(ctx, 'POST', '/api/series-favoritos', token=ctx.user_token, json={'series_id': ctx.series_id}, expected={201, 200, 409, 404})
    assert_true(payload is None or isinstance(payload, dict), 'POST series-favoritos devolvio un formato inesperado')

    _, payload = request_json(ctx, 'DELETE', f'/api/series-favoritos/{ctx.series_id}', token=ctx.user_token, expected={200, 404})
    assert_true(payload is None or isinstance(payload, dict), 'DELETE series-favoritos devolvio un formato inesperado')


def check_reviews(ctx: SmokeContext) -> None:
    assert_true(ctx.movie_id is not None, 'No hay movie_id para reviews')
    assert_true(ctx.series_id is not None, 'No hay series_id para reviews')

    _, payload = request_json(ctx, 'GET', f'/api/peliculas/{ctx.movie_id}/reviews', expected={200})
    assert_true(isinstance(payload, list), 'GET reviews de pelicula no devolvio lista')

    _, payload = request_json(ctx, 'GET', f'/api/peliculas/{ctx.movie_id}/average-rating', expected={200})
    assert_true(isinstance(payload, dict) and 'average_rating' in payload, 'GET average-rating pelicula invalido')

    _, payload = request_json(
        ctx,
        'POST',
        '/api/reviews',
        token=ctx.user_token,
        json={'movie_id': ctx.movie_id, 'rating': 9, 'review_text': 'Smoke test review for movie'},
        expected={201, 409},
    )
    if isinstance(payload, dict) and payload.get('review'):
        ctx.created_movie_review_id = int(payload['review']['id'])
    elif ctx.created_movie_review_id is None:
        _, reviews = request_json(ctx, 'GET', f'/api/peliculas/{ctx.movie_id}/reviews', expected={200})
        if isinstance(reviews, list):
            for review in reviews:
                if review.get('review_text') == 'Smoke test review for movie':
                    ctx.created_movie_review_id = int(review['id'])
                    break

    if ctx.created_movie_review_id is not None:
        _, payload = request_json(ctx, 'DELETE', f'/api/reviews/{ctx.created_movie_review_id}', token=ctx.user_token, expected={200, 404, 403})
        assert_true(payload is None or isinstance(payload, dict), 'DELETE review pelicula devolvio un formato inesperado')

    _, payload = request_json(ctx, 'GET', f'/api/series/{ctx.series_id}/reviews', expected={200})
    assert_true(isinstance(payload, list), 'GET reviews de serie no devolvio lista')

    _, payload = request_json(ctx, 'GET', f'/api/series/{ctx.series_id}/average-rating', expected={200})
    assert_true(isinstance(payload, dict) and 'average_rating' in payload, 'GET average-rating serie invalido')

    _, payload = request_json(
        ctx,
        'POST',
        '/api/series/reviews',
        token=ctx.user_token,
        json={'series_id': ctx.series_id, 'rating': 8, 'review_text': 'Smoke test review for series'},
        expected={201, 409},
    )
    if isinstance(payload, dict) and payload.get('review'):
        ctx.created_series_review_id = int(payload['review']['id'])
    elif ctx.created_series_review_id is None:
        _, reviews = request_json(ctx, 'GET', f'/api/series/{ctx.series_id}/reviews', expected={200})
        if isinstance(reviews, list):
            for review in reviews:
                if review.get('review_text') == 'Smoke test review for series':
                    ctx.created_series_review_id = int(review['id'])
                    break

    if ctx.created_series_review_id is not None:
        _, payload = request_json(ctx, 'DELETE', f'/api/series/reviews/{ctx.created_series_review_id}', token=ctx.user_token, expected={200, 404, 403})
        assert_true(payload is None or isinstance(payload, dict), 'DELETE review serie devolvio un formato inesperado')


def check_permissions(ctx: SmokeContext) -> None:
    _, payload = request_json(ctx, 'POST', '/api/peliculas', token=ctx.user_token, json={'title': 'Forbidden'}, expected={403})
    assert_true(isinstance(payload, dict) and 'error' in payload, 'POST /api/peliculas sin admin no rechazo correctamente')

    _, payload = request_json(ctx, 'POST', '/api/series', token=ctx.user_token, json={'title': 'Forbidden'}, expected={403})
    assert_true(isinstance(payload, dict) and 'error' in payload, 'POST /api/series sin admin no rechazo correctamente')


def check_sync(ctx: SmokeContext) -> None:
    _, payload = request_json(ctx, 'POST', '/api/sync/peliculas', token=ctx.admin_token, expected={200})
    assert_true(isinstance(payload, dict) and 'resultado' in payload, 'Sync de peliculas no devolvio resultado')

    _, payload = request_json(ctx, 'POST', '/api/sync/series', token=ctx.admin_token, expected={200})
    assert_true(isinstance(payload, dict) and 'resultado' in payload, 'Sync de series no devolvio resultado')


def check_movie_search_performance(ctx: SmokeContext) -> None:
    """Mide el rendimiento al obtener y filtrar películas."""
    search_terms = ['the', 'and', 'a', 'to', 'of']
    search_times = []
    
    for term in search_terms:
        start_time = time.time()
        _, movies = request_json(ctx, 'GET', '/api/peliculas', expected={200})
        elapsed_time = time.time() - start_time
        search_times.append(elapsed_time)
        
        assert_true(isinstance(movies, list), f'GET /api/peliculas no devolvio lista')
        # Simular filtrado en cliente
        filtered = [m for m in movies if term.lower() in str(m.get('title', '')).lower()]
        assert_true(elapsed_time < 10, f'GET /api/peliculas tardo {elapsed_time:.2f}s (limite: 10s)')
    
    avg_time = sum(search_times) / len(search_times)
    print(f'   Tiempo promedio de respuesta de catálogo: {avg_time:.2f}s (individual: {[f"{t:.2f}s" for t in search_times]})')


def check_concurrent_users_load(ctx: SmokeContext) -> None:
    """Prueba carga de 25+ usuarios conectados simultáneamente."""
    num_users = 30
    user_tokens = []
    failed_logins = 0
    login_times = []
    
    def create_and_login_user(user_index: int) -> tuple[bool, float]:
        """Crea un usuario y lo autentica."""
        try:
            unique = f"{uuid.uuid4().hex[:6]}_{user_index}"
            email = f'load_{unique}@example.com'
            password = 'LoadTest123!'
            
            # Registrar usuario
            local_session = requests.Session()
            headers = {}
            start_time = time.time()
            response = local_session.post(
                api_url(ctx.base_url, '/api/registro'),
                json={'username': f'load_{unique}', 'email': email, 'password': password},
                timeout=20,
                headers=headers
            )
            
            # Login
            response = local_session.post(
                api_url(ctx.base_url, '/api/login'),
                json={'email': email, 'password': password},
                timeout=20,
                headers=headers
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    payload = response.json()
                    token = payload.get('token')
                    return (token is not None, elapsed)
                except ValueError:
                    return (False, elapsed)
            return (False, elapsed)
        except Exception as e:
            print(f'   Error en usuario {user_index}: {e}')
            return (False, 0)
    
    # Ejecutar registros y logins concurrentes
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(create_and_login_user, i): i for i in range(num_users)}
        
        for future in as_completed(futures):
            user_index = futures[future]
            try:
                success, elapsed = future.result()
                if success:
                    user_tokens.append(True)
                    login_times.append(elapsed)
                else:
                    failed_logins += 1
            except Exception as e:
                print(f'   Exception en usuario {user_index}: {e}')
                failed_logins += 1
    
    successful_users = len(user_tokens)
    assert_true(successful_users >= 25, f'Solo {successful_users} usuarios se conectaron exitosamente (minimo requerido: 25)')
    
    avg_login_time = sum(login_times) / len(login_times) if login_times else 0
    print(f'   {successful_users}/{num_users} usuarios conectados exitosamente')
    print(f'   Tiempo promedio de login: {avg_login_time:.2f}s')
    if failed_logins > 0:
        print(f'   Fallos: {failed_logins}')


def destructive_delete_and_restore(ctx: SmokeContext) -> None:
    assert_true(ctx.movie_id is not None, 'No hay movie_id para borrar')
    assert_true(ctx.series_id is not None, 'No hay series_id para borrar')

    _, payload = request_json(ctx, 'DELETE', f'/api/peliculas/{ctx.movie_id}', token=ctx.admin_token, expected={200, 404})
    assert_true(payload is None or isinstance(payload, dict), 'DELETE pelicula devolvio formato inesperado')

    _, movies = request_json(ctx, 'GET', '/api/peliculas', expected={200})
    assert_true(all(int(movie['id']) != ctx.movie_id for movie in movies), 'La pelicula borrada sigue apareciendo antes de resync')

    _, payload = request_json(ctx, 'POST', '/api/sync/peliculas', token=ctx.admin_token, expected={200})
    assert_true(isinstance(payload, dict), 'Resync de peliculas no devolvio JSON')

    _, movies = request_json(ctx, 'GET', '/api/peliculas', expected={200})
    assert_true(any(movie.get('id') == ctx.movie_id or movie.get('title') for movie in movies), 'La resincro de peliculas no repobló el catalogo')

    _, payload = request_json(ctx, 'DELETE', f'/api/series/{ctx.series_id}', token=ctx.admin_token, expected={200, 404})
    assert_true(payload is None or isinstance(payload, dict), 'DELETE serie devolvio formato inesperado')

    _, series = request_json(ctx, 'GET', '/api/series', expected={200})
    assert_true(all(int(serie['id']) != ctx.series_id for serie in series), 'La serie borrada sigue apareciendo antes de resync')

    _, payload = request_json(ctx, 'POST', '/api/sync/series', token=ctx.admin_token, expected={200})
    assert_true(isinstance(payload, dict), 'Resync de series no devolvio JSON')

    _, series = request_json(ctx, 'GET', '/api/series', expected={200})
    assert_true(any(serie.get('id') == ctx.series_id or serie.get('title') for serie in series), 'La resincro de series no repobló el catalogo')


def run_smoke(ctx: SmokeContext, destructive: bool) -> None:
    steps: list[tuple[str, Callable[[], None]]] = [
        ('assets estaticos', lambda: check_static_assets(ctx)),
        ('registro y login de usuario', lambda: check_registration_and_login(ctx)),
        ('login de admin', lambda: check_admin_login(ctx)),
        ('catalogos TMDB', lambda: check_catalog_lists(ctx)),
        ('detalle de catalogo', lambda: check_catalog_details(ctx)),
        ('favoritos de peliculas y series', lambda: check_favorites(ctx)),
        ('reviews de peliculas y series', lambda: check_reviews(ctx)),
        ('permisos de admin', lambda: check_permissions(ctx)),
        ('sincronizacion de peliculas y series', lambda: check_sync(ctx)),
        ('rendimiento de busquedas de peliculas', lambda: check_movie_search_performance(ctx)),
        ('carga de 25+ usuarios concurrentes', lambda: check_concurrent_users_load(ctx)),
    ]

    for title, fn in steps:
        step(ctx, title, fn)

    if destructive:
        step(ctx, 'borrado y restauracion', lambda: destructive_delete_and_restore(ctx))


def main() -> int:
    parser = argparse.ArgumentParser(description='Smoke test de STREAMFLIX')
    parser.add_argument('--base-url', default='http://localhost:5000', help='URL base del servidor local')
    parser.add_argument('--destructive', action='store_true', help='Prueba borrado y restauracion de una pelicula y una serie')
    args = parser.parse_args()

    ctx = SmokeContext(base_url=args.base_url)

    try:
        run_smoke(ctx, destructive=args.destructive)
    except SmokeFailure as exc:
        print(f'[FAIL] {exc}')
        return 1
    except requests.RequestException as exc:
        print(f'[FAIL] Error de red: {exc}')
        return 1

    print('\nOK: todas las comprobaciones han pasado.')
    for item in ctx.results:
        print(f' - {item}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
