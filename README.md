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
- ✅ **Módulo de Administración (CRUD):** Panel para administradores con operaciones sobre películas

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
│  ├─ Modelos (User, Movie, Favorite)  │
│  ├─ Endpoints REST                   │
│  └─ Autenticación JWT                │
└─────────────────────────────────────┘
           ↕ SQL
┌─────────────────────────────────────┐
│   BASE DE DATOS (SQLite)             │
│  ├─ user                             │
│  ├─ movie                            │
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

Al iniciar, `app.py` creará `streamflix.db` y, si no hay datos, ejecutará `seed.sql` automáticamente para poblar los usuarios y las películas de ejemplo.

Además, el backend sincroniza películas desde una API externa de forma incremental (upsert) según un intervalo configurable, manteniendo la arquitectura SPA + API REST.

La aplicación estará disponible en: **http://localhost:5000**

> No es necesario servir el frontend por separado. Flask ya entrega `index.html` y `app.js`.

---

## 📡 ENDPOINTS DE LA API

### Autenticación

| Método | Ruta | Descripción | Body |
|--------|------|-------------|------|
| **POST** | `/api/registro` | Registrar usuario | `{email, username, password}` |
| **POST** | `/api/login` | Iniciar sesión | `{email, password}` |

### Películas (CRUD)

| Método | Ruta | Descripción | Autenticación | Body |
|--------|------|-------------|---|------|
| **GET** | `/api/peliculas` | Listar todas | ❌ | - |
| **GET** | `/api/peliculas/<id>` | Obtener por ID | ❌ | - |
| **POST** | `/api/peliculas` | Crear película | ✅ Admin | `{title, description, director, ...}` |
| **PUT** | `/api/peliculas/<id>` | Actualizar película | ✅ Admin | `{title, description, ...}` |
| **DELETE** | `/api/peliculas/<id>` | Eliminar película | ✅ Admin | - |

### Sincronización de Catálogo (API externa)

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---|
| **POST** | `/api/sync/peliculas` | Forzar sincronización externa | ✅ Admin |

### Favoritos

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---|
| **POST** | `/api/favoritos` | Agregar a favoritos | ✅ User |
| **GET** | `/api/favoritos` | Listar mis favoritos | ✅ User |
| **DELETE** | `/api/favoritos/<id>` | Eliminar de favoritos | ✅ User |

---

## 📁 ESTRUCTURA DEL PROYECTO

```
streamflix/
├── app.py                 # Backend Flask (modelos, endpoints, BD)
├── app.js                 # Frontend SPA (Vanilla JS)
├── index.html             # HTML principal (estructura y estilos)
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
1. Una vez autenticado, verá todas las películas
2. Puede buscar por título en tiempo real
3. Puede agregar películas a favoritos

### 4. Gestionar Favoritos
1. Hacer clic en "❤️ Mis Favoritos"
2. Ver películas marcadas como favoritas
3. Agregar o remover películas

### 5. Panel de Administración (solo admins)
1. Ir a "⚙️ Administración"
2. Gestionar películas, actualizar, eliminar
3. Crear nuevas películas con datos completos

---

## 👥 USUARIOS DE PRUEBA

El proyecto incluye usuarios iniciales en `seed.sql`:

- **Administrador**
  - Username: `admin`
  - Email: `admin@example.com`
  - Contraseña: `demo123`
  - Rol: `admin`
  - Puede crear, editar y eliminar películas.

- **Usuario normal**
  - Username: `demo`
  - Email: `demo@example.com`
  - Contraseña: `demo123`
  - Rol: `user`
  - Puede ver películas, iniciar sesión y gestionar favoritos.

> Si el archivo `seed.sql` no está disponible, `app.py` crea un usuario `demo` con rol `admin` como backup.

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
✅ **Roles y permisos** (solo admins pueden gestionar películas)
✅ **Relaciones de BD** con Foreign Keys

---

## 📌 CHECKLIST DE ENTREGA (16 de Abril)

- [x] Esquema de base de datos (usuarios y películas)
- [x] Endpoints REST completos (CRUD)
- [x] Frontend SPA funcional
- [x] Sistema de registro e inicio de sesión
- [x] Gestión de favoritos
- [x] Panel administrativo
- [x] Seguridad (Bcrypt, JWT)
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

**Última actualización:** 4 de Abril, 2026

