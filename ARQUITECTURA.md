# 🏗️ ARQUITECTURA STREAMFLIX - DIAGRAMAS Y FLOWS

---

## 📐 ARQUITECTURA DE CAPAS

```
┌─────────────────────────────────────────────────────────────┐
│                      CAPA DE PRESENTACIÓN                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ index.html   │  │  app.js      │  │  styles.css  │         │
│  │ (Estructura) │  │ (Lógica SPA) │  │ (Diseño)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         ↓                   ↓                ↓                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │        Single Page Application (Vanilla JS)              │ │
│  │  - Rutas del lado del cliente                            │ │
│  │  - Gestión del estado (tokens, usuarios)                 │ │
│  │  - Renderización dinámica del DOM                        │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓  ↑
                         HTTP/REST (JSON)
                              ↓  ↑
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE NEGOCIO                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Flask Application (app.py)                              │ │
│  │  ┌────────────────────────────────────────────────────┐  │ │
│  │  │  Middlewares & Decoradores                        │  │ │
│  │  │  - @token_required (autenticación JWT)            │  │ │
│  │  │  - @admin_required (autorización)                 │  │ │
│  │  │  - CORS (Control de acceso)                       │  │ │
│  │  └────────────────────────────────────────────────────┘  │ │
│  │                                                          │ │
│  │  ┌────────────────────────────────────────────────────┐  │ │
│  │  │  Rutas (Endpoints)                                 │  │ │
│  │  │  - /api/registro, /api/login                      │  │ │
│  │  │  - /api/peliculas, /api/series                    │  │ │
│  │  │  - /api/favoritos, /api/series-favoritos          │  │ │
│  │  │  - /api/reviews, /api/series/reviews              │  │ │
│  │  │  - /api/sync/peliculas, /api/sync/series          │  │ │
│  │  └────────────────────────────────────────────────────┘  │ │
│  │                                                          │ │
│  │  ┌────────────────────────────────────────────────────┐  │ │
│  │  │  Lógica de Negocio                                │  │ │
│  │  │  - Validaciones de datos                          │  │ │
│  │  │  - Hasheo de contraseñas (Bcrypt)                 │  │ │
│  │  │  - Generación de tokens (JWT)                     │  │ │
│  │  │  - Sincronización incremental desde TMDB          │  │ │
│  │  │  - Purga de contenido local no-TMDB               │  │ │
│  │  └────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓  ↑
                           SQL/ORM
                              ↓  ↑
┌─────────────────────────────────────────────────────────────┐
│               CAPA DE PERSISTENCIA (BD)                         │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  SQLAlchemy ORM (app.py)                                 │ │
│  │  ┌────────────────────────────────────────────────────┐  │ │
│  │  │  Modelos                                          │  │ │
│  │  │  - User (usuarios)                                │  │ │
│  │  │  - Movie (películas TMDB)                         │  │ │
│  │  │  - Series / Episode                               │  │ │
│  │  │  - Favorites / SeriesFavorites                   │  │ │
│  │  │  - Reviews / SeriesReview / EpisodeReview        │  │ │
│  │  │  - SyncState                                      │  │ │
│  │  └────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              ↓                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  SQLite Database (`streamflix.db`)                       │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │ user         │  │ movie        │  │ series       │   │ │
│  │  │ - id         │  │ - id         │  │ - id         │   │ │
│  │  │ - username   │  │ - title      │  │ - title      │   │ │
│  │  │ - email      │  │ - source     │  │ - source     │   │ │
│  │  │ - password   │  │ - external_id│  │ - external_id│   │ │
│  │  │ - role       │  │ - created_at │  │ - created_at │   │ │
│  │  │ - created_at │  │ - updated_at │  │ - updated_at │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  │  ┌──────────────┐  ┌────────────────┐  ┌──────────────┐ │ │
│  │  │ favorites    │  │ series_favs    │  │ sync_state   │ │ │
│  │  │ - user_id(FK) │  │ - user_id(FK)  │  │ - key        │ │ │
│  │  │ - movie_id(FK)│  │ - series_id(FK)│  │ - value      │ │ │
│  │  │ - created_at │  │ - created_at   │  │ - updated_at │ │ │
│  │  └──────────────┘  └────────────────┘  └──────────────┘ │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 FLUJO DE AUTENTICACIÓN

```
┌─────────────┐                                    ┌────────────┐
│   Usuario   │                                    │   Backend  │
│   (Browser) │                                    │   (Flask)  │
└─────────────┘                                    └────────────┘
      │                                                   │
      │  1. Ingresa credenciales (email, password)       │
      │──────────────────────────────────────────────────>
      │                                                   │
      │                                    2. Busca usuario en BD
      │                                    3. Verifica contraseña
      │                                       (Bcrypt.verify)
      │                                                   │
      │                    4. Genera JWT Token (24hs)    │
      │  <──────────────────────────────────────────────
      │  {token, usuario}                                │
      │                                                   │
      │  5. Guarda token en localStorage                 │
      │  6. Almacena datos del usuario                   │
      │                                                   │
    │  7. Hace petición con token en header            │
    │     GET /api/peliculas / GET /api/series         │
      │     Authorization: Bearer <token>                │
      │──────────────────────────────────────────────────>
      │                                                   │
      │                         8. Verifica token JWT
      │                         9. Valida expiración
      │                         10. Autoriza petición
      │                                                   │
      │  <──────────────────────────────────────────────
      │  [peliculas_json]                                │
      │                                                   │
    │  11. Renderiza catálogo en el DOM                │
      │                                                   │
