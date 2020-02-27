# main.py --- 
# 
# Filename: main.py
# Author: Louise <louise>
# Created: Thu Feb 27 11:44:41 2020 (+0100)
# Last-Updated: Thu Feb 27 12:29:42 2020 (+0100)
#           By: Louise <louise>
# 
import configparser
import mysql.connector

def parse_config(file_name):
    parser = configparser.ConfigParser()
    parser.read(file_name)
    config = {i:dict(parser[i])
              for i in parser.sections()}
    
    return config

def main():
    config = parse_config("conf.ini")
    try:
        cnx = mysql.connector.connect(user=config['database']['user'],
                                      password=config['database']['password'],
                                      host=config['database']['host'],
                                      database=config['database']['database'])
    except mysql.connector.Error as error:
        if error.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Bad username or password.")
            exit()
        elif error.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist.")
            exit()
        else:
            print(error)
            exit()

    cursor = cnx.cursor()

    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()
