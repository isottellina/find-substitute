# scrape.py --- 
# This file is supposed to scrape the OpenFoodFacts database
# Filename: scrape.py
# Author: Louise <louise>
# Created: Thu Feb 27 12:33:08 2020 (+0100)
# Last-Updated: Mon Mar  2 02:20:59 2020 (+0100)
#           By: Louise <louise>
#
import database
import logging
import requests, json, mysql.connector

def scrape(cnx, lcode, ccode):
    url = "https://{ccode}-{lcode}.openfoodfacts.org/categories.json".format(
        ccode=ccode.strip(),
        lcode=lcode.strip()
    )

    req = requests.get(url)
    json_resp = json.loads(req.text)
    # Only register categories within that country and with
    # more than one product (otherwise there's really no need
    # to find a substitute)
    categories = [i for i in json_resp["tags"]
                  if (ccode + ':') in i["id"] and i["products"] > 1]
    categories_name = [i["name"] for i in categories]
    
    logging.info("Adding categories to database.")
    database.add_categories(cnx, categories_name)

    logging.info("Getting and adding product info.")

    for category in categories:
        logging.info("Scraping %s.", category["name"])
        for page_nb in range(1, (category["products"] // 20) + 2):
            category_id = database.get_category_id(cnx, category["name"])
            category_url = "{}/{}.json".format(category["url"], page_nb)
            category_page = requests.get(category_url).json()
        
            category_products = [
                {
                    "product_name": product["product_name"],
                    "nutriscore": product["nutrition_grade_fr"],
                    "category": category_id,
                    "shops": product.get("stores", ""),
                    "url": product["url"]
                }
                for product in category_page["products"]
                # We have no business with products that don't have a nutriscore
                # or even a product name, why is there products out there without
                # a product name that is beyond stupid
                if ("nutrition_grade_fr" in product and
                    "product_name" in product)
            ]
                
            database.add_products(cnx, category_products)
