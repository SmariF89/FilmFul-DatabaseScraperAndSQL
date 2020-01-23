# This script scrapes IMDB top 250 films, ordered alphabetically, and uses the
# gathered data to generate PostgreSQL table population script. 
# This will result in six .sql files, one for each table:
#           -   actor
#           -   director
#           -   movie
#           -   action
#           -   direction
#           -   genre

from base64 import b64encode
from binascii import hexlify
from bs4 import BeautifulSoup
from io import BytesIO
from os import path, remove
from requests import get

from modules.film_scraper_constants import  IMDB_URLS,              \
                                            ACTORS_SCRIPT_NAME,     \
                                            DIRECTORS_SCRIPT_NAME,  \
                                            MOVIES_SCRIPT_NAME,     \
                                            ACTIONS_SCRIPT_NAME,    \
                                            DIRECTIONS_SCRIPT_NAME, \
                                            GENRES_SCRIPT_NAME,     \
                                            ACTOR_SCRIPT_START,     \
                                            DIRECTOR_SCRIPT_START,  \
                                            ACTION_SCRIPT_START,    \
                                            DIRECTION_SCRIPT_START, \
                                            GENRE_SCRIPT_START,     \
                                            MOVIE_SCRIPT_START

# ===========================   Data gathering functions  =========================== #

# TODO: Return True/False upon success/failure of the get function.
def get_data():
    imdb_responses = []
    for url in IMDB_URLS:
        imdb_responses.append(BeautifulSoup(get(url, headers = {"Accept-Language": "en-US, en;q=0.5"}).text, 'html.parser'))

    # There are five pages that need to be scraped. If we got less than five responses,
    # one of the requests must have failed.
    """if len(imdb_responses) < 5:
        return False"""

    return (True, accumulate_data(imdb_responses))

# IMDB divides the movies into five pages. Their data is accummulated here into a single data structure.
# The data structure is a map where the key is the title of the film and the data is another map where the
# key is the keyed movie's attribute and the data is the attribute's value.
# Examples:  MAP["12 Angry Men"][title] == "12 Angry Men"
#            MAP["American History X"]["actors"] == ["Edward Norton", "Edward Furlong", "Beverly D'Angelo", "Jennifer Lien"]
def accumulate_data(imdb_responses):
    imdb_dic = {}
    
    # For every page of IMDB Top 250 we iterate through every movie. 5 * 50 = 250 movies.
    for page in imdb_responses:
        for movie_item in page.find_all("div", class_="lister-item mode-advanced"):
            movie_title = get_title(imdb_dic, movie_item)
            get_actors(imdb_dic, movie_item, movie_title)
            get_directors(imdb_dic, movie_item, movie_title)
            get_genres(imdb_dic, movie_item, movie_title)
            # get_poster(imdb_dic, movie_item, movie_title)         # Takes a long time. Don't execute during development and testing.
            get_poster_dev(imdb_dic, movie_item, movie_title)            # Use this one instead while developing and testing.
            get_description(imdb_dic, movie_item, movie_title)
            get_duration(imdb_dic, movie_item, movie_title)
            get_release_year(imdb_dic, movie_item, movie_title)
            get_rating_imdb(imdb_dic, movie_item, movie_title)
            get_rating_metascore(imdb_dic, movie_item, movie_title)
            get_certificate(imdb_dic, movie_item, movie_title)
            get_gross(imdb_dic, movie_item, movie_title)
            get_vote_count(imdb_dic, movie_item, movie_title)

    return imdb_dic

# NOTE: PostgreSQL is not a fan of single quotes. Thus, they must be
#       escaped so that the script is accepted by PostgreSQL.

def get_title(dic, movie):
    title = movie                                       \
        .find_next("div", class_="lister-item-content") \
        .find_next("h3")                                \
        .find_next("a")                                 \
            .get_text()

    dic[title] = {}
    dic[title]["title"] = title if "'" not in title else title.replace("'", "''")       # Single quotes taken care of.
    return title

# Note: Single quotes are taken care of in sql generation function for actors.
def get_actors(dic, movie, title):
    dic[title]["actors"] = [tag.get_text() for tag in movie \
        .find_next("div", class_="lister-item-content")     \
        .find_all("p")[2]                                   \
        .find_next("span")                                  \
        .find_next_siblings("a")                            \
    ]

# Note: Single quotes are taken care of in sql generation function for directors.
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

# Note: None of the genres contain single quotes.
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

# Use this function instead of get_poster when developing.
def get_poster_dev(dic, movie, title):
    dic[title]["poster"] = "!!!DUMMY_POSTER!!!"

def get_poster(dic, movie, title):
    poster_url = movie                                              \
        .find_next("div", class_="lister-item-image float-left")    \
        .find_next("img")                                           \
            .get("loadlate")
    
    # For each image url, we download the image binary data (bytes), 
    # write it to a buffer, move the cursor to the first byte, read
    # the information, convert it to base64 string and finally it is
    # saved to our dictionary.
    poster_byte_arr = BytesIO()
    poster_response = get(poster_url)
    if poster_response.status_code == 200:
        for chunk in poster_response:
            poster_byte_arr.write(chunk)

    poster_byte_arr.seek(0)
    dic[title]["poster"] = str(b64encode(poster_byte_arr.read())).replace("'", "''")

