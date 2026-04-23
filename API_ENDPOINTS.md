# StreamFlix - Documentación API

## Authentication
- Login: `POST /api/login`
- Register: `POST /api/registro`
- Token format: `Bearer token_{user_id}_{username}`

---

## Películas

### Obtener todas las películas
```
GET /api/peliculas
```
**Respuesta**: Array de películas

### Obtener película por ID
```
GET /api/peliculas/<id>
```
**Respuesta**: Objeto película

### Crear película (Solo Admin)
```
POST /api/peliculas
Authorization: Bearer token

Body:
{
  "title": "string (requerido)",
  "description": "string",
  "director": "string",
  "genre": "string",
  "release_date": "YYYY-MM-DD",
  "duration_minutes": number,
  "rating": number,
  "poster_url": "string",
  "video_url": "string"
}
```

### Editar película (Solo Admin)
```
PUT /api/peliculas/<id>
Authorization: Bearer token

Body: (campos a actualizar)
{
  "title": "string",
  "description": "string",
  ...
}
```

### Eliminar película (Solo Admin)
```
DELETE /api/peliculas/<id>
Authorization: Bearer token
```

---

## Favoritos

### Obtener mis favoritos
```
GET /api/favoritos
Authorization: Bearer token
```
**Respuesta**: Array de películas marcadas como favoritas

### Agregar a favoritos
```
POST /api/favoritos
Authorization: Bearer token

Body:
{
  "movie_id": number
}
```

### Quitar de favoritos
```
DELETE /api/favoritos/<movie_id>
Authorization: Bearer token
```

---

## Críticas y Ratings

### Obtener críticas de una película
```
GET /api/peliculas/<movie_id>/reviews
```
**Respuesta**:
```json
[
  {
    "id": number,
    "user_id": number,
    "username": "string",
    "movie_id": number,
    "rating": 1-10,
    "review_text": "string",
    "created_at": "ISO datetime",
    "updated_at": "ISO datetime"
  }
]
```

### Obtener rating promedio de una película
```
GET /api/peliculas/<movie_id>/average-rating
```
**Respuesta**:
```json
{
  "movie_id": number,
  "average_rating": number (0.00-10.00),
  "total_reviews": number
}
```

### Obtener mis críticas
```
GET /api/reviews
Authorization: Bearer token
```
**Respuesta**: Array de críticas del usuario autenticado

### Crear crítica
```
POST /api/reviews
Authorization: Bearer token

Body:
{
  "movie_id": number (requerido),
  "rating": 1-10 (requerido),
  "review_text": "string (opcional)"
}
```
**Nota**: Un usuario solo puede tener una crítica por película

### Editar crítica
```
PUT /api/reviews/<review_id>
Authorization: Bearer token

Body:
{
  "rating": 1-10,
  "review_text": "string"
}
```
**Nota**: Solo puede editar sus propias críticas

### Eliminar crítica
```
DELETE /api/reviews/<review_id>
Authorization: Bearer token
```
**Nota**: Solo puede eliminar sus propias críticas

---

## Códigos de Error

| Código | Descripción |
|--------|------------|
| 200 | OK - Éxito |
| 201 | Created - Recurso creado exitosamente |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Token requerido o inválido |
| 403 | Forbidden - Acceso denegado (no admin, no propietario) |
| 404 | Not Found - Recurso no encontrado |
| 409 | Conflict - Duplicado (ej: película ya en favoritos) |
| 500 | Server Error - Error del servidor |

---

## Ejemplos de Uso

### Registrar usuario
```bash
curl -X POST http://localhost:5000/api/registro \
  -H "Content-Type: application/json" \
  -d '{"username": "juan", "email": "juan@example.com", "password": "pass123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "juan@example.com", "password": "pass123"}'
```

### Crear crítica
```bash
curl -X POST http://localhost:5000/api/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token_1_juan" \
  -d '{"movie_id": 1, "rating": 9, "review_text": "¡Excelente película!"}'
```

### Obtener críticas de una película
```bash
curl http://localhost:5000/api/peliculas/1/reviews
```

### Obtener rating promedio
```bash
curl http://localhost:5000/api/peliculas/1/average-rating
```
