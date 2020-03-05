# main.py ---
#
# Filename: main.py
# Author: Louise <louise>
# Created: Thu Feb 27 11:44:41 2020 (+0100)
# Last-Updated: Thu Mar  5 23:57:18 2020 (+0100)
#           By: Louise <louise>
#
import logging
import configparser
import database
import scrape
import ui

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
    cnx = database.connect(config)

    if database.create_tables(cnx):
        logging.warning("Database non-existent, creating and scraping.")
        scrape.scrape(cnx,
                      config["openfoodfacts"]["lcode"],
                      config["openfoodfacts"]["ccode"])

    ui.main_menu(cnx)
    cnx.close()

if __name__ == "__main__":
    main()
