/**
 * STREAMFLIX - Single Page Application (SPA)
 * Gestión completa de películas, usuarios y favoritos
 */

// ==================== CONFIG ====================
const API_URL = '/api';
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
let userFavSeriesIds = [];
let currentRoute = routes.inicio;
let currentContentType = 'peliculas'; // 'peliculas' o 'series'
let peliculasData = [];
let seriesData = [];

// ==================== INICIALIZACIÓN ====================
document.addEventListener('DOMContentLoaded', () => {
  console.log('App initialized');
  console.log('API URL:', API_URL);
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
      <li><a href="#" onclick="navigateTo('${routes.peliculas}'); return false;">Catálogo</a></li>
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
        
        <!-- <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 8px; margin: 2rem 0; text-align: left; max-width: 500px;"> -->
          <!-- <h3 style="color: #667eea; margin-bottom: 1rem;">🚀 Usuario de Prueba</h3> -->
          <!-- <p><strong>Email:</strong> demo@example.com</p> -->
          <!-- <p><strong>Contraseña:</strong> demo123</p> -->
          <!-- <p style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">Este usuario ya tiene algunas películas favoritas para que puedas probar la funcionalidad.</p> -->
        <!-- </div> -->
        
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
      <div class="catalog-tabs">
        <button class="tab-btn active" id="tab-peliculas" onclick="switchContentType('peliculas')">🎬 Películas</button>
        <button class="tab-btn" id="tab-series" onclick="switchContentType('series')">📺 Series</button>
      </div>
      <div id="content-type-container"></div>
    </div>
  `;

  // 1. Obtener favoritos (películas y series)
  const favoritosPeliculas = await fetchAPI(`${API_URL}/favoritos`, 'GET', null, authToken);
  const favoritosSeries = await fetchAPI(`${API_URL}/series-favoritos`, 'GET', null, authToken);
  
  userFavIds = favoritosPeliculas ? favoritosPeliculas.map(f => f.id) : [];
  userFavSeriesIds = favoritosSeries ? favoritosSeries.map(s => s.id) : [];

  // 2. Obtener películas y series
  peliculasData = await fetchAPI(`${API_URL}/peliculas`, 'GET');
  seriesData = await fetchAPI(`${API_URL}/series`, 'GET');
  
  // 3. Mostrar contenido por defecto (películas)
  currentContentType = 'peliculas';
  switchContentType('peliculas');
}

async function switchContentType(type) {
  currentContentType = type;
  
  // Actualizar botones activos
  document.getElementById('tab-peliculas').classList.toggle('active', type === 'peliculas');
  document.getElementById('tab-series').classList.toggle('active', type === 'series');
  
  const container = document.getElementById('content-type-container');
  
  if (type === 'peliculas') {
    renderPeliculasSection();
  } else if (type === 'series') {
    renderSeriesSection();
  }
}

function renderPeliculasSection() {
  let contenido = '';
  
  if (peliculasData && peliculasData.length > 0) {
    contenido = '<div class="peliculas-grid">';
    peliculasData.forEach(p => {
      contenido += renderPeliculaCard(p, 'pelicula');
    });
    contenido += '</div>';
  } else {
    contenido = '<p>No hay películas disponibles.</p>';
  }
  
  document.getElementById('content-type-container').innerHTML = contenido;
}

function renderSeriesSection() {
  let contenido = '';
  
  if (seriesData && seriesData.length > 0) {
    contenido = '<div class="peliculas-grid">';
    seriesData.forEach(s => {
      contenido += renderSerieCard(s);
    });
    contenido += '</div>';
  } else {
    contenido = '<p>No hay series disponibles.</p>';
  }
  
  document.getElementById('content-type-container').innerHTML = contenido;
}

function renderPeliculaCard(p, type = 'pelicula') {
  const isFav = userFavIds.includes(p.id);
  return `
    <div class="pelicula-card ${isFav ? 'card-highlight' : ''}" style="cursor: pointer;" onclick="mostrarDetalles('${type}', ${p.id})">
      <img src="${p.poster_url}" alt="${p.title}" style="cursor: pointer;">
      <div class="card-content">
        <h3>${p.title} ${isFav ? '⭐' : ''}</h3> 
        <div class="card-buttons">
          <button class="btn ${isFav ? 'btn-active-fav' : 'btn-favorite'}" onclick="event.stopPropagation(); toggleFavorito('pelicula', ${p.id})">
            ${isFav ? '❤️ Quitar' : '🤍 Favorito'}
          </button>
        </div>
      </div>
    </div>
  `;
}

function renderSerieCard(s) {
  const isFav = userFavSeriesIds.includes(s.id);
  return `
    <div class="pelicula-card ${isFav ? 'card-highlight' : ''}" style="cursor: pointer; border: 2px solid #ff6b9d;" onclick="mostrarDetalles('serie', ${s.id})">
      <div style="position: relative;">
        <img src="${s.poster_url}" alt="${s.title}" style="cursor: pointer;">
        <span style="position: absolute; top: 8px; right: 8px; background: #ff6b9d; color: white; padding: 0.3rem 0.6rem; border-radius: 4px; font-size: 0.8rem; font-weight: bold;">SERIE</span>
      </div>
      <div class="card-content">
        <h3>${s.title} ${isFav ? '⭐' : ''}</h3> 
        <div class="card-buttons">
          <button class="btn ${isFav ? 'btn-active-fav' : 'btn-favorite'}" onclick="event.stopPropagation(); toggleFavorito('serie', ${s.id})">
            ${isFav ? '❤️ Quitar' : '🤍 Favorito'}
          </button>
        </div>
      </div>
    </div>
  `;
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
        <input type="text" id="video_url" placeholder="URL del Video (opcional)">
        <button type="submit" class="btn btn-primary">Crear Película</button>
      </form>
      <div id="create-result" class="create-result"></div>
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
      mode: 'cors',
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
    duration_minutes: document.getElementById('duration_minutes').value,
    rating: document.getElementById('rating').value,
    poster_url: document.getElementById('poster_url').value,
    video_url: document.getElementById('video_url').value
  };

  const response = await fetchAPI(`${API_URL}/peliculas`, 'POST', pelicula, authToken);
  
  if (response) {
    console.log('Película creada:', response.pelicula);
    const resultDiv = document.getElementById('create-result');
    if (resultDiv) {
      resultDiv.innerHTML = mostrarPeliculaCreada(response.pelicula);
    }
    switchTab('lista');
  }
}

function mostrarPeliculaCreada(pelicula) {
  return `
    <div class="created-movie-card">
      <h4>Película creada con éxito</h4>
      <p><strong>ID:</strong> ${pelicula.id}</p>
      <p><strong>Título:</strong> ${pelicula.title}</p>
      <p><strong>Género:</strong> ${pelicula.genre || 'N/A'}</p>
      <p><strong>Fecha de estreno:</strong> ${pelicula.release_date || 'N/A'}</p>
      <p><strong>Duración:</strong> ${pelicula.duration_minutes ? pelicula.duration_minutes + ' min' : 'N/A'}</p>
      <p><strong>Rating:</strong> ${pelicula.rating || 'N/A'}/10</p>
      <p><strong>Poster URL:</strong> ${pelicula.poster_url || 'N/A'}</p>
      <p><strong>Video URL:</strong> ${pelicula.video_url || 'N/A'}</p>
      <p><strong>Created at:</strong> ${pelicula.created_at || 'N/A'}</p>
      <p><strong>Updated at:</strong> ${pelicula.updated_at || 'N/A'}</p>
    </div>
  `;
}

async function editarPelicula(id) {
  const pelicula = await fetchAPI(`${API_URL}/peliculas/${id}`, 'GET');
  if (!pelicula) return;

  const adminContent = document.getElementById('admin-content');
  adminContent.innerHTML = `
    <h3>Editar Película</h3>
    <form onsubmit="actualizarPelicula(event, ${id})" class="admin-form">
      <input type="text" id="edit-title" placeholder="Título" value="${pelicula.title || ''}" required>
      <textarea id="edit-description" placeholder="Descripción">${pelicula.description || ''}</textarea>
      <input type="text" id="edit-director" placeholder="Director" value="${pelicula.director || ''}">
      <input type="text" id="edit-genre" placeholder="Género" value="${pelicula.genre || ''}">
      <input type="date" id="edit-release_date" value="${pelicula.release_date || ''}">
      <input type="number" id="edit-duration_minutes" placeholder="Duración (minutos)" value="${pelicula.duration_minutes || ''}">
      <input type="number" id="edit-rating" placeholder="Calificación (0-10)" step="0.1" value="${pelicula.rating || ''}">
      <input type="text" id="edit-poster_url" placeholder="URL del Poster" value="${pelicula.poster_url || ''}">
      <input type="text" id="edit-video_url" placeholder="URL del Video (opcional)" value="${pelicula.video_url || ''}">
      <button type="submit" class="btn btn-primary">Guardar Cambios</button>
      <button type="button" class="btn btn-secondary" onclick="switchTab('lista')">Volver a la lista</button>
    </form>
    <div id="edit-result" class="create-result"></div>
  `;
}

async function actualizarPelicula(event, id) {
  event.preventDefault();

  const pelicula = {
    title: document.getElementById('edit-title').value,
    description: document.getElementById('edit-description').value,
    director: document.getElementById('edit-director').value,
    genre: document.getElementById('edit-genre').value,
    release_date: document.getElementById('edit-release_date').value,
    duration_minutes: document.getElementById('edit-duration_minutes').value,
    rating: document.getElementById('edit-rating').value,
    poster_url: document.getElementById('edit-poster_url').value,
    video_url: document.getElementById('edit-video_url').value
  };

  const response = await fetchAPI(`${API_URL}/peliculas/${id}`, 'PUT', pelicula, authToken);
  if (response) {
    const resultDiv = document.getElementById('edit-result');
    if (resultDiv) {
      resultDiv.innerHTML = mostrarPeliculaCreada(response.pelicula).replace('Película creada con éxito', 'Película actualizada con éxito');
    }
    setTimeout(() => switchTab('lista'), 1200);
  }
}

async function eliminarPelicula(id) {
  if (!confirm('¿Estás seguro de que deseas eliminar esta película?')) return;

  const response = await fetchAPI(`${API_URL}/peliculas/${id}`, 'DELETE', null, authToken);
  
  if (response) {
    switchTab('lista');
  }
}

// ==================== FUNCIONES: FAVORITOS ====================
async function toggleFavorito(type, itemId) {
  if (!authToken) {
    alert('Necesitas iniciar sesión para agregar favoritos.');
    navigateTo(routes.login);
    return;
  }

  const endpoint = type === 'serie' ? '/api/series-favoritos' : '/api/favoritos';
  const body = type === 'serie' 
    ? { series_id: itemId }
    : { movie_id: itemId };

  const response = await fetchAPI(`${API_URL}${endpoint}`, 'POST', body, authToken);
  
  if (response) {
    const mensaje = response.mensaje || 'Agregado a favoritos.';
    alert(mensaje);

    // Actualizar el array de favoritos
    if (type === 'serie') {
      if (!userFavSeriesIds.includes(itemId)) {
        userFavSeriesIds.push(itemId);
      }
    } else {
      if (!userFavIds.includes(itemId)) {
        userFavIds.push(itemId);
      }
    }

    // Si estamos en la página de favoritos, actualizar la vista
    if (currentRoute === routes.favoritos) {
      renderFavoritos();
    }
  }
}

// ==================== FUNCIONES: UTILIDADES ====================
async function mostrarDetalles(type, id) {
  try {
    if (type === 'serie') {
      await mostrarDetallesSerie(id);
    } else {
      await mostrarDetallesPelicula(id);
    }
  } catch (error) {
    console.error('Error al obtener detalles:', error);
    alert('Error al cargar los detalles');
  }
}

async function mostrarDetallesPelicula(id) {
  try {
    console.log(`Obteniendo detalles de película ${id}`);
    const pelicula = await fetchAPI(`${API_URL}/peliculas/${id}`, 'GET');
    
    if (!pelicula || pelicula.error) {
      alert('No se pudieron obtener los detalles de la película');
      return;
    }

    // Obtener críticas y rating promedio
    const reviews = await fetchAPI(`${API_URL}/peliculas/${id}/reviews`, 'GET');
    const ratingData = await fetchAPI(`${API_URL}/peliculas/${id}/average-rating`, 'GET');
    
    const esFavorito = userFavIds.includes(id);
    const posterUrl = pelicula.poster_url || 'https://via.placeholder.com/300x450?text=No+Image';
    
    // Verificar si el usuario ya tiene una crítica para esta película
    const userReview = reviews && reviews.find(r => r.user_id === currentUser?.id);
    
    let detailsHTML = `
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
            <button class="btn ${esFavorito ? 'btn-danger' : 'btn-favorite'}" onclick="toggleFavorito('pelicula', ${pelicula.id})">
              ${esFavorito ? '❌ Eliminar de Favoritos' : '❤️ Agregar a Favoritos'}
            </button>
          </div>
        </div>
      </div>

      <!-- SECCIÓN DE CRÍTICAS Y RATINGS -->
      <div class="reviews-section" style="margin-top: 2rem; padding: 1.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px;">
        <h3 style="color: #667eea; margin-bottom: 1rem;">⭐ Críticas y Calificaciones</h3>
        
        <!-- Rating Promedio -->
        <div class="rating-summary" style="background: white; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem; text-align: center;">
          <div style="font-size: 2rem; font-weight: bold; color: #667eea;">
            ${ratingData ? ratingData.average_rating : '0.00'}/10
          </div>
          <p style="color: #666; margin: 0.5rem 0 0 0;">
            Basado en ${ratingData ? ratingData.total_reviews : '0'} crítica${ratingData && ratingData.total_reviews !== 1 ? 's' : ''}
          </p>
        </div>

        <!-- Formulario para crear crítica -->
        ${authToken ? `
          <div id="create-review-form" style="background: white; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
            ${userReview ? `
              <p style="color: #667eea; font-weight: bold; margin-bottom: 1rem;">Tu crítica:</p>
            ` : `
              <h4 style="margin-top: 0; color: #333;">Escribe tu crítica</h4>
            `}
            <form onsubmit="crearOEditarReview(event, ${id}, ${userReview ? userReview.id : 'null'})" style="display: flex; flex-direction: column; gap: 0.8rem;">
              <div>
                <label style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500;">Calificación (1-10):</label>
                <input 
                  type="number" 
                  id="review-rating" 
                  min="1" 
                  max="10" 
                  placeholder="Ej: 8"
                  value="${userReview ? userReview.rating : ''}"
                  required
                  style="width: 100%; padding: 0.6rem; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;"
                >
              </div>
              <div>
                <label style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500;">Tu crítica (opcional):</label>
                <textarea 
                  id="review-text" 
                  placeholder="Comparte tu opinión sobre esta película..."
                  style="width: 100%; padding: 0.6rem; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-family: inherit; font-size: 0.95rem; min-height: 80px; resize: vertical;"
                >${userReview ? (userReview.review_text || '') : ''}</textarea>
              </div>
              <div style="display: flex; gap: 0.8rem;">
                <button type="submit" class="btn btn-primary" style="flex: 1;">
                  ${userReview ? '✏️ Actualizar crítica' : '➕ Enviar crítica'}
                </button>
                ${userReview ? `
                  <button type="button" class="btn btn-danger" onclick="eliminarReview(${userReview.id}, ${id})" style="flex: 1;">
                    🗑️ Eliminar mi crítica
                  </button>
                ` : ''}
              </div>
            </form>
          </div>
        ` : `
          <div style="background: #fff3cd; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem; color: #856404;">
            <p style="margin: 0;">👤 <a href="#" onclick="navigateTo('${routes.login}'); return false;" style="color: #667eea; text-decoration: underline;">Inicia sesión</a> para escribir una crítica</p>
          </div>
        `}

        <!-- Lista de críticas -->
        <div id="reviews-list" style="background: white; border-radius: 6px; padding: 1rem;">
          ${reviews && reviews.length > 0 ? `
            <h4 style="margin-top: 0; color: #333; margin-bottom: 1rem;">Críticas de usuarios (${reviews.length})</h4>
            ${reviews.map((review, index) => `
              <div style="padding: 1rem; border-bottom: ${index < reviews.length - 1 ? '1px solid #eee' : 'none'}; position: relative;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                  <div style="display: flex; align-items: center; gap: 0.8rem;">
                    <strong style="color: #667eea;">${review.username}</strong>
                    <span style="color: #ffc107; font-size: 1.1rem;">⭐ ${review.rating}/10</span>
                  </div>
                  ${currentUser?.id === review.user_id ? `
                    <button 
                      class="btn btn-small btn-danger" 
                      onclick="eliminarReview(${review.id}, ${id})"
                      style="padding: 0.4rem 0.8rem; font-size: 0.85rem;"
                    >
                      ✕
                    </button>
                  ` : ''}
                </div>
                ${review.review_text ? `
                  <p style="color: #555; margin: 0.5rem 0 0 0; line-height: 1.5;">
                    "${review.review_text}"
                  </p>
                ` : ''}
                <small style="color: #999;">
                  ${new Date(review.created_at).toLocaleDateString('es-ES')}
                </small>
              </div>
            `).join('')}
          ` : `
            <p style="color: #999; margin: 0; text-align: center; padding: 1rem;">
              No hay críticas aún. ¡Sé el primero en escribir una!
            </p>
          `}
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

async function mostrarDetallesSerie(id) {
  try {
    console.log(`Obteniendo detalles de serie ${id}`);
    const serie = await fetchAPI(`${API_URL}/series/${id}`, 'GET');
    
    if (!serie || serie.error) {
      alert('No se pudieron obtener los detalles de la serie');
      return;
    }

    const esFavorito = userFavSeriesIds.includes(id);
    const posterUrl = serie.poster_url || 'https://via.placeholder.com/300x450?text=No+Image';
    
    // Agrupar episodios por temporada
    const episodiosPorTemporada = serie.episodes_by_season || {};
    
    let detailsHTML = `
      <div class="movie-detail">
        <div class="movie-poster">
          <img src="${posterUrl}" alt="${serie.title}" onerror="this.src='https://via.placeholder.com/300x450?text=No+Image'">
        </div>
        <div class="movie-info">
          <h2>${serie.title} <span style="color: #ff6b9d; font-size: 0.8em;">📺 SERIE</span></h2>
          
          <div class="movie-meta">
            <div class="meta-item">
              <span class="meta-label">Género</span>
              <span class="meta-value">${serie.genre || 'No especificado'}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Creador</span>
              <span class="meta-value">${serie.director || 'No especificado'}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Año de Estreno</span>
              <span class="meta-value">${serie.release_date ? serie.release_date.slice(0, 4) : 'No especificado'}</span>
            </div>
          </div>

          <h3 style="color: #667eea; margin-top: 1.5rem; margin-bottom: 0.8rem;">Sinopsis</h3>
          <div class="movie-description">
            ${serie.description || 'No hay descripción disponible'}
          </div>

          <div class="movie-controls">
            <button class="btn btn-primary" onclick="cerrarDetalles()">Cerrar</button>
            <button class="btn ${esFavorito ? 'btn-danger' : 'btn-favorite'}" onclick="toggleFavorito('serie', ${serie.id})">
              ${esFavorito ? '❌ Eliminar de Favoritos' : '❤️ Agregar a Favoritos'}
            </button>
          </div>
        </div>
      </div>

      <!-- SECCIÓN DE EPISODIOS -->
      <div class="episodes-section" style="margin-top: 2rem; padding: 1.5rem; background: rgba(255, 107, 157, 0.1); border-radius: 8px;">
        <h3 style="color: #ff6b9d; margin-bottom: 1rem;">📺 Episodios</h3>
        
        ${Object.keys(episodiosPorTemporada).sort((a,b) => a-b).map(season => `
          <div class="season-section" style="margin-bottom: 2rem;">
            <h4 style="color: #333; border-bottom: 2px solid #ff6b9d; padding-bottom: 0.5rem;">Temporada ${season}</h4>
            <div style="display: grid; grid-template-columns: 1fr; gap: 0.8rem;">
              ${episodiosPorTemporada[season].map((ep, idx) => `
                <div style="background: white; padding: 1rem; border-radius: 6px; border-left: 4px solid #ff6b9d;">
                  <div style="display: flex; justify-content: space-between; align-items: start; gap: 1rem;">
                    <div style="flex: 1;">
                      <h5 style="margin: 0 0 0.5rem 0; color: #333;">
                        Cap. ${ep.episode_number}: ${ep.title}
                      </h5>
                      ${ep.description ? `
                        <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0; line-height: 1.4;">
                          ${ep.description}
                        </p>
                      ` : ''}
                      <small style="color: #999;">
                        ${ep.air_date ? new Date(ep.air_date).toLocaleDateString('es-ES') : 'Fecha no disponible'}
                        ${ep.duration_minutes ? ' - ' + ep.duration_minutes + ' min' : ''}
                      </small>
                    </div>
                    ${ep.video_url ? `
                      <a href="${ep.video_url}" target="_blank" class="btn btn-small" style="white-space: nowrap;">
                        ▶️ Ver
                      </a>
                    ` : ''}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    `;

    document.getElementById('movieDetails').innerHTML = detailsHTML;
    document.getElementById('movieModal').classList.add('active');
  } catch (error) {
    console.error('Error al obtener detalles:', error);
    alert('Error al cargar los detalles de la serie');
  }
}

// ==================== FUNCIONES: CRÍTICAS ====================
async function crearOEditarReview(event, movieId, reviewId) {
  event.preventDefault();

  if (!authToken) {
    alert('Necesitas iniciar sesión para escribir críticas');
    navigateTo(routes.login);
    return;
  }

  const rating = document.getElementById('review-rating').value;
  const reviewText = document.getElementById('review-text').value;

  if (!rating || rating < 1 || rating > 10) {
    alert('La calificación debe estar entre 1 y 10');
    return;
  }

  const reviewData = {
    movie_id: movieId,
    rating: parseInt(rating),
    review_text: reviewText.trim()
  };

  let response;
  if (reviewId && reviewId !== 'null') {
    // Editar crítica existente
    response = await fetchAPI(`${API_URL}/reviews/${reviewId}`, 'PUT', reviewData, authToken);
  } else {
    // Crear nueva crítica
    response = await fetchAPI(`${API_URL}/reviews`, 'POST', reviewData, authToken);
  }

  if (response) {
    alert(response.mensaje || 'Crítica guardada correctamente');
    // Recargar los detalles para mostrar la crítica actualizada
    mostrarDetalles(movieId);
  }
}

async function eliminarReview(reviewId, movieId) {
  if (!confirm('¿Estás seguro de que deseas eliminar tu crítica?')) return;

  const response = await fetchAPI(`${API_URL}/reviews/${reviewId}`, 'DELETE', null, authToken);
  
  if (response) {
    alert(response.mensaje || 'Crítica eliminada correctamente');
    // Recargar los detalles para actualizar la lista de críticas
    mostrarDetalles(movieId);
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
