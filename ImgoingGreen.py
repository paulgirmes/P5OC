"""
Program that allows to find healthier food replacement by interacting
with a database please see README.md
"""

# -*- coding: utf8 -*-
from classes import Database
from constants import *


p5oc = Database(DATABASE_NAME, USER_NAME, USER_PWD, URL)


def main():
    """
    displays the main menu(console interactions only)
    """
    i = 1
    while i:
        answer = input(
            "veuillez choisir une option :\n\n"
            "[1] : effectuer une nouvelle recherche\n"
            "[2] : consulter les aliments sauvegardés\n[3] : Quitter\n"
        )
        if answer == "3":
            print("Au revoir !\n\n")
            i = 0
        elif answer == "1":
            new_search()
        elif answer == "2":
            saved_searches()
        else:
            print("\nMerci de taper un chiffre parmis les choix proposés\n")


def new_search():
    """
    Makes a database search for an healthier food_item from the choosen foo-item category
    """
    food_categories = p5oc.get_all("category")
    cat = []
    for item in food_categories:
        cat.append("[" + str(food_categories.index(item)) + "] : " + str(item))
    choosen_category = menu(
        ("\nVeuillez choisir une categorie :\n\n" + "\n".join(cat) + "\n\n"),
        food_categories,
    )
    food_items = p5oc.get_food_items(food_categories[int(choosen_category)])
    f_i = []
    k = 0
    for item in food_items:
        f_i.append("[" + str(k) + "] : " + item["name"] + " " + item["brand"])
        k += 1
    choosen_food_item = menu(
        ("\nVeuillez choisir un aliment à remplacer :\n\n" + "\n".join(f_i) + "\n\n"),
        f_i,
    )
    try:
        healthier = p5oc.healthier(
            food_items[int(choosen_food_item)]["name"],
            food_categories[int(choosen_category)],
        )
    except:
        print(
            "Vous êtes vertueux ! Il n'existe pas d'aliment plus sain pour cette categorie dans la base de donnée.\n\n"
        )
        return
    id_replacement_food = []
    replacement_food = []
    k = 0
    for key, value in healthier.items():
        replacement_food.append(
            "["
            + str(k)
            + "] : "
            + str(value[0])
            + " "
            + str(value[1])
            + ", Nutriscore: "
            + str(value[2])
            + " Nova Grade: "
            + str(value[3])
        )
        id_replacement_food.append(key)
        k += 1
    choosen_replacement_item = menu(
        (
            "\nVeuillez choisir l'aliment de remplacement (le plus sain est en premier !):\n\n"
            + "\n".join(replacement_food)
            + "\n\n"
        ),
        replacement_food,
    )
    stores = p5oc.find_store(id_replacement_food[int(choosen_replacement_item)])

    save = menu(
        (
            "\nVoici les informations de l'aliment de remplacement :"
            "\n\nNom : "
            + str(healthier[id_replacement_food[int(choosen_replacement_item)]][0])
            + "\nmarque : "
            + str(healthier[id_replacement_food[int(choosen_replacement_item)]][1])
            + "\nmagasins : "
            + ", ".join(stores)
            + "\nNutriscore , Nova Grade : "
            + str(healthier[id_replacement_food[int(choosen_replacement_item)]][2])
            + ", "
            + str(healthier[id_replacement_food[int(choosen_replacement_item)]][3])
            + "\nLien vers la page web Open Food Facts : https://fr.openfoodfacts.org/product/"
            + str(id_replacement_food[int(choosen_replacement_item)])
            + "\n\nVeuillez taper 0 pour sauver ou 1 pour retourner au menu principal\n"
        ),
        [0, 1],
    )
    if save == "0":
        try:
            p5oc.add(
                "favoris",
                ["favori_id_openfoodfacts"],
                [id_replacement_food[int(choosen_replacement_item)]],
            )
            print("\n\nCet aliment a été ajouté à vos favoris.\n")
        except:
            print("\n\nL'aliment est déjà présent dans vos favoris\n\n")
    else:
        pass


def saved_searches():
    """
    display the list of saved food items and their details if any.
    returns to the main menu if no food items are available in the favoris.
    """
    favoris = {}
    try:
        favoris = p5oc.favoris()
    except:
        print("\n\nIl n'existe pas d'aliments déjà sauvegardés dans les favoris !\n\n")
        return
    print(
        "str(healthier[id_replacement_food[int(choosen_replacement_item)]][1])oici vos aliments favoris : "
    )
    for key, value in favoris.items():
        strores = p5oc.find_store(key)
        print(
            "----------------------------------------------------------------------------------------------------------\n"
            "Nom : "
            + str(value[0])
            + "\nMarque : "
            + str(value[1])
            + "\nMagasins : "
            + ", ".join(strores)
            + "\nNutriscore , Nova Grade : "
            + str(value[2])
            + ", "
            + str(value[3])
            + "\nLien vers la page web Open Food Facts : https://fr.openfoodfacts.org/product/"
            + str(key)
            + "\n"
        )
    print(
        "----------------------------------------------------------------------------------------------------------\n"
    )
    menu("Veuillez presser 0 pour retourner au menu principal\n", [0])


def menu(texte, data):
    """
    input texte, returns the answer if it is an int within data indexes.
    """
    j = 1
    while j:
        choice = input(texte)
        try:
            data[int(choice)]
            return choice
        except:
            print("\nMerci de taper un chiffre parmis les choix proposés\n\n")


if __name__ == "__main__":
    """
    Just in case it gets to be used as a lib ;)
    """
    main()
