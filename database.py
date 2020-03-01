# database.py --- 
# 
# Filename: database.py
# Author: Louise <louise>
# Created: Thu Feb 27 12:36:38 2020 (+0100)
# Last-Updated: Mon Mar  2 00:13:52 2020 (+0100)
#           By: Louise <louise>
#
import logging
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

def create_tables(cnx):
    cursor = cnx.cursor()

    with open("creation.sql", "r") as file:
        query = file.read()
        # Iterate to execute all statements
        for result in cursor.execute(query, multi = True):
            pass
    
    cursor.close()

def add_categories(cnx, names):
    statement = "INSERT INTO Categories (category_name) VALUES (%s)"
    cursor = cnx.cursor()
    # We have to transmute every list element into a singleton for the request
    logging.info("Adding %d elements to the database.", len(names))
    cursor.executemany(statement, ((name,) for name in names))
    cnx.commit()
    cursor.close()

def get_category_id(cnx, name):
    statement = "SELECT (id) FROM Categories WHERE category_name=%s"
    cursor = cnx.cursor()
    cursor.execute(statement, (name,))
    id = cursor.fetchone()[0]
    cursor.close()

    return id

def add_products(cnx, products):
    """
    The product argument is a dictionary comprising of:
     - product_name
     - nutriscore (one character)
     - category (the ID of the category)
     - shops (an URL)
     - url (that of the product)
    """
    statement = (
        "INSERT INTO Products"
        "(product_name, nutriscore, category, shops, url) "
        "VALUES (%(product_name)s, %(nutriscore)s, "
        "%(category)s, %(shops)s, %(url)s)"
    )
    cursor = cnx.cursor()
    cursor.executemany(statement, products)
    cnx.commit()
    cursor.close()
