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
('Inception', 'Un ladrón experto que roba secretos corporativos mediante tecnología de intercambio de sueños.', 'Christopher Nolan', 'Ciencia Ficción', '2010-07-16', 148, 8.8, 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh88PCbHm3hyphenhyphenvBtFJ0aOzeD1X15qJ8V-trbpsqbPAveXpZaetKdLhyZTFWqWUGkE6-HUOFs7c6tckJnHjVgBUwW_4haqdn599MEgFWVuibVrsCTPBP5Owyjza-9hky_75HzV3GjXh0kDlUt25kE6vjccWUwNhYlTQ7hNsLUsYPKh86EmqwO4DGzWKioNfM/s1008/critica-pelicula-origen-2010.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Matrix', 'Un hacker aprende la verdadera naturaleza de su realidad y su papel en la guerra contra sus controladores.', 'Las Wachowski', 'Ciencia Ficción', '1999-03-31', 136, 8.7, 'https://www.posterscine.com/media/catalog/product/cache/1c91d037a1f0ef180108abb0973795cc/m/a/matrix_1999_poster_1.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Interestelar', 'Un equipo de exploradores viaja a través de un agujero de gusano en el espacio para garantizar la supervivencia de la humanidad.', 'Christopher Nolan', 'Ciencia Ficción', '2014-11-07', 169, 8.6, 'https://pics.filmaffinity.com/Interstellar-366875261-large.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Blade Runner 2049', 'Un oficial de la LAPD busca a un oficial desaparecido para prevenir un conflicto entre dos mundos.', 'Denis Villeneuve', 'Ciencia Ficción', '2017-10-06', 163, 8.0, 'https://m.media-amazon.com/images/I/7101A53+ygL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Star Wars: Episodio IV', 'Luke Skywalker se une a un caballero Jedi, un piloto audaz, un Wookiee y dos droides para salvar la galaxia.', 'George Lucas', 'Ciencia Ficción', '1977-05-25', 121, 8.6, 'https://m.media-amazon.com/images/I/91YXgocJn5L._UF1000,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Drama
('Cadena Perpetua', 'Dos hombres encarcelados se unen a lo largo de los años encontrando consuelo y redención mediante actos de decencia común.', 'Frank Darabont', 'Drama', '1994-09-23', 142, 9.3, 'https://i.ebayimg.com/images/g/Y8MAAOSwnWBdZ9Dm/s-l1200.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Forrest Gump', 'Las presidencias de Kennedy y Johnson, Vietnam, Watergate y otros eventos históricos vistos través de un hombre de Alabama con cociente intelectual de 75.', 'Robert Zemeckis', 'Drama', '1994-07-06', 142, 8.8, 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh86k8w5isb3n60OC5YoOjbBkHUAUu3dTsuQnAgopb_0oJnsO3tQbf24OdEUTTJPdwsfpaxvuC9s3dwHHGamyNKIYeb6KeUJ3hgY27JadJ1o7jH2warIHck9v1HBX3Cia-zDLur7UnHrJ2LOa0MpBPF99KzG_Bt9mdq7ZtzyWkNCG6ya4rUiaf8A0ucCF0/s1450/Forrest-Gump.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('El Club de la Lucha', 'Un trabajador de oficina insomne y un fabricante de jabón sin preocupaciones forman un club de peleas clandestino que evoluciona en algo mucho mayor.', 'David Fincher', 'Drama', '1999-10-15', 139, 8.8, 'https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Acción y Suspenso
('El Caballero Oscuro', 'Cuando el Joker causa caos en Gotham, Batman debe aceptar una de las mayores pruebas psicológicas y físicas.', 'Christopher Nolan', 'Suspenso', '2008-07-18', 152, 9.0, 'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('John Wick', 'Un ex asesino sale de retiro para vengarse cuando el hijo de un jefe del crimen mata a su perro.', 'Chad Stahelski', 'Acción', '2014-10-24', 101, 7.4, 'https://cdng.europosters.eu/pod_public/750/263137.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Los Vengadores', 'Los héroes más poderosos de la Tierra deben reunirse y aprender a luchar como equipo para detener a Loki y su ejército extranjero.', 'Joss Whedon', 'Acción', '2012-05-04', 143, 8.0, 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/2/2b/The_Avengers_Poster.png/revision/latest/scale-to-width-down/1200?cb=20150610135853&path-prefix=es', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Die Hard', 'Un detective debe salvar a su esposa y a varias personas tomadas como rehenes por terroristas en un rascacielos.', 'John McTiernan', 'Acción', '1988-07-15', 131, 8.3, 'https://images.photowall.com/products/59337/bruce-willis-in-die-hard.jpg?h=699&q=85', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Parásita', 'La relación entre dos familias se pone a prueba cuando empiezan a vivir juntas en un apartamento pequeño.', 'Bong Joon-ho', 'Suspenso', '2019-05-30', 132, 8.5, 'https://m.media-amazon.com/images/I/71960VfyitL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Crimen
('Pulp Fiction', 'Las vidas de dos asesinos a sueldo, un boxeador y un gánster se cruzan en cuatro historias de violencia y redención.', 'Quentin Tarantino', 'Crimen', '1994-10-14', 154, 8.9, 'https://m.media-amazon.com/images/I/81UTs3sC5hL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('El Padrino', 'El patriarca envejecido de un imperio del crimen organizado transfiere el control a su hijo reacio.', 'Francis Ford Coppola', 'Crimen', '1972-03-24', 175, 9.2, 'https://m.media-amazon.com/images/M/MV5BNGEwYjgwOGQtYjg5ZS00Njc1LTk2ZGEtM2QwZWQ2NjdhZTE5XkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Fantasía
('El Señor de los Anillos: La Comunidad del Anillo', 'Un pequeño Hobbit del Condado y ocho compañeros salen en una aventura para destruir el Anillo Único y salvar la Tierra Media.', 'Peter Jackson', 'Fantasía', '2001-12-19', 178, 8.8, 'https://upload.wikimedia.org/wikipedia/en/f/fb/Lord_Rings_Fellowship_Ring.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Harry Potter y la Piedra Filosofal', 'Un joven mago descubre su verdadero legado y asiste a una escuela de magia donde debe enfrentarse a fuerzas oscuras.', 'Chris Columbus', 'Fantasía', '2001-11-16', 152, 7.6, 'https://media.posterstore.com/site_images/68631db092c536b9cc92b06f_775081888_WB0101-5.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Comedia
('Hotel Budapest', 'Una película sobre las aventuras de un escritor ficticio y un film que documenta sus recuerdos de infancia.', 'Wes Anderson', 'Comedia', '2014-03-28', 99, 8.1, 'https://media.posterlounge.com/img/products/740000/732265/732265_poster.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Resacón en las Vegas', 'Tres amigos despiertan de una despedida de soltero en Las Vegas sin recuerdos de la noche anterior y con el novio desaparecido.', 'Todd Phillips', 'Comedia', '2009-06-05', 100, 7.7, 'https://m.media-amazon.com/images/I/91pvafw44bL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Animación
('El Viaje de Chihiro', 'Durante la mudanza de su familia, una chica malhumorada aparentemente se somete a una transformación sobrenatural.', 'Hayao Miyazaki', 'Animación', '2001-07-20', 125, 8.6, 'https://m.media-amazon.com/images/M/MV5BM2E2YzcwMTQtNWRlMC00ZGZlLWJhZTEtMDU4ZGIzMWI0NzJmXkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Coco', 'Inspirado a seguir su pasión por la música, un joven talentoso entra a la vibrante Tierra de los Muertos.', 'Lee Unkrich', 'Animación', '2017-11-22', 105, 8.4, 'https://i.ebayimg.com/images/g/6IkAAOSwMw1hZOzG/s-l1200.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Your Name', 'Dos adolescentes intercambian sus cuerpos a través del tiempo y deben colaborar para evitar un desastre.', 'Makoto Shinkai', 'Animación', '2016-08-26', 106, 8.4, 'https://m.media-amazon.com/images/M/MV5BMTIyNzFjNzItZmQ1MC00NzhjLThmMzYtZjRhN2Y3MmM2OGQyXkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Toy Story', 'Un vaquero de juguete se siente profundamente amenazado y celoso cuando una nueva figura de astronauta lo reemplaza como juguete principal en la habitación de un niño.', 'John Lasseter', 'Animación', '1995-11-22', 81, 8.3, 'https://m.media-amazon.com/images/M/MV5BZTA3OWVjOWItNjE1NS00NzZiLWE1MjgtZDZhMWI1ZTlkNzYwXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP); 

-- ==================== INSERCIONES DE FAVORITOS ====================

-- Favoritos del usuario demo (id: 1)
INSERT OR IGNORE INTO favorites (user_id, movie_id) VALUES
(1, 1), -- demo favorita Inception
(1, 8), -- demo favorita El Caballero Oscuro
(1, 16); -- demo favorita El Padrino

-- Favoritos de los usuarios adicionales
-- juan_doe (id: 3) favoritos
INSERT OR IGNORE INTO favorites (user_id, movie_id) VALUES
(3, 1), -- juan_perez favorita Inception
(3, 6); -- juan_perez favorita La Redención

-- maria_garcia (id: 4) favoritos
INSERT OR IGNORE INTO favorites (user_id, movie_id) VALUES
(4, 2), -- maria_garcia favorita Matrix
(4, 11); -- maria_garcia favorita Cristal Oscuro

-- carlos_martinez (id: 5) favoritos
INSERT OR IGNORE INTO favorites (user_id, movie_id) VALUES
(5, 8), -- carlos_martinez favorita The Dark Knight
(5, 18); -- carlos_martinez favorita Spirited Away
-- ==================== INSERCIONES DE CRÍTICAS Y RATINGS ====================

-- Críticas del usuario demo (id: 1)
INSERT OR IGNORE INTO review (user_id, movie_id, rating, review_text, created_at, updated_at) VALUES
(1, 1, 9, 'Una película increíble. Nolan es un genio. La narrativa no lineal me dejó fascimado. Totalmente recomendada.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 8, 10, 'La mejor película de Christopher Nolan. Ledger es simplemente espectacular como el Joker. Magistral.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 6, 9, 'Una obra maestra del cine. La actuación de Morgan Freeman y Tim Robbins es impecable. Imprescindible.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Críticas de juan_doe (id: 3)
INSERT OR IGNORE INTO review (user_id, movie_id, rating, review_text, created_at, updated_at) VALUES
(3, 1, 8, 'Good movie, aunque un poco confusa al principio. Pero vale mucho la pena verla.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 2, 9, 'The Matrix es una película que cambió el cine para siempre. Aún se ve perfecta hoy en día.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 10, 7, 'Una película de acción divertida. Nada extraordinario pero entretenida.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Críticas de maria_garcia (id: 4)
INSERT OR IGNORE INTO review (user_id, movie_id, rating, review_text, created_at, updated_at) VALUES
(4, 2, 10, 'Simplemente la mejor película de ciencia ficción. Los efectos siguen siendo increíbles.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 3, 9, 'Interstellar es épica. La música de Hans Zimmer es simplemente hermosa.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 7, 9, 'Fight Club es brutal e inteligente. Denzel Washington es excelente en este rol.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Críticas de carlos_martinez (id: 5)
INSERT OR IGNORE INTO review (user_id, movie_id, rating, review_text, created_at, updated_at) VALUES
(5, 8, 10, 'The Dark Knight es la más grande película de superhéroes jamás realizada.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 14, 9, 'Pulp Fiction es una obra de arte. Tarantino es un maestro del cine.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 21, 8, 'Coco es una película hermosa con una historia conmovedora. Recomendadísima.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
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

-- ==================== INSERCIONES DE SERIES ====================

-- Breaking Bad - Serie de prueba
INSERT OR IGNORE INTO series (title, description, director, genre, release_date, poster_url, created_at, updated_at) VALUES
('Breaking Bad', 'A high school chemistry teacher turned meth kingpin. A story of transformation, ambition, and the consequences of choices.', 'Vince Gilligan', 'Drama/Crime', '2008-01-20', 'https://m.media-amazon.com/images/M/MV5BMJQ0MTQ2MzAxNV5BMl5BanBnXkFtZTgwNTAwMzQxNzE@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ==================== INSERCIONES DE EPISODIOS ====================

-- Temporada 1
INSERT OR IGNORE INTO episode (series_id, title, description, season, episode_number, air_date, duration_minutes, video_url, created_at, updated_at) VALUES
(1, 'Pilot', 'When an unassuming high school chemistry teacher discovers he is dying, he decides to use his last years to gain wealth for his family.', 1, 1, '2008-01-20', 58, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Cat''s in the Bag', 'Walter must dispose of evidence while Jesse deals with a prisoner in chains. Hank celebrates his latest DEA bust.', 1, 2, '2008-01-27', 48, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'And the Bag''s in the River', 'Walter and Jesse go to extreme lengths to dispose of evidence. Nacho sets his sights on Jesse for revenge.', 1, 3, '2008-02-03', 47, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Cancer Man', 'Walter Jr. worries about his father''s condition. Walter''s wife Skyler wants him to turn to his former teacher.', 1, 4, '2008-02-10', 47, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Gray Matter', 'When Walter uses chemistry to eliminate some undesirable gang members, Jesse grows anxious. Flashbacks reveal how Walter came to be a high school teacher.', 1, 5, '2008-02-17', 58, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Crazy Handful of Nothin''', 'Walter makes a bold move as a drug dealer. Jesse faces a hard choice when he spots an old flame. Walt Jr. gets in trouble at school.', 1, 6, '2008-02-24', 58, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'A No-Rough-Stuff-Type Deal', 'Walter and Jesse must make a high-stakes decision when Krazy-8 and Emilio corner them.', 1, 7, '2008-03-09', 58, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Temporada 2
INSERT OR IGNORE INTO episode (series_id, title, description, season, episode_number, air_date, duration_minutes, video_url, created_at, updated_at) VALUES
(1, 'Seven Thirty-Seven', 'An old adversary surfaces in Albuquerque. Walt, Jesse, and Skyler face challenges as Walt lies to cover up his activities.', 2, 1, '2009-03-08', 58, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Grilled', 'Walter and Jesse are trapped in a dire situation. Hank investigates a connection to a major drug dealer.', 2, 2, '2009-03-15', 47, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Bit by a Dead Bee', 'Walt and Jesse are revealed after being found by DEA. Skyler becomes suspicious. A mysterious figure makes an appearance.', 2, 3, '2009-03-22', 47, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Down', 'Skyler fights for her marriage with Walt. Jesse spirals after a tough loss. Nacho leads a criminal enterprise.', 2, 4, '2009-03-29', 47, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Breakage', 'Walter and Jesse expand their operation. Skyler visits her son. Mike is introduced to the story.', 2, 5, '2009-04-05', 47, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Temporada 3 (primeros 2 episodios como ejemplo)
INSERT OR IGNORE INTO episode (series_id, title, description, season, episode_number, air_date, duration_minutes, video_url, created_at, updated_at) VALUES
(1, 'No Mas', 'Walt and Skyler face a turning point in their relationship. The Cousins arrive in Albuquerque.', 3, 1, '2010-03-21', 58, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Caballo sin Nombre', 'Jesse is traumatized by the aftermath. Walt makes a plea to a former associate.', 3, 2, '2010-03-28', 47, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
