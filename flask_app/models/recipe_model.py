from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import time
from flask_app.models.user_model import User


class Recipe:
    db = "recipe_share_erd"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.quick = data['quick']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # set user to none so you can attach a User instance and user attributes in the classmethod
        self.user = None

    @classmethod
    def save(cls, data):
        query = """INSERT INTO recipes (name, description, instructions, date_made, quick, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(quick)s, %(user_id)s )
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_recipes = []
        
        for recipe in results:
            meal = cls(recipe)
            # make temporary user dictionary
            recipe_author = {
                'id' : recipe['users.id'],
                'first_name' : recipe['first_name'],
                'last_name' : recipe['last_name'],
                'email' : recipe['email'],
                'password' : recipe['password'],
                'created_at' : recipe['users.created_at'],
                'updated_at' : recipe['users.updated_at'],
            }
            # add user to meal
            meal.user = User(recipe_author)
            all_recipes.append(meal)
        return all_recipes

    @classmethod
    def get_recipe(cls, data):
        query = """SELECT * FROM recipes
                WHERE id = %(id)s """
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update_recipe(cls,data):
        query = """UPDATE recipes SET
                name = %(name)s, description = %(description)s, instructions = %(instructions)s, 
                date_made = %(date_made)s, quick = %(quick)s"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def delete(cls, id):
        query = """DELETE FROM recipes 
                WHERE id = %(id)s"""
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        return results

    # RECIPE VALIDATIONS
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be more than 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3 or len(recipe['instructions']) < 3:
            flash("Field must be at least 3 characters", "recipe")
            is_valid = False
        if recipe['date_made'] == "":
            flash("Please select a date", "recipe")
            is_valid = False
        if recipe['quick'] == "":
            flash("Field cannot be blank", "recipe")
            is_valid = False
        return is_valid