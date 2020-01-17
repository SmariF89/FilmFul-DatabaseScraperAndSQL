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

def get_data():
    imdb_responses = []
    #for url in IMDB_URLS:
    #    imdb_responses.append(BeautifulSoup(get(url).text, 'html.parser'))

    imdb_responses.append(BeautifulSoup(get(IMDB_URLS[0], headers = {"Accept-Language": "en-US, en;q=0.5"}).text, 'html.parser'))
    return accumulate_data(imdb_responses)

# IMDB divides the movies into five pages. Their data is accummulated here into a single data structure.
# The data structure is a map where the key is the title of the film and the data is another map where the
# key is the keyed movie's attribute and the data is the attribute's value.
# Example:  MAP["12 Angry Men"][name] == "12 Angry Men"
#           MAP["American History X"][actors] == ["Edward Norton", "Edward Furlong", "Beverly D'Angelo", "Jennifer Lien"]
def accumulate_data(data):
    imdb_dic = {}

    # Gets first item
    # data[0].find_all("div", class_="lister-item-content")[0]

    # Gets first item's number (1.)
    # data[0].find_all("div", class_="lister-item-content")[0].find_all("span")[0].get_text()

    # Gets all items' names
    # for x in data[0].find_all("div", class_="lister-item-content"):
    #     print(x.find_next("h3").find_next("a").get_text())
  
    for movie_item in data[0].find_all("div", class_="lister-item mode-advanced"):
        movie_title = get_title(imdb_dic, movie_item)

        get_actors(imdb_dic, movie_item, movie_title)
        get_directors(imdb_dic, movie_item, movie_title)
        get_genres(imdb_dic, movie_item, movie_title)
        get_poster(imdb_dic, movie_item, movie_title)
        get_description(imdb_dic, movie_item, movie_title)
        get_duration(imdb_dic, movie_item, movie_title)
        get_release_year(imdb_dic, movie_item, movie_title)
        get_rating_imdb(imdb_dic, movie_item, movie_title)
        get_rating_metascore(imdb_dic, movie_item, movie_title)
        get_certificate(imdb_dic, movie_item, movie_title)
        get_gross(imdb_dic, movie_item, movie_title)
        get_vote_count(imdb_dic, movie_item, movie_title

    print(imdb_dic)
    return imdb_dic

def get_title(dic, movie):
    title = movie.find_next("div", class_="lister-item-content").find_next("h3").find_next("a").get_text()
    dic[title] = title
    return title

def get_actors(dic, movie, title):
    return False

def get_directors(dic, movie, title):
    return False

def get_genres(dic, movie, title):
    return False


def get_poster(dic, movie, title):
    return False

def get_description(dic, movie, title):
    return False

def get_duration(dic, movie, title):
    return False

def get_release_year(dic, movie, title):
    return False

def get_rating_imdb(dic, movie, title):
    return False

def get_rating_metascore(dic, movie, title):
    return False

def get_certificate(dic, movie, title):
    return False

def get_gross(dic, movie, title):
    return False

def get_vote_count(dic, movie, title):
    return False

# ===========================   SQL generation functions  =========================== #

def generate_sql_population_scripts():
    """return  generate_actors_sql()     and \
            generate_directors_sql()  and \
            generate_movies_sql()     and \
            generate_actions_sql()    and \
            generate_directions_sql() and \
            generate_genres_sql()"""

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