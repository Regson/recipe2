import sqlite3
from modules.queries import *


connection = sqlite3.connect("recipeDB.db")


def create_tables():
    with connection:
        connection.execute(CREATE_TABLE_RECIPE)
        connection.execute(CREATE_TABLE_INGREDIENTS)
        connection.execute(CREATE_TABLE_RECIPE_ING)
        connection.execute("PRAGMA foreign_keys = ON;")


def find_recipe_by_name(name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(RECIPE_BY_NAME, (name,))
        return cursor.fetchone()


def find_ingredient_by_name(name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(INGREDIENT_BY_NAME, (name,))
        return cursor.fetchone()


def find_recipe_ing_name(name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(RECIPE_ING_BY_NAME, (name,))
        return cursor.fetchall()


# With this you can add multiple recipe at once
def add_recipe(names):
    existed = []
    new_recipe = []
    for recipe in names:
        if find_recipe_by_name(recipe):
            existed.append(recipe)
        else:
            with connection:
                connection.execute(ADD_RECIPE, (recipe,))
                new_recipe.append(recipe)
    if not existed:
        print(f"\n{new_recipe} added to kitchen successfully!\n")
    elif not new_recipe:
        print(f"\n{existed} already exist!\n")
    else:
        print(f"\n{new_recipe} added to kitchen successfully!\n")
        print(f"\n{existed} already exist!\n")


def add_ingredient(names):
    existed = []
    new_ingredient = []
    for ingredient in names:
        if find_ingredient_by_name(ingredient):
            existed.append(ingredient)
        else:
            with connection:
                connection.execute(ADD_INGREDIENT, (ingredient,))
                new_ingredient.append(ingredient)
    if not existed:
        print(f"\n{new_ingredient} added to kitchen successfully!\n")
    elif not new_ingredient:
        print(f"\n{existed} already exist!\n")
    else:
        print(f"\n{new_ingredient} added to kitchen successfully!\n")
        print(f"\n{existed} already exist!\n")


def add_recipe_ing(recipe_name, ingredient_names):
    with connection:
        connection.execute(
            ADD_RECIPE_ING, (recipe_name, ingredient_names)
            )


def get_all_recipe():
    with connection:
        cursor = connection.cursor()
        cursor.execute(VIEW_ALL_RECIPE)
        return cursor.fetchall()


def get_all_ingredients():
    with connection:
        cursor = connection.cursor()
        cursor.execute(VIEW_ALL_INGREDIENTS)
        return cursor.fetchall()


def get_recipe_ing(recipe_name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(VIEW_RECIPE_ING, (recipe_name,))
        return cursor.fetchall()


def del_recipe(name):
    with connection:
        connection.execute(DELETE_RECIPE, (name,))


def del_ingredient(name):
    with connection:
        connection.execute(DELETE_INGREDIENT, (name,))


def del_all_recipe():
    with connection:
        connection.execute(DELETE_ALL_RECIPE)


def del_all_ingredient():
    with connection:
        connection.execute(DELETE_ALL_INGREDIENT)
