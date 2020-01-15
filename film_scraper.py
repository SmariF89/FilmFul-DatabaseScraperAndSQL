# This script scrapes IMDB top 250 films, ordered alphabetically, and uses the
# gathered data to generate PostgreSQL table population script. 
# This will result in six .sql files, one for each table:
#           -   actor
#           -   director
#           -   movie
#           -   action
#           -   direction
#           -   genre

from bs4 import BeautifulSoup
from requests import get
from modules.film_scraper_constants import  IMDB_URL,               \
                                            ACTORS_SCRIPT_NAME,     \
                                            DIRECTORS_SCRIPT_NAME,  \
                                            MOVIES_SCRIPT_NAME,     \
                                            ACTIONS_SCRIPT_NAME,    \
                                            DIRECTIONS_SCRIPT_NAME, \
                                            GENRES_SCRIPT_NAME

# ===========================   Data gathering functions  =========================== #

actors = []
directors = []
movies = []
actions = []
directions = []
genres = []

def get_data():
    return  get_actors()     and \
            get_directors()  and \
            get_movies()     and \
            get_actions()    and \
            get_directions() and \
            get_genres()

def get_actors():
    actors = None
    return False

def get_directors():
    directors = None
    return False

def get_movies():
    movies = None
    return False

def get_actions():
    actions = None
    return False

def get_directions():
    directors = None
    return False

def get_genres():
    genres = None
    return False

# ===========================   SQL generation functions  =========================== #

def generate_sql_population_scripts():
    return  generate_actors_sql()     and \
            generate_directors_sql()  and \
            generate_movies_sql()     and \
            generate_actions_sql()    and \
            generate_directions_sql() and \
            generate_genres_sql()

def generate_actors_sql():
    writeToFile('', '')
    return False

def generate_directors_sql():
    writeToFile('', '')
    return False

def generate_movies_sql():
    writeToFile('', '')
    return False

def generate_actions_sql():
    writeToFile('', '')
    return False

def generate_directions_sql():
    writeToFile('', '')
    return False

def generate_genres_sql():
    writeToFile('', '')
    return False

# ===========================   Utility functions  =========================== #

# TODO: Throw error if incorrect filename
# Expects a list of strings which will be written to a file, newline separated.
def writeToFile(file, dataToWrite):
    sep = '\n'

    f = open(file, 'w', encoding='utf-8')
    f.write(sep.join(dataToWrite))
    f.close()

# ===========================   Script root   =========================== #

def main():
    if get_data() and generate_sql_population_scripts():
        print("Scrape successful!")
        return 0
    print("Scrape failed!")
    return -1

main()