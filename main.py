# main.py ---
#
# Filename: main.py
# Author: Louise <louise>
# Created: Thu Feb 27 11:44:41 2020 (+0100)
# Last-Updated: Fri Mar  6 16:05:14 2020 (+0100)
#           By: Louise <louise>
#
import logging
import configparser
from database import connect, create_tables
from scrape import Scraper
from ui import main_menu

# Config
def parse_config(file_name):
    """Loads and parses the config file."""
    parser = configparser.ConfigParser()
    parser.read(file_name)
    config = {i:dict(parser[i])
              for i in parser.sections()}

    return config

def main():
    """
    Main function. Basic configuration and firing up
    the more pertinent functions.
    """
    config = parse_config("conf.ini")
    logging.basicConfig(level=config["general"]["logging"])
    cnx = connect(config)

    if create_tables(cnx):
        logging.warning("Database non-existent, creating and scraping.")
        scraper = Scraper(config["openfoodfacts"]["lcode"],
                          config["openfoodfacts"]["ccode"])
        scraper.scrape(cnx)

    main_menu(cnx)
    cnx.close()

if __name__ == "__main__":
    main()
