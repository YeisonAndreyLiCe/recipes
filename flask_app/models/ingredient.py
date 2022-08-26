from flask_app.config.mysqlconnection import MySQLConnection

class Ingredient:
    def __init__(self,data):
        self.id = data['id']
        self.ingredient = data['ingredient']
        self.quantity = data['quantity'] # quantity (list)

    @classmethod
    def create(cls,data):
        mysql = MySQLConnection('recipes')
        query = "INSERT INTO ingredients (ingredient, quantity) VALUES (%(ingredient)s, %(quantity)s)"
        return mysql.query_db(query, data)

    @classmethod
    def get_all(cls):
        mysql = MySQLConnection('recipes')
        query = "SELECT * FROM ingredients"
        return mysql.query_db(query)

    @classmethod
    def get_by_id(cls,data):
        mysql = MySQLConnection('recipes')
        query = "SELECT * FROM ingredients WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @classmethod
    def update(cls,data):
        mysql = MySQLConnection('recipes')
        query = "UPDATE ingredients SET ingredient = %(ingredient)s WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @classmethod
    def delete(cls,data):
        mysql = MySQLConnection('recipes')
        query = "DELETE FROM ingredients WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @classmethod
    def get_by_ingredient(cls,data):
        mysql = MySQLConnection('recipes')
        query = "SELECT * FROM ingredients WHERE ingredient = %(ingredient)s"
        return mysql.query_db(query, data)

    @classmethod
    def get_quantity(cls,data):
        mysql = MySQLConnection('recipes')
        query = "SELECT quantity FROM ingredients WHERE id = %(id)s"
        return mysql.query_db(query, data)