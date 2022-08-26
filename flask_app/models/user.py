from flask_app.config.mysqlconnection import MySQLConnection
import re 

password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')# we can use this regex to validate email, but we will use a custom validation method for email
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def login(cls, data):
        mysql = MySQLConnection('recipes')
        query = "SELECT * FROM users WHERE email = %(email)s AND password = %(password)s"
        result = mysql.query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False

    @classmethod
    def register(cls,data):
        mysql = MySQLConnection('recipes')
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return mysql.query_db(query, data)

    @staticmethod
    def validate_registration(data):
        valid = True
        list = []
        if len(data['first_name']) < 3:
            list.append('First name must be at least 3 characters')
        if len(data['last_name']) < 3:
            list.append('Last name must be at least 3 characters')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            list.append('Email must be valid')
        if not password_regex.match(data['password']):
            list.append('Password must be at least 8 characters, contain 1 uppercase, 1 lowercase, and 1 number')
        if data['password'] != data['confirm_password']:
            list.append('Passwords do not match')

        query = "SELECT * FROM users WHERE email = %(email)s"# we will use this query to check if the email is already in use
        mysql = MySQLConnection('recipes')
        #data['email'] = data['email'].lower()
        result = mysql.query_db(query, data)
        if result:
            list.append('Email already in use')
        if list:
            valid = False
        return (list , valid)

    @classmethod
    def get_by_email(cls, data):
        mysql = MySQLConnection('recipes')
        #data['email'] = data['email'].lower()
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = mysql.query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False

    @classmethod
    def get_by_id(cls, id):
        mysql = MySQLConnection('recipes')
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {'id': id}
        result = mysql.query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all_except(cls, id):
        mysql = MySQLConnection('recipes')
        query = "SELECT * FROM users ORDER BY first_name ASC"
        result = mysql.query_db(query)
        return [cls(row) for row in result if row['id'] != id]