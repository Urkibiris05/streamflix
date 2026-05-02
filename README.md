# 🎬 STREAMFLIX - Single Page Application (SPA)

Plataforma de streaming de películas y series con arquitectura de tres capas (Frontend, Backend, Base de Datos).

**Fecha de Entrega:** 16 de Abril, 2026

---

## 📋 ÍNDICE

1. [Requisitos del Proyecto](#requisitos-del-proyecto)
2. [Arquitectura](#arquitectura)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Endpoints de la API](#endpoints-de-la-api)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Guía de Uso](#guía-de-uso)
7. [Stack Tecnológico](#stack-tecnológico)

---

## ✅ REQUISITOS DEL PROYECTO

### 1. Arquitectura y Estructura
- ✅ **Frontend (SPA):** Gestión de interfaz y rutas del lado del cliente
- ✅ **Backend (API REST):** Lógica de negocio robusta
- ✅ **Persistencia:** Sistema de almacenamiento con SQLite local

### 2. Funcionalidades Requeridas
- ✅ **Sistema de Registro:** Flujo completo de registro de usuarios
- ✅ **Módulo de Administración (CRUD):** Panel para administradores con operaciones sobre películas y series

---

## 🏗️ ARQUITECTURA

### Diagrama de Capas

```
┌─────────────────────────────────────┐
│   FRONTEND (SPA - Vanilla JS)        │
│  ├─ index.html                       │
│  ├─ app.js                           │
│  └─ Gestión de rutas y UI            │
└─────────────────────────────────────┘
           ↕ HTTP/REST
┌─────────────────────────────────────┐
│   BACKEND (Flask + SQLAlchemy)       │
│  ├─ app.py                           │
│  ├─ Modelos (User, Movie, Series,    │
│  │   Episode, Reviews, SyncState)     │
│  ├─ Endpoints REST                   │
│  └─ Autenticación JWT                │
└─────────────────────────────────────┘
           ↕ SQL
┌─────────────────────────────────────┐
│   BASE DE DATOS (SQLite)             │
│  ├─ user                             │
│  ├─ movie                            │
│  ├─ series                           │
│  ├─ episode                          │
│  └─ favorites                        │
└─────────────────────────────────────┘
```

---

## 🚀 INSTALACIÓN Y CONFIGURACIÓN

### Requisitos Previos
- Python 3.8+
- SQLite (incluido en Python)
- Node.js (opcional, para servir archivos estáticos)

### Paso 1: Clonar el Repositorio
```bash
cd streamflix
```

### Paso 2: Inicializar la Base de Datos
El backend usa SQLite por defecto y crea el archivo local `streamflix.db` automáticamente la primera vez que se ejecuta.

Si deseas revisar la estructura, `schema.sql` contiene el esquema de tablas usado por el proyecto.


### Paso 3: Configurar el Backend
```bash
# Instalar dependencias de Python
pip install -r requirements.txt
```

El backend está configurado por defecto para usar SQLite local:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'streamflix.db')}"
```

Si deseas usar MySQL, cambia esta línea por la URI de tu servidor.

### Paso 4: Iniciar el Backend y el Frontend
```bash
python app.py
```

Al iniciar, `app.py` crea `streamflix.db`, prepara usuarios base si la BD está vacía, limpia el contenido local que no proviene de TMDB y sincroniza automáticamente el catálogo de películas y series desde la API externa.

El archivo `seed.sql` sigue en el proyecto como referencia histórica y para pruebas locales, pero ya no se usa para poblar el catálogo visible en el arranque normal.

Además, el backend sincroniza películas y series desde TMDB de forma incremental (upsert) según un intervalo configurable, manteniendo la arquitectura SPA + API REST.

La aplicación estará disponible en: **http://localhost:5000**

> No es necesario servir el frontend por separado. Flask ya entrega `index.html` y `app.js`.

### Verificación rápida completa
```bash
python smoke_test_streamflix.py

# Para incluir borrado/restauración controlada:
python smoke_test_streamflix.py --destructive
```

---

## 📡 ENDPOINTS DE LA API

### Autenticación

| Método | Ruta | Descripción | Body |
|--------|------|-------------|------|
| **POST** | `/api/registro` | Registrar usuario | `{email, username, password}` |
| **POST** | `/api/login` | Iniciar sesión | `{email, password}` |

### Películas

| Método | Ruta | Descripción | Autenticación | Body |
|--------|------|-------------|---|------|
| **GET** | `/api/peliculas` | Listar sincronizadas | ❌ | - |
| **GET** | `/api/peliculas/<id>` | Obtener por ID | ❌ | - |
| **POST** | `/api/peliculas` | Crear manual deshabilitado | ✅ Admin | Devuelve `403` |
| **PUT** | `/api/peliculas/<id>` | Editar manual deshabilitado | ✅ Admin | Devuelve `403` |
| **DELETE** | `/api/peliculas/<id>` | Eliminar sincronizada | ✅ Admin | - |

### Sincronización de Catálogo (API externa)

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---|
| **POST** | `/api/sync/peliculas` | Forzar sincronización externa | ✅ Admin |

### Series

| Método | Ruta | Descripción | Autenticación | Body |
|--------|------|-------------|---|------|
| **GET** | `/api/series` | Listar sincronizadas | ❌ | - |
| **GET** | `/api/series/<id>` | Obtener por ID | ❌ | - |
| **POST** | `/api/series` | Crear manual deshabilitado | ✅ Admin | Devuelve `403` |
| **PUT** | `/api/series/<id>` | Editar manual deshabilitado | ✅ Admin | Devuelve `403` |
| **DELETE** | `/api/series/<id>` | Eliminar sincronizada | ✅ Admin | - |

### Sincronización de Series

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---|
| **POST** | `/api/sync/series` | Forzar sincronización de series | ✅ Admin |

### Favoritos

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---|
| **POST** | `/api/favoritos` | Agregar a favoritos | ✅ User |
| **GET** | `/api/favoritos` | Listar mis favoritos | ✅ User |
| **DELETE** | `/api/favoritos/<id>` | Eliminar de favoritos | ✅ User |

### Favoritos de Series

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---|
| **POST** | `/api/series-favoritos` | Agregar serie a favoritos | ✅ User |
| **GET** | `/api/series-favoritos` | Listar mis series favoritas | ✅ User |
| **DELETE** | `/api/series-favoritos/<id>` | Eliminar serie de favoritos | ✅ User |

### Reviews

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---|
| **GET** | `/api/peliculas/<id>/reviews` | Reviews de película | ❌ |
| **GET** | `/api/peliculas/<id>/average-rating` | Rating promedio de película | ❌ |
| **POST** | `/api/reviews` | Crear review de película | ✅ User |
| **DELETE** | `/api/reviews/<id>` | Eliminar review propia de película | ✅ User |
| **GET** | `/api/series/<id>/reviews` | Reviews de serie | ❌ |
| **GET** | `/api/series/<id>/average-rating` | Rating promedio de serie | ❌ |
| **POST** | `/api/series/reviews` | Crear review de serie | ✅ User |
| **DELETE** | `/api/series/reviews/<id>` | Eliminar review propia de serie | ✅ User |

---

## 📁 ESTRUCTURA DEL PROYECTO

```
streamflix/
├── app.py                 # Backend Flask (modelos, endpoints, BD)
├── app.js                 # Frontend SPA (Vanilla JS)
├── index.html             # HTML principal (estructura y estilos)
├── seed.sql               # Seed legado / referencia histórica
├── seed_data.sql          # Datos de prueba históricos
├── smoke_test_streamflix.py # Smoke test funcional
├── schema.sql             # Script de creación de BD
├── requirements.txt       # Dependencias de Python
├── models.py              # Modelos de datos (opcional)
└── README.md              # Documentación
```

---

## 📝 ESQUEMA DE BASE DE DATOS

### Tabla: `user`
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(120) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: `movie`
```sql
CREATE TABLE movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    director VARCHAR(255),
    genre VARCHAR(100),
    release_date DATE,
    duration_minutes INTEGER,
    rating REAL,
    poster_url VARCHAR(500),
    video_url VARCHAR(500),
    external_id VARCHAR(120),
    source VARCHAR(50) DEFAULT 'local',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: `series`
```sql
CREATE TABLE series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    director VARCHAR(255),
    genre VARCHAR(100),
    release_date DATE,
    poster_url VARCHAR(500),
    external_id VARCHAR(120),
    source VARCHAR(50) DEFAULT 'local',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: `episode`
```sql
CREATE TABLE episode (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    season INTEGER NOT NULL,
    episode_number INTEGER NOT NULL,
    air_date DATE,
    duration_minutes INTEGER,
    video_url VARCHAR(500),
    external_id VARCHAR(120),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE
);
```

### Tabla: `favorites`
```sql
CREATE TABLE favorites (
    movie_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (movie_id, user_id),
    FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);
```

### Tabla: `series_favorites`
```sql
CREATE TABLE series_favorites (
    series_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (series_id, user_id),
    FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);
```

---

## 🎯 GUÍA DE USO

### 1. Registro de Usuario
1. Ir a la página de inicio
2. Hacer clic en "Registrarse"
3. Completar formulario (username, email, password)
4. Se registrará y podrá iniciar sesión

### 2. Iniciar Sesión
1. Hacer clic en "Login"
2. Ingresar email y contraseña
3. Se redirigirá al catálogo de películas

### 3. Ver Catálogo de Películas
1. Una vez autenticado, verá el catálogo sincronizado desde TMDB
2. Puede alternar entre Películas y Series con las pestañas superiores
3. Puede buscar por título en tiempo real
4. Puede agregar películas y series a favoritos

### 4. Gestionar Favoritos
1. Hacer clic en "❤️ Mis Favoritos"
2. Ver películas marcadas como favoritas
3. Cambiar a series favoritas desde su sección correspondiente
4. Agregar o remover elementos

### 5. Panel de Administración (solo admins)
1. Ir a "⚙️ Administración"
2. Alternar entre "Gestionar Películas" y "Gestionar Series"
3. Sincronizar catálogo desde TMDB o eliminar elementos sincronizados

---

## 👥 USUARIOS DE PRUEBA

El proyecto incluye usuarios base creados automáticamente al arrancar si la BD está vacía:

- **Administrador**
  - Username: `admin`
  - Email: `admin@example.com`
  - Contraseña: `demo123`
  - Rol: `admin`
  - Puede crear, editar y eliminar películas.

**Usuario normal**
  - Username: `demo`
  - Email: `demo@example.com`
  - Contraseña: `demo123`
  - Rol: `user`
  - Puede ver el catálogo, iniciar sesión y gestionar favoritos.

> `seed.sql` sigue disponible como referencia de datos históricos y pruebas, pero ya no se usa para poblar el catálogo visible en el arranque normal.

---

## 🔄 SINCRONIZACIÓN AUTOMÁTICA DE PELÍCULAS

El backend descarga películas desde una API externa y las inserta/actualiza en SQLite sin duplicados.

La aplicación carga automáticamente un archivo `.env` ubicado en la raíz del proyecto, así que puedes definir ahí `TMDB_API_KEY` y el resto de variables.

Variables de entorno opcionales:

- `MOVIES_PROVIDER_SOURCE` (default: `tmdb`)
- `TMDB_BASE_URL` (default: `https://api.themoviedb.org/3`)
- `TMDB_API_KEY` (required para usar TMDB)
- `TMDB_LANGUAGE` (default: `es-ES`)
- `TMDB_MAX_PAGES` (default: `3`)
- `TMDB_IMAGE_BASE_URL` (default: `https://image.tmdb.org/t/p/w500`)
- `OMDB_PROVIDER_URL` (default: `https://www.omdbapi.com/`)
- `OMDB_API_KEY` (default: `thewdb`)
- `OMDB_RECENT_YEARS` (default: `3`)
- `OMDB_MAX_PAGES_PER_QUERY` (default: `2`)
- `OMDB_MAX_TITLES` (default: `120`)
- `GHIBLI_PROVIDER_URL` (default: `https://ghibliapi.vercel.app/films`)
- `MOVIES_SYNC_INTERVAL_MINUTES` (default: `60`)
- `MOVIES_SYNC_MAX_PAGES` (default: `2`)
- `MOVIES_SYNC_PAGE_LIMIT` (default: `50`)
- `MOVIES_PROVIDER_TIMEOUT_SECONDS` (default: `8`)
- `MOVIES_AUTO_SYNC_ON_READ` (default: `true`)

Con `MOVIES_AUTO_SYNC_ON_READ=true`, cada `GET /api/peliculas` intenta sincronizar si ya venció el intervalo configurado.

Si `TMDB_API_KEY` no está configurada o TMDB no responde, el backend aplica fallback automático a OMDb para mantener el catálogo actualizado.

Consulta `.env.example` para ver un ejemplo completo de configuración.

## 🔄 SINCRONIZACIÓN AUTOMÁTICA DE SERIES

Las series siguen el mismo patrón de TMDB, con sus propias variables de entorno:

- `SERIES_PROVIDER_SOURCE` (default: `tmdb`)
- `SERIES_PROVIDER_TIMEOUT_SECONDS` (default: `8`)
- `SERIES_SYNC_INTERVAL_MINUTES` (default: `120`)
- `SERIES_SYNC_MAX_PAGES` (default: `2`)
- `SERIES_AUTO_SYNC_ON_READ` (default: `true`)

La sincronización manual se expone en `POST /api/sync/series` y también se ejecuta al iniciar la aplicación.

---

## 🛠️ STACK TECNOLÓGICO

### Frontend
- **Vanilla JavaScript (ES6+):** Sin frameworks, código limpio y eficiente
- **HTML5:** Estructura semántica
- **CSS3:** Diseño responsivo con gradientes y animaciones

### Backend
- **Flask:** Framework web ligero y poderoso
- **SQLAlchemy:** ORM para manejo de base de datos
- **Bcrypt:** Hasheo seguro de contraseñas
- **PyJWT:** Tokens JWT para autenticación
- **Flask-CORS:** Control de CORS para peticiones del frontend

### Base de Datos
- **SQLite:** Base de datos local integrada en Python
- **sqlite3:** Conector interno de Python para el archivo `streamflix.db`

### Autenticación y Seguridad
- **Bcrypt:** Hash seguro de contraseñas
- **JWT (JSON Web Tokens):** Autenticación stateless
- **Roles:** Sistema de roles (user, admin)

---

## 🔒 Seguridad Implementada

✅ **Contraseñas hasheadas** con Bcrypt (nunca en texto plano)
✅ **Tokens JWT** con expiración de 24 horas
✅ **Validación de inputs** en servidor y cliente
✅ **CORS configurado** para evitar accesos no autorizados
✅ **Roles y permisos** (solo admins pueden gestionar el catálogo)
✅ **Relaciones de BD** con Foreign Keys

---

## 📌 CHECKLIST DE ENTREGA (16 de Abril)

- [x] Esquema de base de datos (usuarios y películas)
- [x] Endpoints REST completos (CRUD)
- [x] Frontend SPA funcional
- [x] Sistema de registro e inicio de sesión
- [x] Gestión de favoritos de películas y series
- [x] Panel administrativo con pestañas y sincronización TMDB
- [x] Seguridad (Bcrypt, JWT)
- [x] Sincronización TMDB (películas y series)
- [x] Smoke test funcional automatizado
- [x] Documentación completa

---

## 🐛 Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "No se puede abrir la base de datos SQLite"
- Verificar que `app.py` puede crear y leer `streamflix.db`
- Ejecutar `python app.py` y revisar la salida por errores
- Asegurarse de que `app.config['SQLALCHEMY_DATABASE_URI']` apunte a `sqlite:///streamflix.db`

### Error: CORS en el frontend
- Verificar que Flask-CORS está instalado
- Verificar que `CORS(app)` está en `app.py`

### Error: "Token inválido"
- Verificar que el token se está enviando en el header: `Authorization: Bearer <token>`
- Verificar que la SESSION_SECRET es la misma en frontend y backend

---

## 📞 Soporte

Para reportar issues o sugerencias, contactar al equipo de desarrollo.

---

**Última actualización:** 2 de Mayo, 2026