```

---

## 🎬 FLUJO: OBTENER PELÍCULAS (READ)

```
┌─────────────────────┐
│   Frontend (app.js) │
└─────────────────────┘
          │
          │ 1. fetch('http://localhost:5000/api/peliculas')
          ↓
┌─────────────────────────────────────┐
│  Backend (Flask - app.py)           │
│  @app.route('/api/peliculas')      │
│  def obtener_peliculas():           │
│    - peliculas = Movie.query.filter_by(source='tmdb').all()  │ ← 2. Consulta BD
│    - return jsonify(...)             │
└─────────────────────────────────────┘
          │
          │ 2. SELECT * FROM movie;
          ↓
┌──────────────────────────────┐
│  Base de Datos (SQLite)       │
│  ┌─────────────────────────┐ │
│  │ movie table             │ │
│  │ ┌──────────────────────┐│ │
│  │ │ id │ title │ rating ││ │
│  │ ├──────────────────────┤│ │
│  │ │ 1  │Inception│ 8.8 ││ │
│  │ │ 2  │ Matrix  │ 8.7 ││ │
│  │ │ 3  │Interst. │ 8.6 ││ │
│  │ │...                  ││ │
│  │ └──────────────────────┘│ │
│  └─────────────────────────┘ │
└──────────────────────────────┘
          ↑
          │ 3. Devuelve datos [...]
          │
┌─────────────────────────────────────┐
│  SQLAlchemy ORM                     │
│  Convierte filas ↔ Objetos Python   │
└─────────────────────────────────────┘
          ↑
          │ 4. JSON Response
          │
┌─────────────────────────────────────┐
│  Flask Response                     │
│  Content-Type: application/json     │
│  Status: 200 OK                     │
│  Body: [{id:1, title:...}, ...]     │
└─────────────────────────────────────┘
          ↑
          │ 5. response.json()
          │
┌─────────────────────┐
│  Frontend (app.js)  │
│  renderPeliculas()  │
│  Actualiza DOM      │
└─────────────────────┘
```

---

## 🔄 FLUJO: SINCRONIZAR PELÍCULAS (SYNC) - ADMIN

```
┌─────────────────────────────────┐
│  Admin Panel Frontend            │
│  - Clica "Actualizar desde API externa" │
└─────────────────────────────────┘
          │
        │ 1. POST /api/sync/peliculas
          │    Headers: Authorization: Bearer <token>
        │    Body: vacío
          ↓
