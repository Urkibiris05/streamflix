-- ==================== DATOS INICIALES - STREAMFLIX ====================
-- Integración de seed_data.sql y seed.sql

-- ==================== INSERCIONES DE USUARIOS ====================

-- Usuario demo
INSERT OR IGNORE INTO user (username, email, password_hash, role, is_active) VALUES
('demo', 'demo@example.com', '$2b$12$IOWaGAooEVVOg5IjCTOIAexFY227N2fY30KVDq8sWKGPNHwcrspO.', 'user', 1); -- Contraseña: "demo123"

-- Usuario admin
INSERT OR IGNORE INTO user (username, email, password_hash, role, is_active) VALUES
('admin', 'admin@example.com', '$2b$12$IOWaGAooEVVOg5IjCTOIAexFY227N2fY30KVDq8sWKGPNHwcrspO.', 'admin', 1); -- Contraseña: "demo123"

-- Usuarios adicionales de seed_data.sql
INSERT OR IGNORE INTO user (username, email, password_hash, role, is_active) VALUES
('admin_user', 'admin@streamflix.com', '$2b$12$..', 'admin', 1),
('juan_doe', 'juan@example.com', '$2b$12$..', 'user', 1),
('maria_garcia', 'maria@example.com', '$2b$12$..', 'user', 1),
('carlos_martinez', 'carlos@example.com', '$2b$12$..', 'user', 1);

-- ==================== INSERCIONES DE PELÍCULAS ====================

INSERT OR IGNORE INTO movie (title, description, director, genre, release_date, duration_minutes, rating, poster_url, created_at, updated_at) VALUES

