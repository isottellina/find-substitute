# database.py --- 
# 
# Filename: database.py
# Author: Louise <louise>
# Created: Thu Feb 27 12:36:38 2020 (+0100)
# Last-Updated: Thu Feb 27 13:49:16 2020 (+0100)
#           By: Louise <louise>
# 
import mysql.connector

def connect(config):
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
    return cnx
