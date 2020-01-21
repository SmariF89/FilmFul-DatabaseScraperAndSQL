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

# TODO: Return True/False upon success/failure of the get function.
def get_data():
    imdb_responses = []
    #for url in IMDB_URLS:
    #    imdb_responses.append(BeautifulSoup(get(url).text, 'html.parser'))

    imdb_responses.append(BeautifulSoup(get(IMDB_URLS[0], headers = {"Accept-Language": "en-US, en;q=0.5"}).text, 'html.parser'))
    return accumulate_data(imdb_responses)

# IMDB divides the movies into five pages. Their data is accummulated here into a single data structure.
# The data structure is a map where the key is the title of the film and the data is another map where the
# key is the keyed movie's attribute and the data is the attribute's value.
# Example:  MAP["12 Angry Men"][title] == "12 Angry Men"
#           MAP["American History X"]["actors"] == ["Edward Norton", "Edward Furlong", "Beverly D'Angelo", "Jennifer Lien"]
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

        # get_actors(imdb_dic, movie_item, movie_title)
        # get_directors(imdb_dic, movie_item, movie_title)
        # get_genres(imdb_dic, movie_item, movie_title)
         get_poster(imdb_dic, movie_item, movie_title)             # TODO
        # get_description(imdb_dic, movie_item, movie_title)
        # get_duration(imdb_dic, movie_item, movie_title)
        # get_release_year(imdb_dic, movie_item, movie_title)
        # get_rating_imdb(imdb_dic, movie_item, movie_title)
        # get_rating_metascore(imdb_dic, movie_item, movie_title)
        # get_certificate(imdb_dic, movie_item, movie_title)
        # get_gross(imdb_dic, movie_item, movie_title)
        # get_vote_count(imdb_dic, movie_item, movie_title)

    print(imdb_dic)
    return imdb_dic

def get_title(dic, movie):
    title = movie                                       \
        .find_next("div", class_="lister-item-content") \
        .find_next("h3")                                \
        .find_next("a")                                 \
            .get_text()

    dic[title] = {}
    dic[title]["title"] = title
    return title

def get_actors(dic, movie, title):
    dic[title]["actors"] = [tag.get_text() for tag in movie \
        .find_next("div", class_="lister-item-content")     \
        .find_all("p")[2]                                   \
        .find_next("span")                                  \
        .find_next_siblings("a")                            \
    ]

def get_directors(dic, movie, title):
    directors = [tag.get_text() for tag in movie        \
        .find_next("div", class_="lister-item-content") \
        .find_all("p")[2]                               \
        .find_next("span")                              \
        .find_previous_siblings("a")
    ]
    
    # If movie has more than one director, the scraper gets directors in reverse order. This line fixes the order.
    if len(directors) > 1:
        directors.reverse()
    dic[title]["directors"] = directors

def get_genres(dic, movie, title):
    genres_str = movie                                  \
        .find_next("div", class_="lister-item-content") \
        .find_next("p", class_="text-muted")            \
        .find_next("span", class_="genre")              \
            .get_text()
    
    # The first entry always starts with a "\" which must be removed.
    genres_str = genres_str[1:]

    # The scraping returns a string, comma separated if there is more than one genre. 
    # Then the string must be split and into a list of strings where each string must 
    # be stripped of white spaces.
    if "," in genres_str:
        dic[title]["genres"] = [genre.strip(" ") for genre in genres_str.split(",")]
    else:
        # Films with single genre sometimes have extra white spaces.
        dic[title]["genres"] = [genres_str.strip(" ")] if " " in genres_str else [genres_str]

# TODO: Implement.
def get_poster(dic, movie, title):
    return None

def get_description(dic, movie, title):
    # The second p-tag within "lister-item-content" with the class "text-muted"
    # contains the description. It has unwanted newlines and whitespaces which
    # are stripped off.
    dic[title]["description"] = movie                   \
        .find_next("div", class_="lister-item-content") \
        .find_all("p", class_="text-muted")[1]          \
            .get_text()                                 \
                .strip("\n")                            \
                .strip(" ")

def get_duration(dic, movie, title):
    # IMDB's format is e.g. "89 min" but we are only interested in the number.
    # We want to keep the number as an integer in order to order the films by
    # duration.
    dic[title]["duration"] = int(movie
        .find_next("div", class_="lister-item-content") \
        .find_next("p", class_="text-muted")            \
        .find_next("span", class_="runtime")            \
            .get_text()                                 \
                .split(" ")[0]
    )

def get_release_year(dic, movie, title):
    year_string = movie                                                     \
        .find_next("div", class_="lister-item-content")                     \
        .find_next("h3", class_="lister-item-header")                       \
        .find_next("span", class_="lister-item-year text-muted unbold")     \
            .get_text()

    # year_string sometimes contains untwanted extra characters.
    if len(year_string) > 6:
        dic[title]["release_year"] = int(                           \
            year_string.split(" ")[1]                               \
                .strip("(")                                         \
                .strip(")")                                         \
        )
    else:
        dic[title]["release_year"] = int(year_string                \
            .strip("(")                                             \
            .strip(")")                                             \
        )
    

def get_rating_imdb(dic, movie, title):
    dic[title]["rating_imdb"] = float(movie                         \
        .find_next("div", class_="lister-item-content")             \
        .find_next("div", class_="ratings-bar")                     \
        .find_next("div", class_="inline-block ratings-imdb-rating")\
        .find_next("strong")                                        \
            .get_text()                                             
    )


def get_rating_metascore(dic, movie, title):
    # Some films do not have metascore.
    
    metascore_string_tree_path = movie                          \
        .find_next("div", class_="lister-item-content")         \
        .find_next("div", class_="ratings-bar")                 \
        .find(class_="inline-block ratings-metascore")

    if metascore_string_tree_path:
        dic[title]["rating_metascore"] = int(metascore_string_tree_path
            .find_next("span").get_text().strip(" "))
    else:
        dic[title]["rating_metascore"] = None

def get_certificate(dic, movie, title):
    dic[title]["certificate"] = movie                           \
        .find_next("div", class_="lister-item-content")         \
        .find_next("p", class_="text-muted")                    \
        .find_next("span", class_="certificate")                \
            .get_text()

def get_gross(dic, movie, title):
    gross_string_tree_path = movie                              \
        .find_next("div", class_="lister-item-content")         \
        .find_next("p", class_="sort-num_votes-visible")        \
        .find_all("span", class_="text-muted")

    # If there are two span tags with class "text-muted", the gross data is available.
    if len(gross_string_tree_path) == 2:
        dic[title]["gross"] = float(gross_string_tree_path[1]   \
            .next_sibling                                       \
            .next_sibling                                       \
                .get_text()                                     \
                    .strip("$")                                 \
                    .strip("M")
        )
    else:
        dic[title]["gross"] = None

def get_vote_count(dic, movie, title):
    dic[title]["vote_count"] = int(movie                        \
        .find_next("div", class_="lister-item-content")         \
        .find_next("p", class_="sort-num_votes-visible")        \
        .find_next("span", class_="text-muted")                 \
            .next_sibling                                       \
            .next_sibling                                       \
                .get_text()                                     \
                    .replace(",", "")
    )

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