IMDB_URLS = [ "https://www.imdb.com/search/title/?groups=top_250&sort=alpha,asc",
              "https://www.imdb.com/search/title/?groups=top_250&sort=alpha,asc&start=51&ref_=adv_nxt",
              "https://www.imdb.com/search/title/?groups=top_250&sort=alpha,asc&start=101&ref_=adv_nxt",
              "https://www.imdb.com/search/title/?groups=top_250&sort=alpha,asc&start=151&ref_=adv_nxt",
              "https://www.imdb.com/search/title/?groups=top_250&sort=alpha,asc&start=201&ref_=adv_nxt"]

# IMDB_URLS = [ "https://www.imdb.com/search/title/?groups=top_250&sort=alpha,asc"]     # Use this while developing and testing.

ACTORS_SCRIPT_NAME = "FILL_ACTOR.sql"
DIRECTORS_SCRIPT_NAME = "FILL_DIRECTOR.sql"
MOVIES_SCRIPT_NAME = "FILL_MOVIE.sql"
ACTIONS_SCRIPT_NAME = "FILL_ACTION.sql"
DIRECTIONS_SCRIPT_NAME = "FILL_DIRECTION.sql"
GENRES_SCRIPT_NAME = "FILL_GENRE.sql"

ACTOR_SCRIPT_START = """INSERT INTO actor(name) VALUES\n"""
DIRECTOR_SCRIPT_START = """INSERT INTO director(name) VALUES\n"""
ACTION_SCRIPT_START = """INSERT INTO action(actor_id, movie_id) VALUES\n"""
DIRECTION_SCRIPT_START = """INSERT INTO direction(director_id, movie_id) VALUES\n"""
GENRE_SCRIPT_START = """INSERT INTO genre(movie_id, genre) VALUES\n"""
MOVIE_SCRIPT_START = """INSERT INTO movie(title, poster, description, duration, release_year, rating_imdb,\nrating_metascore, certificate, gross, vote_count) VALUES\n"""