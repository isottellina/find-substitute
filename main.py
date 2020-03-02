# main.py --- 
# 
# Filename: main.py
# Author: Louise <louise>
# Created: Thu Feb 27 11:44:41 2020 (+0100)
# Last-Updated: Mon Mar  2 02:49:04 2020 (+0100)
#           By: Louise <louise>
# 
import configparser, logging
import mysql.connector
import database, scrape

def parse_config(file_name):
    parser = configparser.ConfigParser()
    parser.read(file_name)
    config = {i:dict(parser[i])
              for i in parser.sections()}
    
    return config

def main():
    config = parse_config("conf.ini")
    logging.basicConfig(level=config["general"]["logging"])
    cnx = database.connect(config)

    if database.create_tables(cnx):
        logging.warning("Database non-existent, creating and scraping.")
        scrape.scrape(cnx,
                      config["openfoodfacts"]["lcode"],
                      config["openfoodfacts"]["ccode"]
        )

    cnx.close()

if __name__ == "__main__":
    main()
