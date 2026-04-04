/**
 * STREAMFLIX - Single Page Application (SPA)
 * Gestión completa de películas, usuarios y favoritos
 */

// ==================== CONFIG ====================
const API_URL = 'http://localhost:5000/api';
let authToken = 'mock_token'; // Token mock para que funcione sin autenticación real
let currentUser = { id: 1, username: 'usuario_demo', email: 'demo@example.com', role: 'user' };

// ==================== RUTAS SPA ====================
const routes = {
  inicio: 'inicio',
  login: 'login',
  registro: 'registro',
  peliculas: 'peliculas',
  admin: 'admin',
  favoritos: 'favoritos'
};

let currentRoute = routes.inicio;

// ==================== INICIALIZACIÓN ====================
document.addEventListener('DOMContentLoaded', () => {
  renderNavigation();
  // Iniciar directamente en películas (sin login requerido)
  navigateTo(routes.peliculas);
});

// ==================== NAVEGACIÓN ====================
function navigateTo(route) {
  currentRoute = route;
  const content = document.getElementById('content');
  
  if (!content) {
    console.error('Contenedor #content no encontrado');
    return;
  }

  content.innerHTML = '';

  switch (route) {
    case routes.inicio:
      renderInicio();
      break;
    case routes.login:
      renderLogin();
      break;
    case routes.registro:
      renderRegistro();
      break;
    case routes.peliculas:
      if (!authToken) {
        navigateTo(routes.login);
        return;
      }
      renderPeliculas();
      break;
    case routes.admin:
      if (!authToken || currentUser.role !== 'admin') {
        alert('Acceso denegado');
        navigateTo(routes.peliculas);
        return;
      }
      renderAdmin();
      break;
    case routes.favoritos:
      if (!authToken) {
        navigateTo(routes.login);
        return;
      }
      renderFavoritos();
      break;
    default:
      renderInicio();
  }
}

// ==================== RENDERIZACIÓN: NAVEGACIÓN ====================
function renderNavigation() {
  const nav = document.querySelector('nav') || document.createElement('nav');
  nav.className = 'navbar';
  nav.innerHTML = '';

  const logo = document.createElement('div');
  logo.className = 'navbar-logo';
  logo.textContent = '🎬 STREAMFLIX (DEMO)';
  logo.onclick = () => navigateTo(routes.peliculas);
  nav.appendChild(logo);

  const menu = document.createElement('ul');
  menu.className = 'navbar-menu';

  // Modo demo - navegación simplificada
  menu.innerHTML = `
    <li><a href="#" onclick="navigateTo('${routes.peliculas}'); return false;">Películas</a></li>
    <li><a href="#" onclick="navigateTo('${routes.favoritos}'); return false;">❤️ Favoritos</a></li>
    <li><span class="user-info">👤 Modo Demo</span></li>
  `;

  nav.appendChild(menu);

  if (!document.querySelector('nav')) {
    document.body.prepend(nav);
  } else {
    document.querySelector('nav').replaceWith(nav);
  }
}

// ==================== RENDERIZACIÓN: INICIO ====================
function renderInicio() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container inicio-container">
      <div class="welcome-section">
        <h1>🎬 Bienvenido a STREAMFLIX</h1>
        <p>La plataforma de streaming de películas y series más grande del mundo</p>
        <div class="button-group">
          <button class="btn btn-primary" onclick="navigateTo('${routes.login}')">Iniciar Sesión</button>
          <button class="btn btn-secondary" onclick="navigateTo('${routes.registro}')">Crear Cuenta</button>
        </div>
      </div>
    </div>
  `;
}

// ==================== RENDERIZACIÓN: LOGIN ====================
function renderLogin() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container auth-container">
      <div class="auth-form">
        <h2>Iniciar Sesión</h2>
        <form onsubmit="handleLogin(event)">
          <input type="email" id="login-email" placeholder="Email" required>
          <input type="password" id="login-password" placeholder="Contraseña" required>
          <button type="submit" class="btn btn-primary">Entrar</button>
        </form>
        <p>¿No tienes cuenta? <a href="#" onclick="navigateTo('${routes.registro}'); return false;">Regístrate aquí</a></p>
      </div>
    </div>
  `;
}

