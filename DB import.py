# -*- coding: utf8 -*-

import requests
import json

from Classes import Database
from constants import *

for categorie in CATEGORIES_TO_IMPORT:
    i=0
    while i<PAGES_TO_IMPORT:
        a = requests.get("https://fr.openfoodfacts.org/categorie/"+categorie+"/"+str(i)+".json")
        with open(categorie+str(i)+".json", 'w') as fd:
            json.dump(a.json(), fd)
        i+=1

p5oc = Database("p5oc", "program", "program", "127.0.0.1")
for categorie in CATEGORIES_TO_IMPORT:
    i=0
    while i<PAGES_TO_IMPORT:
        data = {}
        with open(categorie+str(i)+".json") as f:
            data = json.load(f)

        for product in data["products"]:
            if (product["lang"] == "fr") and ("brands" in product) and ("nutrition_grades" in product) and ("nova_groups" in product):
                try:
                    p5oc.add("food_item", ("id_openfoodfacts", "food_name", "food_brand", "food_generic_name", "nutriscore", "nova_grade"), 
                            (product["id"], product["product_name"], product["brands"], product["generic_name_fr"], product["nutrition_grades"],
                            product["nova_groups"]))
                    p5oc.add("category", ["name"], [categorie])
                    p5oc.add("food_item_category", ["food_item_id_openfoodfacts", "category_name"], [product["id"], categorie])
                    if product["stores"] != "":
                        stores = product["stores"].split(",")
                        for store in stores:
                            p5oc.add("store", ["name"], [store])
                            p5oc.add("food_item_store", ("food_item_id_openfoodfacts", "store_name"), (product["id"], store))
                except:
                    pass
        i+=1