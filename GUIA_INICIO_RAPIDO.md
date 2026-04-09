
# 🚀 GUÍA DE INICIO RÁPIDO - STREAMFLIX

Guía paso a paso para tener la aplicación funcionando en 10 minutos.

---

## ⚡ INICIO RÁPIDO (10 minutos)

### Requisitos Mínimos
- Python 3.8+
- SQLite (incluido en Python)
- Git (opcional)

---

## 📍 PASO 1: Configurar Base de Datos (2 min)

La aplicación usa SQLite local por defecto y crea el archivo `streamflix.db` al iniciar.

No necesitas ejecutar comandos de MySQL ni crear la base de datos manualmente.

### Verificación
```bash
python -c "import sqlite3; conn=sqlite3.connect('streamflix.db'); cur=conn.cursor(); cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\''); print(cur.fetchall()); conn.close()"
```

---

## 📍 PASO 2: Configurar Backend y Frontend en un solo servidor (3 min)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar servidor Flask
python app.py
```

### Verificación
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

✅ **App lista en:** `http://localhost:5000`

> No necesitas ejecutar `python -m http.server` ni otro servidor estático.

---

## 🎯 PASO 4: Probar la Aplicación (3 min)

### 1️⃣ Ir a http://localhost:5000

### 2️⃣ Iniciar Sesión con usuarios de prueba
Puedes usar las cuentas incluidas en `seed.sql`:

- **Administrador**
  - Usuario: `admin`
  - Email: `admin@example.com`
  - Contraseña: `demo123`

- **Usuario normal**
  - Usuario: `demo`
  - Email: `demo@example.com`
  - Contraseña: `demo123`

### 3️⃣ Ver Películas
- Verás todas las películas de la BD
- Busca por título en el input
- Clica ❤️ para agregar favoritos

### 4️⃣ Panel Admin (si es admin)
- Ve a "⚙️ Administración"
- Crea, edita o elimina películas

### 4️⃣ Ver Películas
- Verás todas las películas de la BD
- Busca por título en el input
- Clica ❤️ para agregar favoritos

### 5️⃣ Panel Admin (si es admin)
- Ve a "⚙️ Administración"
- Crea, edita o elimina películas

---

## ✅ VERIFICACIÓN RÁPIDA DE LOS ENDPOINTS

### Test con cURL

```bash
# 1. Obtener películas
curl http://localhost:5000/api/peliculas | jq

# 2. Registrar usuario
curl -X POST http://localhost:5000/api/registro \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"test@example.com",
    "password":"test123"
  }' | jq

# 3. Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}' | jq
```

---

## 📁 ESTRUCTURA DE ARCHIVOS FINAL

```
streamflix/
├── app.py                    ✅ Backend Flask (500+ líneas)
├── app.js                    ✅ Frontend SPA (500+ líneas)
├── index.html                ✅ HTML + CSS (700+ líneas)
├── config.py                 ✅ Configuración
├── schema.sql                ✅ Esquema BD
├── seed_data.sql             ✅ Datos de prueba
├── requirements.txt          ✅ Dependencias Python
├── README.md                 ✅ Documentación principal
├── EJEMPLOS_API.md           ✅ Ejemplos de endpoints
├── ARQUITECTURA.md           ✅ Diagramas y flujos
└── GUIA_INICIO_RAPIDO.md     ✅ Este archivo
```

---

## 🐛 TROUBLESHOOTING

### ❌ Error: "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### ❌ Error: "No se puede abrir la base de datos SQLite"

- Verificar que `app.py` está usando la URL de SQLite por defecto
- Asegurarse de que el archivo `streamflix.db` sea legible por el usuario
- Ejecutar `python app.py` y revisar la salida por errores

### ❌ Error: "Access Denied" en SQLite

- El archivo SQLite no usa usuarios ni contraseñas MySQL
- El problema suele ser permiso de archivo o ruta incorrecta
- Verifica que `app.config['SQLALCHEMY_DATABASE_URI']` apunte a `streamflix.db`

### ❌ Error: "CORS error" en el navegador

- Verificar que `Flask-CORS` está instalado
- Verificar que `CORS(app)` está en `app.py`

### ❌ El frontend no se conecta al backend

1. Verificar URLs en `app.js`:
   ```javascript
   const API_URL = '/api';
   ```

2. Verificar que la aplicación está corriendo en http://localhost:5000

3. Verificar en la consola del navegador (F12 → Console)

### ❌ Token JWT inválido

- Limpiar localStorage: `localStorage.clear()`
- Hacer login de nuevo

---

## 📊 CHECKLIST DE ENTREGA (16 de Abril)

### ✅ Backend (app.py)
- [x] Modelos de datos (User, Movie, Favorite)
- [x] Endpoint: POST /api/registro
- [x] Endpoint: POST /api/login
- [x] Endpoint: GET /api/peliculas
- [x] Endpoint: GET /api/peliculas/<id>
- [x] Endpoint: POST /api/peliculas (admin)
- [x] Endpoint: PUT /api/peliculas/<id> (admin)
- [x] Endpoint: DELETE /api/peliculas/<id> (admin)
- [x] Endpoint: POST /api/favoritos (user)
- [x] Endpoint: GET /api/favoritos (user)
- [x] Endpoint: DELETE /api/favoritos/<id> (user)
- [x] Autenticación con JWT
- [x] Autorización por roles
- [x] Hasheo de contraseñas (Bcrypt)
- [x] Manejo de errores
- [x] CORS configurado