// ==================== RENDERIZACIÓN: REGISTRO ====================
function renderRegistro() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container auth-container">
      <div class="auth-form">
        <h2>Crear Cuenta</h2>
        <form onsubmit="handleRegistro(event)">
          <input type="text" id="reg-username" placeholder="Nombre de usuario" required>
          <input type="email" id="reg-email" placeholder="Email" required>
          <input type="password" id="reg-password" placeholder="Contraseña" required>
          <input type="password" id="reg-password-confirm" placeholder="Confirmar contraseña" required>
          <button type="submit" class="btn btn-primary">Registrarse</button>
        </form>
        <p>¿Ya tienes cuenta? <a href="#" onclick="navigateTo('${routes.login}'); return false;">Inicia sesión aquí</a></p>
      </div>
    </div>
  `;
}

// ==================== RENDERIZACIÓN: PELÍCULAS ====================
async function renderPeliculas() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container">
      <h2>Nuestro Catálogo</h2>
      <div class="search-bar">
        <input type="text" id="busqueda" placeholder="Buscar película por título..." />
      </div>
      <div id="peliculas-container" class="peliculas-grid"></div>
    </div>
  `;

  // Cargar películas
  const peliculas = await fetchAPI(`${API_URL}/peliculas`, 'GET');
  if (peliculas) {
    renderPeliculasGrid(peliculas);
    setupBusqueda(peliculas);
  }
}