def get_description(dic, movie, title):
    # The second p-tag within "lister-item-content" with the class "text-muted"
    # contains the description. It has unwanted newlines and whitespaces which
    # are stripped off.
    dic[title]["description"] = movie                   \
        .find_next("div", class_="lister-item-content") \
        .find_all("p", class_="text-muted")[1]          \
            .get_text()                                 \
                .strip("\n")                            \
                .strip(" ")                             \
                .replace("'", "''")

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
        dic[title]["rating_metascore"] = "NULL"

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
        dic[title]["gross"] = "NULL"

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

def generate_sql_population_scripts(imdb_data):
    return  generate_actors_sql(imdb_data)     and   \
            generate_directors_sql(imdb_data)  and   \
            generate_movies_sql(imdb_data)     and   \
            """generate_actions_sql(imdb_data)    and   \
            generate_directions_sql(imdb_data) and   \
            generate_genres_sql(imdb_data)"""

def generate_actors_sql(imdb_data):
    # Delete script if it already exists.
    if path.exists(ACTORS_SCRIPT_NAME):
        remove(ACTORS_SCRIPT_NAME)
    
    # First step is to get all actors without duplication. A set does the trick.
    actor_set = set()

    for film in imdb_data.keys():
        for actor in imdb_data[film]["actors"]:
            actor_set.add(actor)

    # PostgreSQL requires that single quotes are escaped by using double single quotes.
    # This is for names like "Beverly D'Angelo".
    actor_list = [a.replace("'", "''") for a in sorted(actor_set)]
    actor_num = len(actor_list)

    f = open(ACTORS_SCRIPT_NAME, 'a', encoding='utf-8')
    f.write(ACTOR_SCRIPT_START)
    for index in range(actor_num):
        f.write("(\'" + actor_list[index] + "\')" + ("\n," if index < (actor_num - 1) else ";"))
    f.close()

    return True

def generate_directors_sql(imdb_data):
    # Delete script if it already exists.
    if path.exists(DIRECTORS_SCRIPT_NAME):
        remove(DIRECTORS_SCRIPT_NAME)

    # First step is to get all directors without duplication. A set does the trick.
    director_set = set()

    for film in imdb_data.keys():
        for director in imdb_data[film]["directors"]:
            director_set.add(director)

    # PostgreSQL requires that single quotes are escaped by using double single quotes.
    # This is for names like "Beverly D'Angelo".
    director_list = [d.replace("'", "''") for d in sorted(director_set)]
    director_num = len(director_list)

    f = open(DIRECTORS_SCRIPT_NAME, 'a', encoding='utf-8')
    f.write(DIRECTOR_SCRIPT_START)
    for index in range(director_num):
        f.write("(\'" + director_list[index] + "\')" + ("\n," if index < (director_num - 1) else ";"))
    f.close()

    return True

# INSERT INTO movie(title, poster, description, duration, release_year, rating_imdb\nrating_metascore, certificate, gross, vote_count) VALUES\n
def generate_movies_sql(imdb_data):
    # Delete script if it already exists.
    if path.exists(MOVIES_SCRIPT_NAME):
        remove(MOVIES_SCRIPT_NAME)

    movie_keys = imdb_data.keys()
    movie_num = len(movie_keys)
    progress = 0
    
    f = open(MOVIES_SCRIPT_NAME, 'a', encoding='utf-8')
    f.write(MOVIE_SCRIPT_START)
    for movie in movie_keys:
        f.write("(" + "\'" + imdb_data[movie]["title"] + "\', \'" + imdb_data[movie]["poster"] + "\', \'" + imdb_data[movie]["description"] + "\', " + str(imdb_data[movie]["duration"]) + ", " + str(imdb_data[movie]["release_year"]) + ", " + str(imdb_data[movie]["rating_imdb"]) + ", " + str(imdb_data[movie]["rating_metascore"]) + ", \'" + imdb_data[movie]["certificate"] + "\', " + str(imdb_data[movie]["gross"]) + ", " + str(imdb_data[movie]["vote_count"]) + ")" + ("\n," if progress < (movie_num - 1) else ";"))
        progress += 1
    f.close()

    return True

def generate_actions_sql(imdb_data):
    # Delete script if it already exists.
    if path.exists(ACTIONS_SCRIPT_NAME):
        remove(ACTIONS_SCRIPT_NAME)

    return True

def generate_directions_sql(imdb_data):
    # Delete script if it already exists.
    if path.exists(DIRECTIONS_SCRIPT_NAME):
        remove(DIRECTIONS_SCRIPT_NAME)

    return True

def generate_genres_sql(imdb_data):
    # Delete script if it already exists.
    if path.exists(GENRES_SCRIPT_NAME):
        remove(GENRES_SCRIPT_NAME)

    return True

# ===========================   Script root   =========================== #

def main():
    imdb_data = get_data()
    if imdb_data[0] and generate_sql_population_scripts(imdb_data[1]):
        print("Scripts generated successfully!")
        return 0
    print("Failed to generate scripts!")
    return -1

main()