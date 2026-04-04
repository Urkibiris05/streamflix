/**
 * STREAMFLIX - Single Page Application (SPA)
 * Gestión completa de películas, usuarios y favoritos
 */

// ==================== CONFIG ====================
const API_URL = 'http://localhost:5000/api';
let authToken = localStorage.getItem('authToken') || null;
let currentUser = JSON.parse(localStorage.getItem('currentUser')) || null;

// ==================== RUTAS SPA ====================
const routes = {
  inicio: 'inicio',
  login: 'login',
  registro: 'registro',
  peliculas: 'peliculas',
  admin: 'admin',
  favoritos: 'favoritos'
};
// Variable global para seguir el rastro de los favoritos en el catálogo
let userFavIds = [];
let currentRoute = routes.inicio;

// ==================== INICIALIZACIÓN ====================
document.addEventListener('DOMContentLoaded', () => {
  console.log('App initialized');
  console.log('Stored authToken:', localStorage.getItem('authToken'));
  console.log('Stored currentUser:', localStorage.getItem('currentUser'));

  renderNavigation();

  // Verificar si hay usuario autenticado, si no, ir a login
  if (!authToken || !currentUser) {
    console.log('No authentication found, redirecting to login');
    navigateTo(routes.login);
  } else {
    console.log('User authenticated, redirecting to peliculas');
    navigateTo(routes.peliculas);
  }
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
  logo.textContent = '🎬 STREAMFLIX';
  logo.onclick = () => navigateTo(currentUser ? routes.peliculas : routes.inicio);
  nav.appendChild(logo);

  const menu = document.createElement('ul');
  menu.className = 'navbar-menu';

  if (currentUser) {
    // Usuario autenticado
    menu.innerHTML = `
      <li><a href="#" onclick="navigateTo('${routes.peliculas}'); return false;">Películas</a></li>
      <li><a href="#" onclick="navigateTo('${routes.favoritos}'); return false;">❤️ Favoritos</a></li>
      ${currentUser.role === 'admin' ? `<li><a href="#" onclick="navigateTo('${routes.admin}'); return false;">⚙️ Admin</a></li>` : ''}
      <li><span class="user-info">👤 ${currentUser.username}</span></li>
      <li><a href="#" onclick="logout(); return false;">🚪 Salir</a></li>
    `;
  } else {
    // Usuario no autenticado
    menu.innerHTML = `
      <li><a href="#" onclick="navigateTo('${routes.inicio}'); return false;">Inicio</a></li>
      <li><a href="#" onclick="navigateTo('${routes.login}'); return false;">Iniciar Sesión</a></li>
      <li><a href="#" onclick="navigateTo('${routes.registro}'); return false;">Registrarse</a></li>
    `;
  }

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
        
        <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 8px; margin: 2rem 0; text-align: left; max-width: 500px;">
          <h3 style="color: #667eea; margin-bottom: 1rem;">🚀 Usuario de Prueba</h3>
          <p><strong>Email:</strong> demo@example.com</p>
          <p><strong>Contraseña:</strong> demo123</p>
          <p style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">Este usuario ya tiene algunas películas favoritas para que puedas probar la funcionalidad.</p>
        </div>
        
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
  content.innerHTML = `<div class="container"><h2>Nuestro Catálogo</h2><div id="peliculas-container" class="peliculas-grid"></div></div>`;

  // 1. Obtener favoritos primero para saber qué marcar
  const favoritos = await fetchAPI(`${API_URL}/favoritos`, 'GET', null, authToken);
  userFavIds = favoritos ? favoritos.map(f => f.id) : [];

  // 2. Obtener todas las películas
  const peliculas = await fetchAPI(`${API_URL}/peliculas`, 'GET');
  
  if (peliculas) {
    renderPeliculasGrid(peliculas); 
  }
}

function renderPeliculasGrid(peliculas, containerId = 'peliculas-container') {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '';

  peliculas.forEach(p => {
    const isFav = userFavIds.includes(p.id);
    const card = document.createElement('div');
    card.className = `pelicula-card ${isFav ? 'card-highlight' : ''}`;
    card.style.cursor = 'pointer';
    card.onclick = () => mostrarDetalles(p.id);
    
    card.innerHTML = `
      <img src="${p.poster_url}" alt="${p.title}" style="cursor: pointer;">
      <div class="card-content">
        <h3>${p.title} ${isFav ? '⭐' : ''}</h3> 
        <div class="card-buttons">
          <button class="btn ${isFav ? 'btn-active-fav' : 'btn-favorite'}" onclick="event.stopPropagation(); toggleFavorito(${p.id})">
            ${isFav ? '❤️ Quitar' : '🤍 Favorito'}
          </button>
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
  content.innerHTML = `<div class="container"><h2>❤️ Mis Favoritos</h2><div id="favoritos-container" class="peliculas-grid"></div></div>`;

  const favoritos = await fetchAPI(`${API_URL}/favoritos`, 'GET', null, authToken);
  
  // Forzamos que use el contenedor de favoritos
  if (favoritos && favoritos.length > 0) {
    userFavIds = favoritos.map(f => f.id);
    renderPeliculasGrid(favoritos, 'favoritos-container');
  } else {
    document.getElementById('favoritos-container').innerHTML = "<p>No tienes favoritos.</p>";
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

    // Usar token si está disponible
    if (token || authToken) {
      options.headers['Authorization'] = `Bearer ${token || authToken}`;
    }

    if (body) {
      options.body = JSON.stringify(body);
    }

    console.log('Making API call to:', url, 'with method:', method);
    const response = await fetch(url, options);
    console.log('Response status:', response.status);

    if (!response.ok) {
      let errorMessage = `Error: ${response.status}`;
      try {
        const error = await response.json();
        if (error && error.error) {
          errorMessage = error.error;
        }
      } catch (jsonError) {
        console.warn('No se pudo leer JSON de error', jsonError);
      }
      alert(errorMessage);
      if (response.status === 401) {
        logout();
      }
      return null;
    }

    const data = await response.json();
    console.log('Response data:', data);
    return data;
  } catch (error) {
    console.error('API Error:', error);
    alert('Error al conectar con el servidor. Intenta de nuevo.');
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
    // Guardar token e información del usuario
    authToken = response.token;
    currentUser = response.usuario;

    // Guardar en localStorage
    localStorage.setItem('authToken', authToken);
    localStorage.setItem('currentUser', JSON.stringify(currentUser));

    renderNavigation(); // Actualizar navegación
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
    navigateTo(routes.login);
  }
}

function logout() {
  // Limpiar datos de sesión
  authToken = null;
  currentUser = null;

  // Limpiar localStorage
  localStorage.removeItem('authToken');
  localStorage.removeItem('currentUser');

  renderNavigation(); // Actualizar navegación
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
    switchTab('lista');
  }
}

// ==================== FUNCIONES: FAVORITOS ====================
async function toggleFavorito(movieId) {
  if (!authToken) {
    alert('Necesitas iniciar sesión para agregar favoritos.');
    navigateTo(routes.login);
    return;
  }

  const response = await fetchAPI(`${API_URL}/favoritos`, 'POST', { movie_id: movieId }, authToken);
  
  if (response) {
    const mensaje = response.mensaje || 'Película añadida a favoritos.';
    alert(mensaje);

    // Si estamos en la página de favoritos, actualizar la vista
    if (currentRoute === routes.favoritos) {
      renderFavoritos();
    }

    // Actualizar el botón visualmente
    updateFavoriteButton(movieId);
  }
}

function updateFavoriteButton(movieId) {
  const buttons = document.querySelectorAll(`button[onclick*="toggleFavorito(${movieId})"]`);
  buttons.forEach(button => {
    button.textContent = '❤️ Agregado';
    button.disabled = true;
    button.style.opacity = '0.7';
    setTimeout(() => {
      button.textContent = '❤️ Favorito';
      button.disabled = false;
      button.style.opacity = '1';
    }, 1500);
  });
}

// ==================== FUNCIONES: UTILIDADES ====================
async function mostrarDetalles(id) {
  try {
    console.log(`Obteniendo detalles de película ${id}`);
    const pelicula = await fetchAPI(`${API_URL}/peliculas/${id}`, 'GET');
    
    if (!pelicula || pelicula.error) {
      alert('No se pudieron obtener los detalles de la película');
      return;
    }

    const esFavorito = userFavIds.includes(id);
    const posterUrl = pelicula.poster_url || 'https://via.placeholder.com/300x450?text=No+Image';
    
    const detailsHTML = `
      <div class="movie-detail">
        <div class="movie-poster">
          <img src="${posterUrl}" alt="${pelicula.title}" onerror="this.src='https://via.placeholder.com/300x450?text=No+Image'">
        </div>
        <div class="movie-info">
          <h2>${pelicula.title}</h2>
          
          <div class="movie-meta">
            <div class="meta-item">
              <span class="meta-label">Calificación</span>
              <span class="meta-value rating-large">⭐ ${pelicula.rating || 'N/A'}/10</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Género</span>
              <span class="meta-value">${pelicula.genre || 'No especificado'}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Duración</span>
              <span class="meta-value">${pelicula.duration_minutes ? pelicula.duration_minutes + ' min' : 'No especificada'}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Director</span>
              <span class="meta-value">${pelicula.director || 'No especificado'}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Año de Lanzamiento</span>
              <span class="meta-value">${pelicula.release_date ? pelicula.release_date.slice(0, 4) : 'No especificado'}</span>
            </div>
          </div>

          <h3 style="color: #667eea; margin-top: 1.5rem; margin-bottom: 0.8rem;">Sinopsis</h3>
          <div class="movie-description">
            ${pelicula.description || 'No hay descripción disponible'}
          </div>

          <div class="movie-controls">
            <button class="btn btn-primary" onclick="cerrarDetalles()">Cerrar</button>
            <button class="btn ${esFavorito ? 'btn-danger' : 'btn-favorite'}" onclick="toggleFavorito(${pelicula.id})">
              ${esFavorito ? '❌ Eliminar de Favoritos' : '❤️ Agregar a Favoritos'}
            </button>
          </div>
        </div>
      </div>
    `;

    document.getElementById('movieDetails').innerHTML = detailsHTML;
    document.getElementById('movieModal').classList.add('active');
  } catch (error) {
    console.error('Error al obtener detalles:', error);
    alert('Error al cargar los detalles de la película');
  }
}

function cerrarDetalles() {
  document.getElementById('movieModal').classList.remove('active');
  document.getElementById('movieDetails').innerHTML = '';
}

// Cerrar modal cuando se hace clic fuera del contenido
document.addEventListener('click', (e) => {
  const modal = document.getElementById('movieModal');
  if (e.target === modal) {
    cerrarDetalles();
  }
});