┌─────────────────────────────────────────┐
│  Backend (Flask)                        │
│  @app.route('/api/sync/peliculas', ...) │
│  @token_required                        │  ← Verifica JWT
│  @admin_required                        │  ← Verifica rol admin
│  def sincronizar_peliculas_api(current_user): │
└─────────────────────────────────────────┘
          │
        │ 2. Descarga catálogo desde TMDB
        │ 3. Aplica upsert por external_id/source
        │ 4. Actualiza películas, series y sync_state
          ↓
┌──────────────────────────────────────┐
│  SQLite Database (`streamflix.db`)     │
│  INSERT/UPDATE movie                 │
│  INSERT/UPDATE series                │
│  → Catálogo actualizado              │
└──────────────────────────────────────┘
          ↑
        │ 4. Retorna resultado de sincronización
        │    Status: 200 OK
          │
┌────────────────────────────────────┐
│  Frontend                          │
│  - Actualiza tabla de películas    │
│  - Muestra mensaje de éxito        │
│  - Limpia formulario               │
└────────────────────────────────────┘
```

**Nota:** Se han añadido pruebas automáticas (`pytest`) y smoke tests; además la búsqueda de títulos se implementa en el frontend (filtrado client-side sobre `/api/peliculas`). El backend incluye ahora tolerancia al crear índices únicos para evitar fallos en instalaciones con datos históricos duplicados.

---

## 🗑️ FLUJO: ELIMINAR PELÍCULA (DELETE) - ADMIN

```
┌─────────────────────────────┐
│  Admin Panel                │
│  - Clica botón "Eliminar"   │
│    película ID: 5           │
└─────────────────────────────┘
          │
          │ 1. DELETE /api/peliculas/5
          │    Authorization: Bearer <token>
          ↓
┌────────────────────────────────────┐
│  Backend (Flask)                   │
│  @token_required                   │
│  @admin_required                   │
│  def eliminar_pelicula(..., id):   │
└────────────────────────────────────┘
          │
          │ 2. pelicula = Movie.query.get(id)
          │    if not pelicula → 404
          │
          │ 3. db.session.delete(pelicula)
          │    db.session.commit()
          ↓
┌────────────────────────────────────┐
│  SQLite Database (`streamflix.db`)     │
│  DELETE FROM movie WHERE id = 5;   │
│  (Favoritos también eliminados     │
│   por Foreign Key)                 │
└────────────────────────────────────┘
          ↑
          │ 4. Status: 200 OK
          │    {mensaje: "Película eliminada"}
          │
┌─────────────────────────────┐
│  Frontend                   │
│  - Elimina fila de tabla    │
│  - Muestra confirmación     │
└─────────────────────────────┘
```

---

## ❤️ FLUJO: AGREGAR A FAVORITOS

```
┌──────────────────────────────┐
│  Usuario Logueado            │
│  Catálogo de Películas       │
│  Clica ❤️ Favorito Movie ID:2│
└──────────────────────────────┘
          │
          │ 1. POST /api/favoritos
          │    Authorization: Bearer <token>
          │    Body: {movie_id: 2}
          ↓
┌─────────────────────────────────┐
│  Backend (Flask)                │
│  @token_required                │
│  def agregar_favorito():        │
│  - user_id: from JWT token      │
│  - movie_id: from request JSON  │
└─────────────────────────────────┘
          │
          │ 2. Valida película existe
          │    movie = Movie.query.get(2)
          │
          │ 3. Valida no duplicado
          │    existing = Favorite.query
          │      .filter_by(user_id, movie_id)
          │    if existing → 409 Conflict
          │
          │ 4. favorito = Favorite(
          │      user_id=1,
          │      movie_id=2
          │    )
          │    db.session.add(favorito)
          │    db.session.commit()
          ↓
┌──────────────────────────────┐
│  SQLite Database (`streamflix.db`)     │
│  INSERT INTO favorites       │
│  (user_id, movie_id)         │
│  VALUES (1, 2)               │
└──────────────────────────────┘
          ↑
          │ 5. Status: 201 Created
          │    {mensaje: "Agregado a favoritos"}
          │
