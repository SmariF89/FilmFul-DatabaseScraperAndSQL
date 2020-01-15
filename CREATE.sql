-- Features

--	Get all movies
--	Get all movies with certain actor(s)
--	Get all movies with certain director(s)
--	Get all movies with certain actor(s) AND director(s)
--	Get all movies with certain actor(s) AND certain genre
--	Get all movies with certain director(s) AND certain genre
--	Get all movies with certain actor(s) AND director(s) AND certain genre
--	Get all movies with certain actor(s) with rate in certain range
--	Get all movies with certain actor(s) 
--	Get all movies where the director(s) is also an actor

-- Get all actors
-- Get all actors of a certain movie
-- Get all actors in films released at or after 1985 and are of a certain genre

-- Get all directors
-- Get all directors who have released more than three films with rating over 8.5


-- And much more

-- Drop tables if recreating database.
DROP TABLE IF EXISTS actor CASCADE;
DROP TABLE IF EXISTS director CASCADE;
DROP TABLE IF EXISTS action CASCADE;
DROP TABLE IF EXISTS direction CASCADE;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS movie CASCADE;


CREATE TABLE actor (
	id SERIAL,
	name CHARACTER VARYING NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE director (
	id SERIAL,
	name CHARACTER VARYING NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE movie (
	id SERIAL,
	title CHARACTER VARYING NOT NULL,
	description CHARACTER VARYING NOT NULL,
	duration INTEGER NOT NULL,				-- Kept as minutes for ordering, displayed in this form: "hh:mm".
	release_year INTEGER NOT NULL,
	rating_imdb REAL NOT NULL,				-- IMDB rating is always a real number.
	rating_metascore INTEGER,				-- Metascore is always an integer. Not always known.
	certificate CHARACTER VARYING NOT NULL,
	gross REAL,								-- Gross is not always known. Value is in million(s) of dollars.
	vote_count INTEGER NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE action (
	actor_id INTEGER NOT NULL,
	movie_id INTEGER NOT NULL,
	PRIMARY KEY (actor_id, movie_id),
	FOREIGN KEY (actor_id) REFERENCES actor(id),
	FOREIGN KEY (movie_id) REFERENCES movie(id)
);

CREATE TABLE direction (
	director_id INTEGER NOT NULL,
	movie_id INTEGER NOT NULL,
	PRIMARY KEY (director_id, movie_id),
	FOREIGN KEY (director_id) REFERENCES director(id),
	FOREIGN KEY (movie_id) REFERENCES movie(id)
);

-- This table is needed, a movie can be of more than one genre.
CREATE TABLE genre (
	movie_id INTEGER NOT NULL,
	genre CHARACTER VARYING NOT NULL,
	PRIMARY KEY (movie_id, genre),
	FOREIGN KEY (movie_id) REFERENCES movie(id)
);

