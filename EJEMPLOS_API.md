# 📡 EJEMPLOS DE USO DE LA API REST - STREAMFLIX

Guía completa con ejemplos de cómo consumir los endpoints de la API usando cURL, JavaScript (fetch) o Postman.

---

## 🔐 AUTENTICACIÓN

### 1. REGISTRO DE USUARIO

**Endpoint:** `POST /api/registro`

#### cURL
```bash
curl -X POST http://localhost:5000/api/registro \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_doe",
    "email": "juan@example.com",
    "password": "miContraseña123"
  }'
```

#### JavaScript (Fetch)
```javascript
const registroData = {
  username: "juan_doe",
  email: "juan@example.com",
  password: "miContraseña123"
};

fetch('http://localhost:5000/api/registro', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(registroData)
})
.then(response => response.json())
.then(data => console.log('Éxito:', data))
.catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (201)
```json
{
  "mensaje": "Usuario registrado exitosamente",
  "usuario": {
    "id": 1,
    "username": "juan_doe",
    "email": "juan@example.com",
    "role": "user"
  }
}
```

#### Respuesta de Error (409 - Email duplicado)
```json
{
  "error": "El email ya está registrado"
}
```

---

### 2. INICIAR SESIÓN (LOGIN)

**Endpoint:** `POST /api/login`

#### cURL
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "miContraseña123"
  }'
```

#### JavaScript (Fetch)
```javascript
const loginData = {
  email: "juan@example.com",
  password: "miContraseña123"
};

fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(loginData)
})
.then(response => response.json())
.then(data => {
  // Guardar token en localStorage
  localStorage.setItem('token', data.token);
  console.log('Token:', data.token);
})
.catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (200)
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 1,
    "username": "juan_doe",
    "email": "juan@example.com",
    "role": "user"
  }
}
```

---

## 🎬 PELÍCULAS (CRUD)

### 3. OBTENER TODAS LAS PELÍCULAS (GET)

**Endpoint:** `GET /api/peliculas`

#### cURL
```bash
curl http://localhost:5000/api/peliculas
```

#### JavaScript (Fetch)
```javascript
fetch('http://localhost:5000/api/peliculas')
  .then(response => response.json())
  .then(peliculas => console.log(peliculas))
  .catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (200)
```json
[
  {
    "id": 1,
    "title": "Inception",
    "description": "A skilled thief who steals corporate secrets...",
    "director": "Christopher Nolan",
    "genre": "Sci-Fi",
    "release_date": "2010-07-16",
    "duration_minutes": 148,
    "rating": 8.8,
    "poster_url": "https://example.com/inception.jpg",
    "video_url": null
  },
  ...
]
```

---

### 4. OBTENER UNA PELÍCULA POR ID

**Endpoint:** `GET /api/peliculas/<id>`

#### cURL
```bash
curl http://localhost:5000/api/peliculas/1
```

#### JavaScript (Fetch)
```javascript
const movieId = 1;

fetch(`http://localhost:5000/api/peliculas/${movieId}`)
  .then(response => response.json())
  .then(pelicula => console.log(pelicula))
  .catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (200)
```json
{
  "id": 1,
  "title": "Inception",
  "description": "A skilled thief who steals corporate secrets...",
  "director": "Christopher Nolan",
  "genre": "Sci-Fi",
  "release_date": "2010-07-16",
  "duration_minutes": 148,
  "rating": 8.8,
  "poster_url": "https://example.com/inception.jpg"
}
```

---

### 5. CREAR UNA NUEVA PELÍCULA (POST) - ⚠️ SOLO ADMIN

**Endpoint:** `POST /api/peliculas`

**Requiere:** Token JWT con rol admin

#### cURL con Token
```bash
curl -X POST http://localhost:5000/api/peliculas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu_token_jwt_aqui" \
  -d '{
    "title": "The Matrix",
    "description": "A hacker learns about the true nature of his reality...",
    "director": "Lana Wachowski, Lilly Wachowski",
    "genre": "Sci-Fi",
    "release_date": "1999-03-31",
    "duration_minutes": 136,
    "rating": 8.7,
    "poster_url": "https://example.com/matrix.jpg",
    "video_url": "https://example.com/matrix-video.mp4"
  }'
```

#### JavaScript (Fetch) con Token
```javascript
const token = localStorage.getItem('token');
const peliculaNueva = {
  title: "The Matrix",
  description: "A hacker learns about the true nature of his reality...",
  director: "Lana Wachowski, Lilly Wachowski",
  genre: "Sci-Fi",
  release_date: "1999-03-31",
  duration_minutes: 136,
  rating: 8.7,
  poster_url: "https://example.com/matrix.jpg"
};

fetch('http://localhost:5000/api/peliculas', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(peliculaNueva)
})
.then(response => response.json())
.then(data => console.log('Película creada:', data))
.catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (201)
```json
{
  "mensaje": "Película creada exitosamente",
  "pelicula": {
    "id": 2,
    "title": "The Matrix",
    "description": "A hacker learns about the true nature of his reality...",
    "director": "Lana Wachowski, Lilly Wachowski",
    "genre": "Sci-Fi",
    "release_date": "1999-03-31",
    "duration_minutes": 136,
    "rating": 8.7,
    "poster_url": "https://example.com/matrix.jpg"
  }
}
```

#### Respuesta de Error (403 - No es admin)
```json
{
  "error": "Acceso denegado. Solo administradores"
}
```

---

### 6. ACTUALIZAR UNA PELÍCULA (PUT) - ⚠️ SOLO ADMIN

**Endpoint:** `PUT /api/peliculas/<id>`

#### cURL con Token
```bash
curl -X PUT http://localhost:5000/api/peliculas/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu_token_jwt_aqui" \
  -d '{
    "title": "Inception (Actualizado)",
    "rating": 9.0
  }'