### ✅ Base de Datos (schema.sql)
- [x] Tabla `user` con campos correctos
- [x] Tabla `movie` con campos correctos
- [x] Tabla `favorites` con FK
- [x] Índices y constraints
- [x] Timestamps (created_at, updated_at)
- [x] Roles (user, admin)

### ✅ Frontend (app.js + index.html)
- [x] SPA funcional con rutas
- [x] Página de inicio
- [x] Formulario de registro
- [x] Formulario de login
- [x] Listado de películas
- [x] Búsqueda por título (client-side)
- [x] Sistema de favoritos
- [x] Panel administrativo (CRUD)
- [x] Gestión de tokens (localStorage)
- [x] Navbar con navegación
- [x] Diseño responsivo
- [x] Feedback visual (botones, mensajes)

### ✅ Seguridad
- [x] Contraseñas hasheadas con Bcrypt
- [x] Tokens JWT con expiración
- [x] Validación en servidor
- [x] Control de roles y permisos
- [x] CORS restringido a orígenes autorizados
- [x] Manejo de errores sin exponer detalles internos

### ✅ Documentación
- [x] README.md con instrucciones
- [x] EJEMPLOS_API.md con endpoint examples
- [x] ARQUITECTURA.md con diagramas
- [x] schema.sql con comentarios
- [x] Comentarios en código

---

## 🧪 CASOS DE PRUEBA RECOMENDADOS

### Test: Flujo Completo de Usuario

**Scenario 1: Nuevo Usuario**
```
1. Ir a http://localhost:5000
2. Clica "Registrarse"
3. Completa formulario con datos:
   - Username: jose_123
   - Email: jose@example.com
   - Password: MiContra123
4. Clica "Registrarse" → Éxito
5. Redirige a página de login
6. Ingresa credenciales → Login exitoso
7. Ve lista de películas
8. Busca "Matrix" → Filtra correctamente
9. Clica ❤️ en película → Agrega a favoritos
10. Va a "❤️ Mis Favoritos" → Ve película agregada
```

**Scenario 2: Admin User**
```
1. Login como admin
2. Va a "⚙️ Administración"
3. Lee lista de películas
4. Clica "Crear Nueva Película"
5. Completa formulario:
   - Title: Avatar
   - Director: James Cameron
   - Genre: Sci-Fi
   - Rating: 7.8
6. Clica "Crear" → Success
7. Vuelve a "Gestionar Películas"
8. Ve nueva película en tabla
9. Clica "Eliminar" en una película
10. Confirma → Eliminada
```

---

## 🎬 VIDEO DE DEMOSTRACIÓN SUGERIDO

```
Tiempo: 5 minutos

- 0:00-0:30 Mostrar estructura del proyecto
- 0:30-1:00 Explicar arquitectura de 3 capas
- 1:00-1:30 Registrar nuevo usuario
- 1:30-2:00 Login y ver catálogo
- 2:00-3:00 Buscar películas, agregar favoritos
- 3:00-3:30 Panel admininistrativo
- 3:30-4:00 Crear película como admin
- 4:00-4:30 Mostrar BD en SQLite
- 4:30-5:00 Resumen y conclusión
```

---

## 📝 NOTAS IMPORTANTES

1. **Contraseñas en Desarrollo**
   - Usar valores reales pero simples (ej: `admin123`)
   - En producción, usar environment variables

2. **Base de Datos**
   - Para development, SQLite local es la opción predeterminada
   - Para producción, se puede migrar a un servicio relacional en nube

3. **CORS**
   - En la configuración actual no necesitas CORS porque backend y frontend usan el mismo origen (`http://localhost:5000`)
   - En producción, cambiar a dominio real si separas frontend y backend

4. **JWT Secret**
   - Cambiar en `config.py` en producción
   - Usar valor fuerte y único

5. **SSL/TLS**
   - En desarrollo, HTTP está bien
   - En producción, HTTPS obligatorio

---

## 🔗 RECURSOS ÚTILES

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- JWT: https://jwt.io/
- Bcrypt: https://github.com/pyca/bcrypt
- Fetch API: https://developer.mozilla.org/es/docs/Web/API/Fetch_API
- SQLite: https://www.sqlite.org/index.html

---

## 📞 SOPORTE

En caso de errores:

1. Verificar los logs de la consola (F12 en navegador)
2. Verificar los logs del servidor Flask (terminal)
3. Revisar sección TROUBLESHOOTING
4. Consultar la documentación en README.md

---

## ✨ ¡LISTO PARA COMENZAR!

Si todo está funcionando, deberías ver:

✅ Frontend y backend en http://localhost:5000
✅ Base de Datos con datos de prueba
✅ Usuarios registrados
✅ Películas disponibles
✅ Panel administrativo
✅ Sistema de favoritos

**¡A codificar!** 🎬🚀

---

**Última actualización:** 4 de Abril, 2026
**Entrega prevista:** 16 de Abril, 2026
