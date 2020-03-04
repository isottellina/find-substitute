# database.py ---
#
# Filename: database.py
# Author: Louise <louise>
# Created: Thu Feb 27 12:36:38 2020 (+0100)
# Last-Updated: Thu Mar  5 00:09:51 2020 (+0100)
#           By: Louise <louise>
#
import sys
import logging
import mysql.connector

class Category:
    def __init__(self, cnx, category_id):
        statement = "SELECT category_name FROM Categories WHERE id=%s"
        self.id = category_id
        cursor = cnx.cursor(dictionary = True)
        cursor.execute(statement, (category_id, ))

        self.name = cursor.fetchone()['category_name']

        cursor.close()

class Product:
    def __init__(self, cnx, product_id):
        statement = "SELECT * FROM Products WHERE id=%s"
        self.id = product_id
        cursor = cnx.cursor(dictionary = True)
        cursor.execute(statement, (product_id, ))
        query = cursor.fetchone()

        self.name = query['product_name']
        self.nutriscore = query['nutriscore']
        self.category = Category(cnx, query['category'])
        self.shops = query['shops']
        self.url = query['url']

        cursor.close()

class Search:
    def __init__(self, cnx, search_id):
        statement = "SELECT * FROM Searches WHERE id=%s"
        self.id = search_id
        cursor = cnx.cursor(dictionary = True)
        cursor.execute(statement, (search_id, ))
        query = cursor.fetchone()

        self.product_searched = Product(cnx, query['product_searched'])
        self.product_given = Product(cnx, query['product_given'])

        cursor.close()
        
def connect(config):
    try:
        cnx = mysql.connector.connect(user=config['database']['user'],
                                      password=config['database']['password'],
                                      host=config['database']['host'],
                                      database=config['database']['database'])
    except mysql.connector.Error as error:
        if error.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Bad username or password.")
            sys.exit()
        elif error.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist.")
            sys.exit()
        else:
            print(error)
            sys.exit()
    return cnx

def create_tables(cnx):
    cursor = cnx.cursor()
    cursor.execute("SHOW TABLES;")
    if (("Categories",) in cursor
            and ("Products",) in cursor
            and ("Searches",) in cursor):
        return False

    with open("creation.sql", "r") as file:
        query = file.read()
        # Iterate to execute all statements
        for _ in cursor.execute(query, multi=True):
            pass

    cursor.close()
    return True

# Scraping functions
def add_categories(cnx, names):
    statement = "INSERT INTO Categories (category_name) VALUES (%s)"
    cursor = cnx.cursor()
    # We have to transmute every list element into a singleton for the request
    logging.info("Adding %d elements to the database.", len(names))
    cursor.executemany(statement, ((name,) for name in names))
    cnx.commit()
    cursor.close()

def remove_category(cnx, category_id):
    """
    Remove a category from the table.
    """

    statement = "DELETE FROM Categories WHERE id=%s"
    cursor = cnx.cursor()
    cursor.execute(statement, (category_id, ))
    cnx.commit()
    cursor.close()

def get_category_id(cnx, name):
    statement = "SELECT (id) FROM Categories WHERE category_name=%s"
    cursor = cnx.cursor()
    cursor.execute(statement, (name,))
    category_id = cursor.fetchone()[0]
    cursor.close()

    return category_id

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

# Use functions
def get_categories(cnx, limit):
    """
    Return `limit` items from the Categories table.
    """

    statement = "SELECT id FROM Categories ORDER BY RAND() LIMIT %s"
    cursor = cnx.cursor()
    cursor.execute(statement, (limit,))
    query = cursor.fetchall()
    cursor.close()

    # Extract each item from each tuple in the list
    return [Category(cnx, i[0]) for i in query]

def get_products(cnx, category, limit):
    """
    Return `limit` items from the Products table
    that belong to the category category_id.
    We return the ID since every other field is
    not unique and can't possibly be.
    """

    statement = ("SELECT id FROM Products WHERE category=%s "
                 "ORDER BY RAND() LIMIT %s")
    cursor = cnx.cursor()
    cursor.execute(statement, (category.id, limit))
    query = cursor.fetchall()
    cursor.close()

    # Extract each item from each tuple
    return [Product(cnx, i[0]) for i in query]

def get_substitute(cnx, category, product):
    statement = ("SELECT id FROM Products "
                 "WHERE (category=%s AND id<>%s) "
                 "ORDER BY nutriscore, RAND() LIMIT 1")

    cursor = cnx.cursor()
    cursor.execute(statement, (category.id, product.id))
    query = cursor.fetchone()
    cursor.close()

    # Garanteed to return a result since there is at least
    # two products in a given category
    return Product(cnx, query[0])

def add_search(cnx, searched, given):
    statement = ("INSERT INTO Searches (product_searched, product_given) "
                 "VALUES (%s, %s)")

    cursor = cnx.cursor()
    cursor.execute(statement, (searched.id, given.id))
    cnx.commit()
    cursor.close()

def get_searches(cnx):
    statement = "SELECT id FROM Searches"

    cursor = cnx.cursor()
    cursor.execute(statement)
    query = cursor.fetchall()
    cursor.close()

    return [Search(cnx, i[0]) for i in query]
