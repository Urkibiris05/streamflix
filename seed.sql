-- Datos iniciales para la base de datos Streamflix

-- Usuario demo
INSERT OR IGNORE INTO user (username, email, password_hash, role) VALUES
('demo', 'demo@example.com', '$2b$12$IOWaGAooEVVOg5IjCTOIAexFY227N2fY30KVDq8sWKGPNHwcrspO.', 'user'); -- Contraseña: "demo123"

-- Usuario admin
INSERT OR IGNORE INTO user (username, email, password_hash, role) VALUES
('admin', 'admin@example.com', '$2b$12$IOWaGAooEVVOg5IjCTOIAexFY227N2fY30KVDq8sWKGPNHwcrspO.', 'admin'); -- Contraseña: "demo123"

-- Películas
INSERT OR IGNORE INTO movie (title, description, director, genre, release_date, duration_minutes, rating, poster_url, created_at, updated_at) VALUES
('Inception', 'A skilled thief who steals corporate secrets through the use of dream-sharing technology.', 'Christopher Nolan', 'Sci-Fi', '2010-07-16', 148, 8.8, 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh88PCbHm3hyphenhyphenvBtFJ0aOzeD1X15qJ8V-trbpsqbPAveXpZaetKdLhyZTFWqWUGkE6-HUOFs7c6tckJnHjVgBUwW_4haqdn599MEgFWVuibVrsCTPBP5Owyjza-9hky_75HzV3GjXh0kDlUt25kE6vjccWUwNhYlTQ7hNsLUsYPKh86EmqwO4DGzWKioNfM/s1008/critica-pelicula-origen-2010.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Matrix', 'A hacker learns about the true nature of his reality and his role in the war against its controllers.', 'The Wachowskis', 'Sci-Fi', '1999-03-31', 136, 8.7, 'https://www.posterscine.com/media/catalog/product/cache/1c91d037a1f0ef180108abb0973795cc/m/a/matrix_1999_poster_1.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity''s survival.', 'Christopher Nolan', 'Sci-Fi', '2014-11-07', 169, 8.6, 'https://pics.filmaffinity.com/Interstellar-366875261-large.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 'Frank Darabont', 'Drama', '1994-09-23', 142, 9.3, 'https://i.ebayimg.com/images/g/Y8MAAOSwnWBdZ9Dm/s-l1200.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Forrest Gump', 'The presidencies of Kennedy and Johnson, Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with an IQ of 75.', 'Robert Zemeckis', 'Drama', '1994-07-06', 142, 8.8, 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh86k8w5isb3n60OC5YoOjbBkHUAUu3dTsuQnAgopb_0oJnsO3tQbf24OdEUTTJPdwsfpaxvuC9s3dwHHGamyNKIYeb6KeUJ3hgY27JadJ1o7jH2warIHck9v1HBX3Cia-zDLur7UnHrJ2LOa0MpBPF99KzG_Bt9mdq7ZtzyWkNCG6ya4rUiaf8A0ucCF0/s1450/Forrest-Gump.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.', 'Christopher Nolan', 'Action', '2008-07-18', 152, 9.0, 'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.', 'Quentin Tarantino', 'Crime', '1994-10-14', 154, 8.9, 'https://m.media-amazon.com/images/I/81UTs3sC5hL._AC_UF894,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Fight Club', 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.', 'David Fincher', 'Drama', '1999-10-15', 139, 8.8, 'https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Lord of the Rings: The Fellowship of the Ring', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth.', 'Peter Jackson', 'Fantasy', '2001-12-19', 178, 8.8, 'https://upload.wikimedia.org/wikipedia/en/f/fb/Lord_Rings_Fellowship_Ring.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Star Wars: Episode IV - A New Hope', 'Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire''s world-destroying battle station.', 'George Lucas', 'Sci-Fi', '1977-05-25', 121, 8.6, 'https://m.media-amazon.com/images/I/91YXgocJn5L._UF1000,1000_QL80_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 'Francis Ford Coppola', 'Crime', '1972-03-24', 175, 9.2, 'https://m.media-amazon.com/images/M/MV5BNGEwYjgwOGQtYjg5ZS00Njc1LTk2ZGEtM2QwZWQ2NjdhZTE5XkEyXkFqcGc@._V1_.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('The Avengers', 'Earth''s mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.', 'Joss Whedon', 'Action', '2012-05-04', 143, 8.0, 'https://static.wikia.nocookie.net/marvelcinematicuniverse/images/2/2b/The_Avengers_Poster.png/revision/latest/scale-to-width-down/1200?cb=20150610135853&path-prefix=es', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Favoritos del usuario demo
INSERT OR IGNORE INTO favorites (movie_id, user_id) VALUES
(1, 1), -- Inception
(6, 1), -- The Dark Knight
(11, 1); -- The Godfather