function renderPeliculasGrid(peliculas) {
  const container = document.getElementById('peliculas-container');
  container.innerHTML = '';

  peliculas.forEach(pelicula => {
    const card = document.createElement('div');
    card.className = 'pelicula-card';
    card.innerHTML = `
      <img src="${pelicula.poster_url || 'https://via.placeholder.com/200x300?text=No+Image'}" alt="${pelicula.title}">
      <div class="card-content">
        <h3>${pelicula.title}</h3>
        <p class="genre">${pelicula.genre || 'N/A'}</p>
        <p class="rating">⭐ ${pelicula.rating || 'N/A'}</p>
        <p class="description">${pelicula.description?.substring(0, 80) || ''}...</p>
        <div class="card-buttons">
          <button class="btn btn-small" onclick="mostrarDetalles(${pelicula.id})">Ver Detalles</button>
          <button class="btn btn-small btn-favorite" onclick="toggleFavorito(${pelicula.id})">❤️ Favorito</button>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function setupBusqueda(peliculasOriginales) {
  const input = document.getElementById('busqueda');
  if (input) {
    input.addEventListener('input', (e) => {
      const termino = e.target.value.toLowerCase();
      const filtradas = peliculasOriginales.filter(p => 
        p.title.toLowerCase().includes(termino)
      );
      renderPeliculasGrid(filtradas);
    });
  }
}

// ==================== RENDERIZACIÓN: ADMIN ====================
async function renderAdmin() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container admin-container">
      <h2>⚙️ Panel de Administración</h2>
      <div class="admin-tabs">
        <button class="tab-btn active" onclick="switchTab('lista')">Gestionar Películas</button>
        <button class="tab-btn" onclick="switchTab('crear')">Crear Nueva Película</button>
      </div>
      <div id="admin-content"></div>
    </div>
  `;

  switchTab('lista');
}

async function switchTab(tab) {
  const adminContent = document.getElementById('admin-content');
  
  if (tab === 'lista') {
    adminContent.innerHTML = '<h3>Lista de Películas</h3><div id="admin-movies-list"></div>';
    const peliculas = await fetchAPI(`${API_URL}/peliculas`, 'GET');
    
    let html = '<table class="admin-table"><thead><tr><th>ID</th><th>Título</th><th>Género</th><th>Acciones</th></tr></thead><tbody>';
    peliculas.forEach(p => {
      html += `
        <tr>
          <td>${p.id}</td>
          <td>${p.title}</td>
          <td>${p.genre || 'N/A'}</td>
          <td>
            <button class="btn btn-small btn-warning" onclick="editarPelicula(${p.id})">Editar</button>
            <button class="btn btn-small btn-danger" onclick="eliminarPelicula(${p.id})">Eliminar</button>
          </td>
        </tr>
      `;
    });
    html += '</tbody></table>';
    document.getElementById('admin-movies-list').innerHTML = html;
  } else {
    adminContent.innerHTML = `
      <h3>Crear Nueva Película</h3>
      <form onsubmit="crearPelicula(event)" class="admin-form">
        <input type="text" id="title" placeholder="Título" required>
        <textarea id="description" placeholder="Descripción"></textarea>
        <input type="text" id="director" placeholder="Director">
        <input type="text" id="genre" placeholder="Género">
        <input type="date" id="release_date">
        <input type="number" id="duration_minutes" placeholder="Duración (minutos)">
        <input type="number" id="rating" placeholder="Calificación (0-10)" step="0.1">
        <input type="text" id="poster_url" placeholder="URL del Poster">
        <button type="submit" class="btn btn-primary">Crear Película</button>
      </form>
    `;
  }
}

// ==================== RENDERIZACIÓN: FAVORITOS ====================
async function renderFavoritos() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container">
      <h2>❤️ Mis Películas Favoritas</h2>
      <div id="favoritos-container" class="peliculas-grid"></div>
    </div>
  `;

  const favoritos = await fetchAPI(`${API_URL}/favoritos`, 'GET', null, authToken);
  if (favoritos) {
    renderPeliculasGrid(favoritos);
  }
}

// ==================== FUNCIONES: API CALLS ====================
async function fetchAPI(url, method = 'GET', body = null, token = null) {
  try {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    // No enviar token por ahora (versión simplificada)
    // if (token) {
    //   options.headers['Authorization'] = `Bearer ${token}`;
    // }

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    alert(`Error: ${error.message}`);
    return null;
  }
}

// ==================== FUNCIONES: AUTENTICACIÓN ====================
async function handleLogin(event) {
  event.preventDefault();

  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  const response = await fetchAPI(`${API_URL}/login`, 'POST', { email, password });

  if (response) {
    alert('Login exitoso (modo demo)');
    navigateTo(routes.peliculas);
  }
}

async function handleRegistro(event) {
  event.preventDefault();

  const username = document.getElementById('reg-username').value;
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;
  const passwordConfirm = document.getElementById('reg-password-confirm').value;

  if (password !== passwordConfirm) {
    alert('Las contraseñas no coinciden');
    return;
  }

  const response = await fetchAPI(`${API_URL}/registro`, 'POST', { username, email, password });

  if (response) {
    alert('Registro exitoso (modo demo)');
    navigateTo(routes.login);
  }
}

function logout() {
  alert('Logout (modo demo)');
  navigateTo(routes.inicio);
}

// ==================== FUNCIONES: CRUD DE PELÍCULAS ====================
async function crearPelicula(event) {
  event.preventDefault();

  const pelicula = {
    title: document.getElementById('title').value,
    description: document.getElementById('description').value,
    director: document.getElementById('director').value,
    genre: document.getElementById('genre').value,
    release_date: document.getElementById('release_date').value,
    duration_minutes: parseInt(document.getElementById('duration_minutes').value),
    rating: parseFloat(document.getElementById('rating').value),
    poster_url: document.getElementById('poster_url').value
  };

  const response = await fetchAPI(`${API_URL}/peliculas`, 'POST', pelicula, authToken);
  
  if (response) {
    alert('Película creada exitosamente');
    switchTab('lista');
  }
}

async function editarPelicula(id) {
  alert('Funcionalidad de edición en desarrollo');
}

async function eliminarPelicula(id) {
  if (!confirm('¿Estás seguro de que deseas eliminar esta película?')) return;

  const response = await fetchAPI(`${API_URL}/peliculas/${id}`, 'DELETE', null, authToken);
  
  if (response) {
    alert('Película eliminada');
    switchTab('lista');
  }
}

// ==================== FUNCIONES: FAVORITOS ====================
async function toggleFavorito(movieId) {
  if (!authToken) {
    alert('Debes iniciar sesión para agregar favoritos');
    navigateTo(routes.login);
    return;
  }

  const response = await fetchAPI(`${API_URL}/favoritos`, 'POST', { movie_id: movieId }, authToken);
  
  if (response) {
    alert('Agregado a favoritos');
  }
}

// ==================== FUNCIONES: UTILIDADES ====================
function mostrarDetalles(id) {
  alert(`Detalles de la película ${id} - Funcionalidad en desarrollo`);
}
    contenedor.appendChild(div);

// Función para filtrar películas por título
function filtrarPeliculas(titulo) {
  const filtradas = peliculasOriginal.filter(pelicula =>
    pelicula.titulo.toLowerCase().includes(titulo.toLowerCase())
  );
  renderPeliculas(filtradas);
}
