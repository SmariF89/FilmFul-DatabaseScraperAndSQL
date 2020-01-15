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
from modules.film_scraper_constants import IMDB_URL

# ===========================   Scraping functions  =========================== #

def scrape():
    if  get_actors()     and \
        get_directors()  and \
        get_movies()     and \
        get_actions()    and \
        get_directions() and \
        get_genres():
        return True
    return False

def get_actors():
    writeToFile('', '')
    return False

def get_directors():
    writeToFile('', '')
    return False

def get_movies():
    writeToFile('', '')
    return False

def get_actions():
    writeToFile('', '')
    return False

def get_directions():
    writeToFile('', '')
    return False

def get_genres():
    writeToFile('', '')
    return False

# TODO: Throw error if incorrect filename
# Expects a list of strings which will be written to a file, newline separated.
def writeToFile(file, dataToWrite):
    sep = '\n'

    f = open(file, 'w', encoding='utf-8')
    f.write(sep.join(dataToWrite))
    f.close()

def main():
    if scrape():
        print("Scrape successful!")
        return 0
    print("Scrape failed!")
    return -1

main()