```

#### JavaScript (Fetch) con Token
```javascript
const token = localStorage.getItem('token');
const movieId = 1;
const actualizaciones = {
  title: "Inception (Actualizado)",
  rating: 9.0
};

fetch(`http://localhost:5000/api/peliculas/${movieId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(actualizaciones)
})
.then(response => response.json())
.then(data => console.log('Película actualizada:', data))
.catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (200)
```json
{
  "mensaje": "Película actualizada exitosamente",
  "pelicula": {
    "id": 1,
    "title": "Inception (Actualizado)",
    "rating": 9.0,
    ...
  }
}
```

---

### 7. ELIMINAR UNA PELÍCULA (DELETE) - ⚠️ SOLO ADMIN

**Endpoint:** `DELETE /api/peliculas/<id>`

#### cURL con Token
```bash
curl -X DELETE http://localhost:5000/api/peliculas/1 \
  -H "Authorization: Bearer tu_token_jwt_aqui"
```

#### JavaScript (Fetch) con Token
```javascript
const token = localStorage.getItem('token');
const movieId = 1;

fetch(`http://localhost:5000/api/peliculas/${movieId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(response => response.json())
.then(data => console.log('Película eliminada:', data))
.catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (200)
```json
{
  "mensaje": "Película eliminada exitosamente"
}
```

---

## ❤️ FAVORITOS

### 8. AGREGAR PELÍCULA A FAVORITOS (POST)

**Endpoint:** `POST /api/favoritos`

$
**Requiere:** Token JWT autenticado (cualquier rol)

#### cURL con Token
```bash
curl -X POST http://localhost:5000/api/favoritos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu_token_jwt_aqui" \
  -d '{
    "movie_id": 1
  }'
```

#### JavaScript (Fetch) con Token
```javascript
const token = localStorage.getItem('token');
const movieId = 1;

fetch('http://localhost:5000/api/favoritos', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ movie_id: movieId })
})
.then(response => response.json())
.then(data => console.log('Agregado a favoritos:', data))
.catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (201)
```json
{
  "mensaje": "Película agregada a favoritos"
}
```

---

### 9. OBTENER MIS PELÍCULAS FAVORITAS (GET)

**Endpoint:** `GET /api/favoritos`

#### cURL con Token
```bash
curl http://localhost:5000/api/favoritos \
  -H "Authorization: Bearer tu_token_jwt_aqui"
```

#### JavaScript (Fetch) con Token
```javascript
const token = localStorage.getItem('token');

fetch('http://localhost:5000/api/favoritos', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(response => response.json())
.then(favoritos => console.log('Mis favoritos:', favoritos))
.catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (200)
```json
[
  {
    "id": 1,
    "title": "Inception",
    "description": "A skilled thief who steals corporate secrets...",
    "director": "Christopher Nolan",
    "genre": "Sci-Fi",
    "rating": 8.8
  },
  ...
]
```

---

### 10. ELIMINAR PELÍCULA DE FAVORITOS (DELETE)

**Endpoint:** `DELETE /api/favoritos/<movie_id>`

#### cURL con Token
```bash
curl -X DELETE http://localhost:5000/api/favoritos/1 \
  -H "Authorization: Bearer tu_token_jwt_aqui"
```

#### JavaScript (Fetch) con Token
```javascript
const token = localStorage.getItem('token');
const movieId = 1;

fetch(`http://localhost:5000/api/favoritos/${movieId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(response => response.json())
.then(data => console.log('Eliminado de favoritos:', data))
.catch(error => console.error('Error:', error));
```

#### Respuesta Exitosa (200)
```json
{
  "mensaje": "Película eliminada de favoritos"
}
```

---

## 📌 NOTAS IMPORTANTES

### Tokens JWT
- El token se obtiene al hacer login
- Debe enviarse en el header: `Authorization: Bearer <token>`
- Expira en 24 horas
- Guardar en `localStorage` para mantener la sesión

### Códigos HTTP
- **200:** Éxito (GET, PUT)
- **201:** Creado (POST)
- **400:** Bad Request (datos faltantes o inválidos)
- **401:** No autorizado (token faltante o inválido)
- **403:** Prohibido (sin permisos suficientes)
- **404:** No encontrado (recurso inexistente)
- **409:** Conflicto (Email duplicado, película ya en favoritos)
- **500:** Error interno del servidor

### Roles
- **user:** Puede ver películas, agregar a favoritos
- **admin:** Puede hacer todo + crear/actualizar/eliminar películas

---

## 🧪 TESTING CON POSTMAN

### Importar Colección
1. Abrir Postman
2. Ir a: `File > Import`
3. Crear solicitudes para cada endpoint

### Variables de Entorno en Postman
```json
{
  "base_url": "http://localhost:5000",
  "token": "",
  "user_id": ""
}
```

---

**Última actualización:** 4 de Abril, 2026