-- Ciencia Ficción
('Inception', 'A skilled thief who steals corporate secrets through the use of dream-sharing technology.', 'Christopher Nolan', 'Sci-Fi', '2010-07-16', 148, 8.8, 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh88PCbHm3hyphenhyphenvBtFJ0aOzeD1X15qJ8V-trbpsqbPAveXpZaetKdLhyZTFWqWUGkE6-HUOFs7c6tckJnHjVgBUwW_4haqdn599MEgFWVuibVrsCTPBP5Owyjza-9hky_75HzV3GjXh0kDlUt25kE6vjccWUwNhYlTQ7hNsLUsYPKh86EmqwO4DGzWKioNfM/s1008/critica-pelicula-origen-2010.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Matrix', 'A hacker learns about the true nature of his reality and his role in the war against its controllers.', 'The Wachowskis', 'Sci-Fi', '1999-03-31', 136, 8.7, 'https://www.posterscine.com/media/catalog/product/cache/1c91d037a1f0ef180108abb0973795cc/m/a/matrix_1999_poster_1.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity''s survival.', 'Christopher Nolan', 'Sci-Fi', '2014-11-07', 169, 8.6, 'https://pics.filmaffinity.com/Interstellar-366875261-large.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Blade Runner 2049', 'An officer of the LAPD searches for a missing former officer to stop an impending conflict between two worlds.', 'Denis Villeneuve', 'Sci-Fi', '2017-10-06', 163, 8.0, 'https://m.media-amazon.com/images/I/7101A53+ygL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Star Wars: Episode IV - A New Hope', 'Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire''s world-destroying battle station.', 'George Lucas', 'Sci-Fi', '1977-05-25', 121, 8.6, 'https://m.media-amazon.com/images/I/91YXgocJn5L._UF1000,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Drama
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 'Frank Darabont', 'Drama', '1994-09-23', 142, 9.3, 'https://i.ebayimg.com/images/g/Y8MAAOSwnWBdZ9Dm/s-l1200.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Forrest Gump', 'The presidencies of Kennedy and Johnson, Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with an IQ of 75.', 'Robert Zemeckis', 'Drama', '1994-07-06', 142, 8.8, 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh86k8w5isb3n60OC5YoOjbBkHUAUu3dTsuQnAgopb_0oJnsO3tQbf24OdEUTTJPdwsfpaxvuC9s3dwHHGamyNKIYeb6KeUJ3hgY27JadJ1o7jH2warIHck9v1HBX3Cia-zDLur7UnHrJ2LOa0MpBPF99KzG_Bt9mdq7ZtzyWkNCG6ya4rUiaf8A0ucCF0/s1450/Forrest-Gump.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Fight Club', 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.', 'David Fincher', 'Drama', '1999-10-15', 139, 8.8, 'https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Acción y Thriller
('The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.', 'Christopher Nolan', 'Thriller', '2008-07-18', 152, 9.0, 'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('John Wick', 'An ex-hitman comes out of retirement to settle a score when the son of a crime boss kills his dog.', 'Chad Stahelski', 'Action', '2014-10-24', 101, 7.4, 'https://cdng.europosters.eu/pod_public/750/263137.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Avengers', 'Earth''s mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.', 'Joss Whedon', 'Action', '2012-05-04', 143, 8.0, 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/2/2b/The_Avengers_Poster.png/revision/latest/scale-to-width-down/1200?cb=20150610135853&path-prefix=es', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Die Hard', 'A detective must save his estranged wife and several others taken hostage by terrorists in a skyscraper.', 'John McTiernan', 'Action', '1988-07-15', 131, 8.3, 'https://images.photowall.com/products/59337/bruce-willis-in-die-hard.jpg?h=699&q=85', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Parasite', 'The relationship between two families is tested when they start living together in a small apartment.', 'Bong Joon-ho', 'Thriller', '2019-05-30', 132, 8.5, 'https://m.media-amazon.com/images/I/71960VfyitL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Crimen
('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.', 'Quentin Tarantino', 'Crime', '1994-10-14', 154, 8.9, 'https://m.media-amazon.com/images/I/81UTs3sC5hL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 'Francis Ford Coppola', 'Crime', '1972-03-24', 175, 9.2, 'https://m.media-amazon.com/images/M/MV5BNGEwYjgwOGQtYjg5ZS00Njc1LTk2ZGEtM2QwZWQ2NjdhZTE5XkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Fantasía
('The Lord of the Rings: The Fellowship of the Ring', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth.', 'Peter Jackson', 'Fantasy', '2001-12-19', 178, 8.8, 'https://upload.wikimedia.org/wikipedia/en/f/fb/Lord_Rings_Fellowship_Ring.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Harry Potter y la Piedra Filosofal', 'Un joven mago descubre su verdadero legado y asiste a una escuela de magia donde debe enfrentarse a fuerzas oscuras.', 'Chris Columbus', 'Fantasía', '2001-11-16', 152, 7.6, 'https://media.posterstore.com/site_images/68631db092c536b9cc92b06f_775081888_WB0101-5.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Comedia
('The Grand Budapest Hotel', 'A movie about the adventures of a fictional writer and a film that documents his childhood memories.', 'Wes Anderson', 'Comedy', '2014-03-28', 99, 8.1, 'https://media.posterlounge.com/img/products/740000/732265/732265_poster.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Hangover', 'Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing.', 'Todd Phillips', 'Comedy', '2009-06-05', 100, 7.7, 'https://m.media-amazon.com/images/I/91pvafw44bL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Animación
('El Viaje de Chihiro', 'Durante la mudanza de su familia a las afueras, una chica malhumorada aparentemente se somete a una transformación sobrenatural.', 'Hayao Miyazaki', 'Animación', '2001-07-20', 125, 8.6, 'https://m.media-amazon.com/images/M/MV5BM2E2YzcwMTQtNWRlMC00ZGZlLWJhZTEtMDU4ZGIzMWI0NzJmXkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Coco', 'Inspirado a seguir su pasión por la música, un joven talentoso entra a la vibrante Tierra de los Muertos.', 'Lee Unkrich', 'Animación', '2017-11-22', 105, 8.4, 'https://i.ebayimg.com/images/g/6IkAAOSwMw1hZOzG/s-l1200.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Your Name', 'Dos adolescentes intercambian sus cuerpos a través del tiempo y deben colaborar para evitar un desastre.', 'Makoto Shinkai', 'Animación', '2016-08-26', 106, 8.4, 'https://m.media-amazon.com/images/M/MV5BMTIyNzFjNzItZmQ1MC00NzhjLThmMzYtZjRhN2Y3MmM2OGQyXkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Toy Story', 'A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy''s room.', 'John Lasseter', 'Animation', '1995-11-22', 81, 8.3, 'https://m.media-amazon.com/images/M/MV5BZTA3OWVjOWItNjE1NS00NzZiLWE1MjgtZDZhMWI1ZTlkNzYwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP); 

-- ==================== INSERCIONES DE FAVORITOS ====================

-- Favoritos del usuario demo (id: 1)
INSERT OR IGNORE INTO favorites (user_id, movie_id) VALUES
(1, 1), -- demo favorita Inception
(1, 8), -- demo favorita The Dark Knight
(1, 16); -- demo favorita The Godfather

-- Favoritos de los usuarios adicionales
-- juan_doe (id: 3) favoritos
INSERT OR IGNORE INTO favorites (user_id, movie_id) VALUES
(3, 1), -- juan_doe favorita Inception
(3, 6); -- juan_doe favorita The Shawshank Redemption

-- maria_garcia (id: 4) favoritos
INSERT OR IGNORE INTO favorites (user_id, movie_id) VALUES
(4, 2), -- maria_garcia favorita The Matrix
(4, 11); -- maria_garcia favorita Die Hard

-- carlos_martinez (id: 5) favoritos
INSERT OR IGNORE INTO favorites (user_id, movie_id) VALUES
(5, 8), -- carlos_martinez favorita The Dark Knight
(5, 18); -- carlos_martinez favorita Spirited Away

-- ==================== NOTAS ====================
/*
IMPORTANTE: Los valores de password_hash son placeholders para testing.
Los usuarios creados son:
- demo (contraseña: demo123)
- admin (contraseña: demo123)
- admin_user
- juan_doe
- maria_garcia
- carlos_martinez

Todas las películas se cargan con INSERT OR IGNORE para evitar duplicados.
*/
