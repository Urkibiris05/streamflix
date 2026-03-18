/*
Escribe el código JavaScript de Vanilla JS para una Single Page Application (SPA). 
El código debe hacer un fetch GET a la ruta '/api/peliculas' de nuestro servidor Flask al cargar la página. 
Renderiza esas películas en el DOM. Además, incluye una función conectada a un input de 
texto que filtre las películas mostradas por título de forma inmediata en el lado del cliente, 
sin volver a hacer peticiones al servidor.
*/

let peliculasOriginal = [];

// Fetch de películas al cargar la página
document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/peliculas')
    .then(response => response.json())
    .then(data => {
      peliculasOriginal = data;
      renderPeliculas(peliculasOriginal);
    })
    .catch(error => console.error('Error al cargar películas:', error));

  // Event listener para el input de búsqueda
  const inputBusqueda = document.getElementById('busqueda');
  if (inputBusqueda) {
    inputBusqueda.addEventListener('input', (e) => {
      filtrarPeliculas(e.target.value);
    });
  }
});

// Función para renderizar películas en el DOM
function renderPeliculas(peliculas) {
  const contenedor = document.getElementById('peliculas-container');
  if (!contenedor) return;

  contenedor.innerHTML = '';

  if (peliculas.length === 0) {
    contenedor.innerHTML = '<p>No se encontraron películas.</p>';
    return;
  }

  peliculas.forEach(pelicula => {
    const div = document.createElement('div');
    div.className = 'pelicula-card';
    div.innerHTML = `
      <h3>${pelicula.titulo}</h3>
      <p><strong>Año:</strong> ${pelicula.año || 'N/A'}</p>
      <p><strong>Género:</strong> ${pelicula.genero || 'N/A'}</p>
      <p>${pelicula.descripcion || ''}</p>
    `;
    contenedor.appendChild(div);
  });
}

// Función para filtrar películas por título
function filtrarPeliculas(titulo) {
  const filtradas = peliculasOriginal.filter(pelicula =>
    pelicula.titulo.toLowerCase().includes(titulo.toLowerCase())
  );
  renderPeliculas(filtradas);
}
