# database.py ---
#
# Filename: database.py
# Author: Louise <louise>
# Created: Thu Feb 27 12:36:38 2020 (+0100)
# Last-Updated: Tue Mar  3 02:53:27 2020 (+0100)
#           By: Louise <louise>
#
import sys
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
    return [i[0] for i in query]

def get_products(cnx, category_id, limit):
    """
    Return `limit` items from the Products table
    that belong to the category category_id.
    We return the ID since every other field is
    not unique and can't possibly be.
    """

    statement = ("SELECT id FROM Products WHERE category=%s "
                 "ORDER BY RAND() LIMIT %s")
    cursor = cnx.cursor()
    cursor.execute(statement, (category_id, limit))
    query = cursor.fetchall()
    cursor.close()

    # Extract each item from each tuple
    return [i[0] for i in query]

def get_category_name(cnx, category_id):
    statement = "SELECT category_name FROM Categories WHERE id=%s"
    cursor = cnx.cursor()
    cursor.execute(statement, (category_id,))
    name = cursor.fetchone()[0]
    cursor.close()

    return name

def get_product_name(cnx, product_id):
    statement = "SELECT product_name FROM Products WHERE id=%s"
    cursor = cnx.cursor()
    cursor.execute(statement, (product_id, ))
    name = cursor.fetchone()[0]
    cursor.close()

    return name

def get_product_info(cnx, product_id):
    statement = "SELECT * FROM Products WHERE id=%s"
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(statement, (product_id, ))
    query = cursor.fetchone()
    cursor.close()

    return query

def get_substitute(cnx, category, product):
    statement = ("SELECT id FROM Products "
                 "WHERE (category=%s AND id<>%s) "
                 "ORDER BY nutriscore, RAND() LIMIT 1")

    cursor = cnx.cursor()
    cursor.execute(statement, (category, product))
    query = cursor.fetchone()
    cursor.close()

    # Garanteed to return a result since there is at least
    # two products in a given category
    return query[0]

def add_search(cnx, searched, given):
    statement = ("INSERT INTO Searches (product_searched, product_given) "
                 "VALUES (%s, %s)")

    cursor = cnx.cursor()
    cursor.execute(statement, (searched, given))
    cnx.commit()
    cursor.close()

def get_searches(cnx):
    statement = "SELECT product_searched, product_given FROM Searches"

    cursor = cnx.cursor()
    cursor.execute(statement)
    query = cursor.fetchall()
    cursor.close()

    return query
