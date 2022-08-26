from flask_app.config.mysqlconnection import MySQLConnection
import re
from flask_app.models.user import User
class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.time_to_make = data['time_to_make'] # time to make in minutes (int) 1:less than 30, 0:more than 30
        self.user_id = data['user_id'] # user_id (int)
        self.user = User.get_by_id(data['user_id']) # user_id (int)

    @classmethod
    def create(cls,data):
        mysql = MySQLConnection('recipes')
        query = "INSERT INTO recipes (name, description, instructions, time_to_make, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(time_to_make)s, %(user_id)s)"
        return mysql.query_db(query, data)

    @classmethod
    def get_all(cls):
        mysql = MySQLConnection('recipes')
        query = "SELECT * FROM recipes"
        result = mysql.query_db(query)
        return [cls(i) for i in result]

    @classmethod
    def get_by_id(cls,id):
        mysql = MySQLConnection('recipes')
        data = {'id':id}
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        result = mysql.query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        mysql = MySQLConnection('recipes')
        query = "UPDATE recipes SET name = %(name)s, description= %(description)s, instructions = %(instructions)s, time_to_make = %(time_to_make)s, user_id = %(user_id)s WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @classmethod
    def delete(cls,data):
        data = {'id':data}
        mysql = MySQLConnection('recipes')
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @staticmethod
    def validate(data):
        errors = []
        valid = True
        if len(data['ingredient[]']) < 1:
            errors.append('Ingredients cannot be blank')
        if len(data['quantity[]']) < 1:
            errors.append('Quantity cannot be blank')
        if len(data['name']) < 1:
            errors.append('Name cannot be blank')
        if len(data['instructions']) < 1:
            errors.append('Instructions cannot be blank')
        if errors:
            valid = False
        return (valid, errors)