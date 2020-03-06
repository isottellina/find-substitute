# scrape.py ---
# This file is supposed to scrape the OpenFoodFacts database
# Filename: scrape.py
# Author: Louise <louise>
# Created: Thu Feb 27 12:33:08 2020 (+0100)
# Last-Updated: Fri Mar  6 00:49:38 2020 (+0100)
#           By: Louise <louise>
#
import logging
import requests
from database import Category, Product

def scrape_categories(lcode, ccode):
    """
    This function returns a tuple of:
     - a list of dictionaries representing the categories
     - the same list but containing only their name
    """
    url = "https://{ccode}-{lcode}.openfoodfacts.org/categories.json".format(
        ccode=ccode.strip(),
        lcode=lcode.strip()
    )

    req = requests.get(url)
    json_resp = req.json()
    # Only register categories within that country and with
    # more than one product (otherwise there's really no need
    # to find a substitute)
    categories = [i for i in json_resp["tags"]
                  if ccode + ':' in i["id"] and i["products"] > 1]
    categories_name = [i["name"] for i in categories]
    return categories, categories_name

def scrape_products(category_json, category_id):
    """
    This function scrapes all scrapable products from a given
    category, and returns a list of dictionaries.
    """
    logging.info("Scraping %s.", category_json["name"])
    category_products = []

    for page_nb in range(1, (category_json["products"] // 20) + 2):
        category_url = "{}/{}.json".format(category_json["url"], page_nb)
        category_page = requests.get(category_url).json()

        category_products += [
            {
                "product_name": product["product_name"],
                "nutriscore": product["nutrition_grade_fr"],
                "category": category_id,
                "shops": product.get("stores", ""),
                "url": product["url"]
            }
            for product in category_page["products"]
            # We have no business with products that don't have a nutriscore
            # or even a product name, why are there products out there without
            # a product name that's beyond idiotic I can't even
            if ("nutrition_grade_fr" in product
                and "product_name" in product
                and product["product_name"])
        ]

    return category_products

def scrape(cnx, lcode, ccode):
    """
    This function scrapes all it can scrape from the API, first
    the categories then all the usable products in them. It removes
    the category if it turns out to be empty once all the useless
    products weeded out (like the ones without a nutriscore or a
    name).
    """
    logging.info("Getting and adding category info")
    categories, categories_name = scrape_categories(lcode, ccode)
    Category.add_bulk(cnx, categories_name)

    logging.info("Getting and adding product info.")
    for category_json in categories:
        category = Category.from_name(cnx, category_json["name"])
        products = scrape_products(category_json, category.id)

        # We only register the products if there is 2 or more products
        # after they have been filtered, or else there is no point.
        # If there is no point we might as well remove the category.
        if len(products) > 1:
            Product.add_products(cnx, products)
        else:
            category.remove(cnx)
