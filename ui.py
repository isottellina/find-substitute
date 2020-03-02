# ui.py --- 
# 
# Filename: ui.py
# Author: Louise <louise>
# Created: Mon Mar  2 22:35:19 2020 (+0100)
# Last-Updated: Tue Mar  3 00:40:44 2020 (+0100)
#           By: Louise <louise>
# 
import database

def get_number(prompt, ran):
    number = input(prompt)
    while not number.isdigit() or int(number) not in ran:
        number = input(prompt)
    return int(number)

def find_substitute(cnx):
    # Choose a category
    cats = database.get_categories(cnx, 30)
    print("Choisissez une catégorie :")
    for n, cat in enumerate(cats):
        print("[{}] {}".format(
            str(n + 1).zfill(2),
            database.get_category_name(cnx, cat)
        ))
    # A number has to be chosen between 0 and 30 (excluded)
    chosen_cat = get_number("? ", range(1, 31)) - 1
    
    prods = database.get_products(cnx, cats[chosen_cat], 30)
    print("Choissez un produit :")
    for n, prod in enumerate(prods):
        print("[{}] {}".format(
            str(n + 1).zfill(2),
            database.get_product_name(cnx, prod)
        ))
    chosen_prod = get_number("? ", range(1, 31)) - 1

    # Find a substitute
    sub = database.get_substitute(cnx, cats[chosen_cat], prod)
    sub_info = database.get_product_info(cnx, sub)
    print("Substitut trouvé:")
    print("Nom :", sub_info["product_name"])
    print("Où l'acheter:",
          sub_info["shops"] if sub_info["shops"] else "Inconnu")
    print("Page OpenFoodFacts:", sub_info["url"])

def main_menu(cnx):
    print("1 - Quel aliment souhaitez-vous remplacer ?")
    print("2 - Retrouver mes aliments substitués.")
    choice = get_number("Quel choix choisissez-vous ? ", range(1, 3))
    if choice == 1:
        find_substitute(cnx)
    elif choice == 2:
        recite_substitutes(cnx)