┌──────────────────────────────┐
│  Frontend                    │
│  - Marca corazón en rojo     │
│  - Confirmación visual       │
│  - Actualiza contador        │
└──────────────────────────────┘
```

---

## 🔐 SEGURIDAD: FLUJO DE CONTRASEÑAS

```
┌──────────────────────┐
│  Usuario ingresa     │
│  contraseña: "abc123"│
└──────────────────────┘
          │
          │ (FRONTEND - client-side validation)
          │ - No vacío
          │ - Mínimo 8 caracteres
          │
          ↓
┌────────────────────────────────────┐
│  POST /api/registro                │
│  JSON: {email, username, password} │
│  (por HTTPS en producción)         │
└────────────────────────────────────┘
          │
          ↓
┌────────────────────────────────────────────┐
│  Backend (Flask) - app.py                  │
│  1. Recibe "abc123"                        │
│  2. salt = bcrypt.gensalt()                │
│     salt = generar valor aleatorio         │
│  3. hash = bcrypt.hashpw(                  │
│      password.encode('utf-8'), salt)       │
│     hash ≠ password (nunca reversible)     │
│  4. Guarda HASH en BD (no contraseña)      │
└────────────────────────────────────────────┘
          │
          ↓
┌────────────────────────────────────────────┐
│  SQLite Database (`streamflix.db`)     │
│  INSERT INTO user                          │
│  password_hash: "$2b$12$R9h/cIPz0... (128) │
│  (nunca la contraseña original)            │
└────────────────────────────────────────────┘
          │ (Posteriormente - Login)
          ↓
┌──────────────────────┐
│  Usuario login       │
│  ingresa: "abc123"   │
└──────────────────────┘
          │
          ↓
┌────────────────────────────────────────────┐
│  Backend (Flask) - app.py                  │
│  1. Busca usuario por email                │
│  2. Obtiene hash guardado de BD            │
│  3. bcrypt.checkpw(                        │
│      "abc123".encode('utf-8'),             │
│      hash_guardado.encode('utf-8')         │
│     )                                      │
│  4. Compara de forma CRIPTOGRAFÍA          │
│  ✓ Si coincide → Login exitoso             │
│  ✗ Si no → Rechaza                         │
└────────────────────────────────────────────┘
          │
          ↓
    ✓ Genera JWT Token (válido 24hs)
    ✗ Error: "Email o contraseña incorrectos"
```

---

## 🎯 DIAGRAMA DE CASOS DE USO

```
                                 ┌─────────────────┐
                                 │    USUARIO      │
                                 └────────┬────────┘
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  │                       │                       │
                  ↓                       ↓                       ↓
            ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
            │  Registrarse│        │ Autenticar  │        │ Ver Películas
            └─────────────┘        │   (Login)   │        └─────────────┘
                  ↓                 └─────────────┘               ↓
                  │                       ↓                       │
      ┌───────────┴───────────┐           │        ┌──────────────┼─────────────┐
      │                       │           │        │              │             │
      ↓                       ↓           ↓        ↓              ↓             ↓
 ┌─────────┐          ┌────────────┐ ┌──────┐ ┌─────────┐ ┌──────────┐ ┌─────────────┐
 │Registrar│          │Validaciones│ │Crear │ │Buscar   │ │Agregar a │ │Ver Detalles │
 │Usuario  │          │de Email    │ │Token │ │Películas│ │Favoritos │ │de Película  │
 │(crear)  │          │Duplicado   │ │ JWT  │ │por      │ │(user)    │ │(user)       │
 │(role:   │          │            │ │      │ │Título  │ │          │ │             │
 │user)    │          │Hashear     │ │      │ │(local) │ └──────────┘ └─────────────┘
 └─────────┘          │Contraseña  │ │      │ │        │
                      │(Bcrypt)    │ │      │ │        │
                      └────────────┘ │      │ └────────┘
                                     └──────┘
                                          │
                                          │ Si role = admin
                                          ↓
                                    ┌─────────────┐
                                    │Gestionar    │
                                    │Películas    │
                                    │(CRUD) Admin │
                                    └──────┬──────┘
                                           │
                            ┌──────────────┼──────────────┐
                            ↓              ↓              ↓
                    ┌────────────┐ ┌────────────┐ ┌────────────┐
                    │ Crear      │ │ Actualizar │ │ Eliminar   │
                    │ Película   │ │ Película   │ │ Película   │
                    │ (admin)    │ │ (admin)    │ │ (admin)    │
                    └────────────┘ └────────────┘ └────────────┘
