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

from modules.film_scraper_constants import  IMDB_URLS,              \
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
    imdb_responses = []
    #for url in IMDB_URLS:
    #    imdb_responses.append(BeautifulSoup(get(url).text, 'html.parser'))

    imdb_responses.append(BeautifulSoup(get(IMDB_URLS[0]).text, 'html.parser'))
    imdb_data = accumulate_data(imdb_responses)

    return  get_actors(imdb_data)     and \
            get_directors(imdb_data)  and \
            get_movies(imdb_data)     and \
            get_actions(imdb_data)    and \
            get_directions(imdb_data) and \
            get_genres(imdb_data)

# IMDB divides the movies into five pages. Their data is accummulated here into a single data structure.
# The data structure is a map where the key is the name of the film and the data is another map where the
# key is the keyed movie's attribute and the data is the attribute's value.
# Example:  MAP["12 Angry Men"][name] == "12 Angry Men"
#           MAP["American History X"][actors] == ["Edward Norton", "Edward Furlong", "Beverly D'Angelo", "Jennifer Lien"]
def accumulate_data(data):
    # Gets first item's number (1.)
    # data[0].find_all("div", class_="lister-item-content")[0].find_all("span")[0].get_text()

    

    return False

def get_actors(data):
    actors = None
    return False

def get_directors(data):
    directors = None
    return False

def get_movies(data):
    movies = None
    return False

def get_actions(data):
    actions = None
    return False

def get_directions(data):
    directors = None
    return False

def get_genres(data):
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
        print("Scripts generated successfully!")
        return 0
    print("Failed to generate scripts!")
    return -1

main()