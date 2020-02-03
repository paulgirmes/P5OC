import mysql.connector
from mysql.connector import errorcode


class Database:
    """"allows CRUD in a database, please give user, pwd, database_name and host IP when creating
    """
    def __init__(self, database_name, user_name, pwd, host):
        self.database = database_name
        self.user_name = user_name
        self.pwd = pwd
        self.host = host
        self.pk = str()

    def add(self, table, col_names , col_values):
        """insert new line in table from list of column names and list of column_values, 
        returns last row PK   
        """
        try:
            cnx = mysql.connector.connect(user=self.user_name  , password=self.pwd,
                                    host=self.host,
                                    database=self.database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        cursor = cnx.cursor()
        ph = []
        [ph.append("%s") for item in col_values]
        add_item = ("INSERT INTO "+table+" ("+", ".join(col_names)+") VALUES ("+", ".join(ph)+")")
        item_data = col_values

        try:
            cursor.execute(add_item, item_data)
        except:
            pass
        self.pk = cursor.lastrowid
        cnx.commit()
        cursor.close()
        cnx.close()
    