```

---

## 📦 FLUJO DE DATOS EN UNA PETICIÓN

```
1️⃣  CLIENTE (Browser)
    ┌──────────────────────────────────────┐
    │ const data = {                       │
    │   movie_id: 5,                       │
    │   ...                                │
    │ }                                    │
    │ const token = localStorage.token     │
    └──────────────────────────────────────┘
                    ↓

2️⃣  CONSTRUCCIÓN DE PETICIÓN (fetchAPI)
    ┌──────────────────────────────────────┐
    │ options = {                          │
    │   method: 'POST',                    │
    │   headers: {                         │
    │     'Content-Type': 'application/json',
    │     'Authorization': 'Bearer ' + token
    │   },                                 │
    │   body: JSON.stringify(data)         │
    │ }                                    │
    └──────────────────────────────────────┘
                    ↓

3️⃣  ENVÍO HTTP
    POST http://localhost:5000/api/favoritos
    Content-Type: application/json
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    
    {"movie_id": 5}
                    ↓

4️⃣  SERVIDOR (Flask) - MIDDLEWARE
    ┌──────────────────────────────────────────┐
    │ @token_required                          │
    │ - Extrae token del header                │
    │ - Decodifica JWT                         │
    │ - Obtiene user_id del token              │
    │ - Busca usuario en BD                    │
    │ - Si no existe/token inválido → ERROR    │
    │ - Pasa current_user a la función         │
    └──────────────────────────────────────────┘
                    ↓

5️⃣  SERVIDOR - ENDPOINT
    ┌──────────────────────────────────────────┐
    │ def agregar_favorito(current_user):      │
    │   datos = request.get_json()             │
    │   movie_id = datos['movie_id']           │
    │   user_id = current_user.id              │
    │   - Valida película existe               │
    │   - Valida no está ya en favs            │
    │   - Crea objeto Favorite                 │
    └──────────────────────────────────────────┘
                    ↓

6️⃣  SERVIDOR - ORM (SQLAlchemy)
    ┌──────────────────────────────────────────┐
    │ favorito = Favorite(                     │
    │   user_id=1,                             │
    │   movie_id=5                             │
    │ )                                        │
    │ db.session.add(favorito)                 │
    │ db.session.commit()                      │
    └──────────────────────────────────────────┘
                    ↓

7️⃣  BASE DE DATOS
    INSERT INTO favorites (user_id, movie_id)
    VALUES (1, 5);
                    ↓

8️⃣  RESPUESTA - SERVIDOR
    ┌──────────────────────────────────────────┐
    │ return jsonify({                         │
    │   'mensaje': 'Película agregada...'      │
    │ }), 201                                  │
    │                                          │
    │ Status: 201 Created                      │
    │ Content-Type: application/json           │
    │ Body: {"mensaje": "..."}                 │
    └──────────────────────────────────────────┘
                    ↓

9️⃣  CLIENTE - PROCESAMIENTO
    ┌──────────────────────────────────────────┐
    │ .then(response => response.json())       │
    │ .then(data => {                          │
    │   alert('Agregado a favoritos');         │
    │   // Actualizar UI                       │
    │ })                                       │
    └──────────────────────────────────────────┘
                    ↓

🔟 UI ACTUALIZADA
    ┌──────────────────────────────────────────┐
    │ - Corazón rojo (favorito)                │
    │ - Mensaje de confirmación                │
    │ - Actualizar lista de favoritos          │
    └──────────────────────────────────────────┘
```

---

**Última actualización:** 4 de Abril, 2026

