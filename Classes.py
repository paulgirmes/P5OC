"""
"Database" class definition for interaction with Mysql server with mysql connector lib.
"""
# -*- coding: utf8 -*-

import mysql.connector
from mysql.connector import errorcode


class Database:
    """allows CRU in a database, please give user, pwd, database_name and host IP when creating
    """

    def __init__(self, database_name, user_name, pwd, host):
        self.database = database_name
        self.user_name = user_name
        self.pwd = pwd
        self.host = host

    def add(self, table, col_names, col_values):
        """ insert new line in table from list of column names (list of strings fields)
            and list of column_values(list of strings fields)  
        """
        cnx = self.__connexion__()
        cursor = cnx.cursor()

        # arg's format for cursor.execute
        ph = []
        [ph.append("%s") for item in col_values]
        add_item = (
            "INSERT INTO "
            + table
            + " ("
            + ", ".join(col_names)
            + ") VALUES ("
            + ", ".join(ph)
            + ")"
        )
        item_data = col_values

        try:
            cursor.execute(add_item, item_data)
        except:
            raise Exception
        cnx.commit()
        cursor.close()
        cnx.close()

    def get_all(self, table):
        """takes a table name as string, returns a list of all food categories available in DB
        """
        cnx = self.__connexion__()
        cursor = cnx.cursor()
        query = "SELECT * FROM " + table

        cursor.execute(query)
        result = []
        [result.append(n) for (n,) in cursor]
        cursor.close()
        cnx.close()
        return result

    def get_food_items(self, category):
        """
            takes a category as a string returns a list of food items that matches the given category
        """
        cnx = self.__connexion__()
        cursor = cnx.cursor()
        query = (
            "select food_name, food_brand from food_item "
            "join food_item_category "
            "on id_openfoodfacts = food_item_id_openfoodfacts "
            "join category "
            "on category_name = name where category.name = (%s)"
        )
        cursor.execute(query, [category])
        result = []
        for (name, brand) in cursor:
            result.append({"name": name, "brand": brand})
        cursor.close()
        cnx.close()
        return result

    def healthier(self, food_item, food_category):
        """
            takes a food item as a str and the category of the given food item as a str, returns an healthier food item
            (tries to find food items with both better nutriscore and nova grade, if it fails tries to find food items 
            with better Nutriscore or Nova grade).
            Raises an Exception if no available healthier food item in DB
        """
        cnx = self.__connexion__()
        cursor = cnx.cursor()
        query = (
            "select nutriscore, nova_grade from food_item " "where food_name like (%s)"
        )
        cursor.execute(query, [food_item])
        grades = []
        for (score, grade) in cursor:
            grades.append(score)
            grades.append(grade)

        query1 = (
            "select id_openfoodfacts, food_name, food_brand, nutriscore, nova_grade from food_item "
            "join food_item_category "
            "on id_openfoodfacts = food_item_id_openfoodfacts "
            "join category "
            "on category_name = name"
            " where food_item_category.category_name = (%s) "
            "and (nova_grade < (%s) and nutriscore < (%s))"
            "order by nutriscore + nova_grade asc"
        )

        cursor.execute(query1, (food_category, grades[1], grades[0]))
        food_replacement = {}
        for (id_off, name, brand, nutri, nova) in cursor:
            food_replacement[id_off] = [name, brand, nutri, nova]

        if len(food_replacement) != 0:
            cursor.close()
            cnx.close()
            return food_replacement
        else:
            query2 = (
                "select id_openfoodfacts, food_name, food_brand, nutriscore, nova_grade from food_item "
                "join food_item_category "
                "on id_openfoodfacts = food_item_id_openfoodfacts "
                "join category "
                "on category_name = name"
                " where food_item_category.category_name = (%s) "
                "and (nova_grade < (%s) or nutriscore < (%s))"
                "order by nutriscore + nova_grade asc"
            )
            cursor.execute(query2, (food_category, grades[1], grades[0]))
            for (id_off, name, brand, nutri, nova) in cursor:
                food_replacement[id_off] = [name, brand, nutri, nova]
            cursor.close()
            cnx.close()
            if len(food_replacement) != 0:
                return food_replacement
            else:
                raise Exception
        cursor.close()
        cnx.close()

    def find_store(self, id_food_item):
        """
        takes a food id return stores where the food item may be bought if any available in DB,
        returns "non disponible" if not.
        """
        cnx = self.__connexion__()
        cursor = cnx.cursor()
        query = (
            "select name from store "
            "join food_item_store "
            "on name = store_name "
            "join food_item "
            "on food_item_id_openfoodfacts = id_openfoodfacts"
            " where id_openfoodfacts = (%s) "
        )

        cursor.execute(query, [id_food_item])
        stores = []
        for (store,) in cursor:
            stores.append(store)
        cursor.close()
        cnx.close()
        if len(stores) != 0:
            return stores
        else:
            return ["non disponible"]

    def favoris(self):
        """
        returns saved items (all from "favoris" DB table), 
        if none raises an Exception.
        """
        cnx = self.__connexion__()
        cursor = cnx.cursor()
        query = (
            "select id_openfoodfacts, food_name, food_brand, nutriscore, nova_grade from food_item "
            "join favoris "
            "on id_openfoodfacts = favori_id_openfoodfacts "
        )

        cursor.execute(query)
        favoris = {}
        for (id_off, name, brand, nutri, nova) in cursor:
            favoris[id_off] = [name, brand, nutri, nova]
        cursor.close()
        cnx.close()
        if len(favoris) != 0:
            return favoris
        else:
            raise Exception

    def __connexion__(self):
        """
        establishes a connection with DB and handles err.
        /!\\ do not forget to close both cnx and cursor in the method /!\\.
        """
        try:
            cnx = mysql.connector.connect(
                user=self.user_name,
                password=self.pwd,
                host=self.host,
                database=self.database,
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        return cnx
