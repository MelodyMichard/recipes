from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def getById(cls, data):
        query  = "SELECT * FROM users WHERE id = %(id)s"
        return cls((connectToMySQL('recipes').query_db(query, data))[0])

    @classmethod
    def getByEmail(cls, data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        resultSet = (connectToMySQL('recipes').query_db(query, data))
        if len(resultSet) > 0:
            return cls(resultSet[0])
        return False

    @staticmethod
    def validate_register(user):
        isValid = True
        minFname = 3
        minLname = 3
        minPassword = 3

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            isValid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            isValid=False
        if len(user['first_name']) < minFname:
            flash("First name must be at least %i characters" % minFname,"register" )
            isValid = False
        if len(user['last_name']) < minLname:
            flash("Last name must be at least %i characters" % minLname,"register" )
            isValid = False
        if len(user['password']) < minPassword:
            flash("Password must be at least %i characters" % minPassword,"register" )
            isValid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
            isValid = False
        return isValid