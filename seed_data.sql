-- ==================== DATOS DE PRUEBA - STREAMFLIX ====================
-- Script de inserción de datos de ejemplo para testing

USE streamflix;

-- Limpiar datos anteriores (opcional)
-- DELETE FROM favorites;
-- DELETE FROM movie;
-- DELETE FROM user;

-- ==================== INSERCIONES DE USUARIOS ====================

INSERT INTO user (username, email, password_hash, role, is_active) VALUES
-- Contraseña: admin123 (hasheada con bcrypt)
('admin_user', 'admin@streamflix.com', '$2b$12$..', 'admin', TRUE),
-- Contraseña: user123 (hasheada con bcrypt)
('juan_doe', 'juan@example.com', '$2b$12$..', 'user', TRUE),
('maria_garcia', 'maria@example.com', '$2b$12$..', 'user', TRUE),
('carlos_martinez', 'carlos@example.com', '$2b$12$..', 'user', TRUE);

-- ==================== INSERCIONES DE PELÍCULAS ====================

INSERT INTO movie (title, description, director, genre, release_date, duration_minutes, rating, poster_url, video_url) VALUES

-- Ciencia Ficción
('Inception', 'Un ladrón experto que roba secretos corporales de objetivos mientras sueñan. Ofrece un último trabajo: hacer realidad una idea en lugar de robar una.', 'Christopher Nolan', 'Sci-Fi', '2010-07-16', 148, 8.8, 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300', NULL),

('The Matrix', 'Un hacker aprende la verdadera naturaleza de su realidad y su rol en la guerra contra los controladores de ella.', 'Lana Wachowski, Lilly Wachowski', 'Sci-Fi', '1999-03-31', 136, 8.7, 'https://images.unsplash.com/photo-1485095329183-d0daf68471ca?w=300', NULL),

('Interstellar', 'Un equipo de exploradores viaja a través de un agujero de gusano en el espacio en un intento desesperado de garantizar la supervivencia humana.', 'Christopher Nolan', 'Sci-Fi', '2014-11-07', 169, 8.6, 'https://images.unsplash.com/photo-1532274040911-5f82f72696c0?w=300', NULL),

('Blade Runner 2049', 'Un oficial de policía de la LAPD busca a Rick Deckard, un ex oficial de policía desaparecido que ha estado en el anonimato durante treinta años.', 'Denis Villeneuve', 'Sci-Fi', '2017-10-06', 163, 8.0, 'https://images.unsplash.com/photo-1420139394332-55c2b3d5b3aa?w=300', NULL),

-- Drama
('The Shawshank Redemption', 'Dos hombres encarcelados se unen durante un número de años, encontrando consuelo y redención a través de actos de decencia común.', 'Frank Darabont', 'Drama', '1994-10-14', 142, 9.3, 'https://images.unsplash.com/photo-1542040220-cd2b14c14a48?w=300', NULL),

('Forrest Gump', 'Las décadas de la vida de la vida de un hombre que tiene una baja capacidad mental, pero la naturaleza de un genio, lo lleva a través de tres eras de Estados Unidos.', 'Robert Zemeckis', 'Drama', '1994-07-06', 142, 8.8, 'https://images.unsplash.com/photo-1506399773649-6e0eb8cfb237?w=300', NULL),

('The Godfather', 'La historia del ascenso y la decadencia de la dinastía del crimen clandestino.', 'Francis Ford Coppola', 'Drama', '1972-03-24', 175, 9.2, 'https://images.unsplash.com/photo-1489599810694-b5c89f8b7cf0?w=300', NULL),

-- Acción
('John Wick', 'Un ex asesino jubilado viene de la jubilación para rastrear a los hombres que lo traicionaron y asesinaron a su mascota.', 'Chad Stahelski', 'Action', '2014-10-24', 101, 7.4, 'https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=300', NULL),

('The Avengers', 'Los héroes más poderosos de la Tierra deben unirse como nunca antes para defender al planeta de un ataque de otro mundo.', 'Joss Whedon', 'Action', '2012-05-04', 143, 8.0, 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=300', NULL),

('Die Hard', 'Un oficial de policía entra en un centro comercial de alta seguridad durante una toma de rehenes y debe salvar a su esposa.', 'John McTiernan', 'Action', '1988-07-15', 131, 8.3, 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300', NULL),

-- Suspenso
('The Dark Knight', 'Cuando la amenaza conocida como The Joker causa un caos en Gotham, el caballero oscuro debe asumir uno de los desafíos más grandes.', 'Christopher Nolan', 'Thriller', '2008-07-18', 152, 9.0, 'https://images.unsplash.com/photo-1454749781529-6a03281a02b7?w=300', NULL),

('Parasite', 'La amistad entre dos familias es puesta a prueba cuando empiezan a vivir juntas en un apartamento muy pequeño.', 'Bong Joon-ho', 'Thriller', '2019-05-30', 132, 8.5, 'https://images.unsplash.com/photo-1520676867-e0a0fe0d4a08?w=300', NULL),

-- Comedia
('Forrest Gump', 'Las décadas de la vida de un hombre de poca capacidad mental tienen un profundo efecto en las personas a su alrededor.', 'Robert Zemeckis', 'Comedy', '1994-07-06', 142, 8.8, 'https://images.unsplash.com/photo-1532274040911-5f82f72696c0?w=300', NULL),

('The Grand Budapest Hotel', 'Un escritor debutante encuentra un anónimo manuscrito en una antigua casa de huéspedes en París descubriendo una historia de amistad.', 'Wes Anderson', 'Comedy', '2014-03-28', 99, 8.1, 'https://images.unsplash.com/photo-1484992651252-895e2ca67fca?w=300', NULL),

-- Animación
('Spirited Away', 'Durante sus viajes, una niña entra en un mundo mágico de dioses y espíritus y debe trabajar en un baño para escapar.', 'Hayao Miyazaki', 'Animation', '2001-07-20', 125, 8.6, 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=300', NULL),

('Coco', 'Inspirado a seguir su pasión por la música, un joven talentoso cruza al fantástico Tierra de los Muertos.', 'Lee Unkrich', 'Animation', '2017-11-22', 105, 8.4, 'https://images.unsplash.com/photo-1469511069256-48b871f8d3ab?w=300', NULL);

-- ==================== INSERCIONES DE FAVORITOS ====================

INSERT INTO favorites (user_id, movie_id) VALUES
(2, 1),  -- juan_doe favorita Inception
(2, 5),  -- juan_doe favorita The Shawshank Redemption
(3, 2),  -- maria_garcia favorita The Matrix
(3, 10), -- maria_garcia favorita Die Hard
(4, 11), -- carlos_martinez favorita The Dark Knight
(4, 15); -- carlos_martinez favorita Spirited Away

-- ==================== VERIFICACIONES ====================

-- Verificar usuarios
SELECT 'USUARIOS CREADOS:' as Info;
SELECT id, username, email, role FROM user;

-- Verificar películas
SELECT 'PELÍCULAS CREADAS:' as Info;
SELECT id, title, genre, rating FROM movie;

-- Verificar favoritos
SELECT 'FAVORITOS CREADOS:' as Info;
SELECT f.user_id, u.username, f.movie_id, m.title 
FROM favorites f 
JOIN user u ON f.user_id = u.id 
JOIN movie m ON f.movie_id = m.id;

-- ==================== NOTAS ====================
/*
IMPORTANTE: Los valores de password_hash en los usuarios son placeholders.
Para crear usuarios con contraseñas reales, usar desde la aplicación con el formulario de registro.

Contraseñas de ejemplo para testing:
- admin@streamflix.com: admin123
- juan@example.com: user123
- maria@example.com: user123
- carlos@example.com: user123

Todos deben ser generados con Bcrypt en la aplicación.
*/
