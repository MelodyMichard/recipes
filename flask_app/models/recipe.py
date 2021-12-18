from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.created_at = data['created_at']
        self.description = data['description']
        self.id = data['id']
        self.instructions = data['instructions']
        self.is_under_thirty = data['is_under_thirty']
        self.name = data['name']
        self.prepared_at = data['prepared_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, is_under_thirty, prepared_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(is_under_thirty)s, %(prepared_at)s, %(user_id)s);"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        print(data)
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, is_under_thirty=%(is_under_thirty)s, prepared_at=%(prepared_at)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get(cls, data):
        query = "SELECT * FROM recipes WHERE user_id = %(id)s;"
        rs = connectToMySQL('recipes').query_db(query, data)
        all_recipes = []
        for r in rs:
            all_recipes.append(cls(r))
        return all_recipes

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results =  connectToMySQL('recipes').query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append( cls(row) )
        return all_recipes

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        isValid = True
        if len(recipe['name']) < 3:
            isValid = False
            flash("Name must be at least 3 characters", "recipe")
        if len(recipe['instructions']) < 3:
            isValid = False
            flash("Instructions must be at least 3 characters", "recipe")
        if len(recipe['description']) < 3:
            isValid = False 
            flash("Description must be at least 3 characters", "recipe")
        if recipe['prepared_at'] == "":
            isValid = False
            flash("Please enter a date", "recipe")
        return isValid