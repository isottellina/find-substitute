# ui.py --- 
# 
# Filename: ui.py
# Author: Louise <louise>
# Created: Mon Mar  2 22:35:19 2020 (+0100)
# Last-Updated: Tue Mar  3 02:22:07 2020 (+0100)
#           By: Louise <louise>
# 
import database

def get_number(prompt, ran):
    number = input(prompt)
    while not number.isdigit() or int(number) not in ran:
        number = input(prompt)
    return int(number)

def print_product_info(info):
    print("Nom :", info["product_name"])
    print("Où l'acheter :",
          info["shops"] if info["shops"] else "Inconnu")
    print("Page OpenFoodFacts :", info["url"])

def choose_category(cnx):
    cats = database.get_categories(cnx, 30)
    print("Choisissez une catégorie :")
    for n, cat in enumerate(cats):
        print("[{}] {}".format(
            str(n + 1).zfill(2),
            database.get_category_name(cnx, cat)
        ))
    # A number has to be chosen between 0 and 30 (excluded)
    chosen_cat = get_number("? ", range(1, 31)) - 1
    
    return cats[chosen_cat]

def choose_product(cnx, cat):
    prods = database.get_products(cnx, cat, 30)
    print("Choissez un produit :")
    for n, prod in enumerate(prods):
        print("[{}] {}".format(
            str(n + 1).zfill(2),
            database.get_product_name(cnx, prod)
        ))
    chosen_prod = get_number("? ", range(1, 31)) - 1

    return prods[chosen_prod]

def save_search(cnx, searched, given):
    print("Voulez-vous enregistrer cette recherche dans la base de données ?")
    print("[1] Oui")
    print("[2] Non")
    choice = get_number("? ", range(1, 3))

    if choice == 1:
        database.add_search(cnx, searched, given)

def find_substitute(cnx):
    # Choose a product
    cat = choose_category(cnx)
    prod = choose_product(cnx, cat)
    
    # Find a substitute
    sub = database.get_substitute(cnx, cats[chosen_cat], prods[chosen_prod])
    sub_info = database.get_product_info(cnx, sub)
    print("Substitut trouvé :")
    print_product_info(sub_info)
    
    # Save it to the database (or not)
    save_search(cnx, prod, sub)

def recite_substitutes(cnx):
    schs = database.get_searches(cnx)
    for search in schs:
        product_searched, product_given = search
        sub_info = database.get_product_info(cnx, product_given)
        print("Substitut pour :", database.get_product_name(cnx, product_searched))
        print_product_info(sub_info)
        print()
        
def main_menu(cnx):
    print("[1] Quel aliment souhaitez-vous remplacer ?")
    print("[2] Retrouver mes aliments substitués.")
    choice = get_number("Quel choix choisissez-vous ? ", range(1, 3))
    if choice == 1:
        find_substitute(cnx)
    elif choice == 2:
        recite_substitutes(cnx)
