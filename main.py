# main.py --- 
# 
# Filename: main.py
# Author: Louise <louise>
# Created: Thu Feb 27 11:44:41 2020 (+0100)
# Last-Updated: Thu Feb 27 12:38:07 2020 (+0100)
#           By: Louise <louise>
# 
import configparser
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
    cnx = database.connect(config)
    cursor = cnx.cursor()

    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()
