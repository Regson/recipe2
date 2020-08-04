import sqlite3

CREATE_TABLE_RECIPE = """CREATE TABLE IF NOT EXISTS recipe (
    name TEXT PRIMARY KEY
)"""
CREATE_TABLE_INGREDIENTS = """CREATE TABLE IF NOT EXISTS ingredients (
    name TEXT PRIMARY KEY
)"""
CREATE_TABLE_RECIPE_ING = """CREATE TABLE IF NOT EXISTS recipe_ing (
    recipe_name TEXT,
    ingredient_name TEXT,
    FOREIGN KEY (recipe_name) REFERENCES recipe(name),
    FOREIGN KEY (ingredient_name) REFERENCES ingredients(name)
)"""

ADD_RECIPE = "INSERT INTO recipe VALUES(?)"
ADD_INGREDIENT = "INSERT INTO ingredients VALUES(?)"
ADD_RECIPE_ING = "INSERT INTO recipe_ing VALUES(?, ?)"
VIEW_ALL_RECIPE = "SELECT * FROM recipe"
VIEW_ALL_INGREDIENTS = "SELECT * FROM ingredients"
VIEW_RECIPE_ING = """SELECT ingredients.*
    FROM ingredients
    JOIN recipe_ing ON recipe_ing.ingredient_name = ingredients.name
    JOIN recipe ON recipe.name = recipe_ing.recipe_name
    WHERE recipe.name = ?;"""
RECIPE_BY_NAME = "SELECT * FROM recipe WHERE recipe.name = ?;"
RECIPE_ING_BY_NAME = """SELECT recipe_name FROM recipe_ing WHERE
    recipe_ing.ingredient_name = ?;"""

connection = sqlite3.connect("recipeDB.db")


def create_tables():
    with connection:
        connection.execute(CREATE_TABLE_RECIPE)
        connection.execute(CREATE_TABLE_INGREDIENTS)
        connection.execute(CREATE_TABLE_RECIPE_ING)


def find_recipe_by_name(name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(RECIPE_BY_NAME, (name,))
        return cursor.fetchone()


def find_recipe_ing_name(*names):
    for ing_name in names:
        for name in ing_name:
            with connection:
                cursor = connection.cursor()
                cursor.execute(RECIPE_ING_BY_NAME, (name,))
                return cursor.fetchall()


# With this you can add multiple recipe at a once
def add_recipe(*names):
    for recipe in names:
        for name in recipe:
            with connection:
                connection.execute(ADD_RECIPE, (name,))


def add_ingredient(*names):
    for ingredient in names:
        for name in ingredient:
            with connection:
                connection.execute(ADD_INGREDIENT, (name,))


def add_recipe_ing(recipe_name, *ingredient_names):
    for name in ingredient_names:
        for ingredient_name in name:
            with connection:
                connection.execute(
                    ADD_RECIPE_ING, (recipe_name, ingredient_name)
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


def get_recipe_ing(recipeName):
    with connection:
        cursor = connection.cursor()
        cursor.execute(VIEW_RECIPE_ING, (recipeName,))
        return cursor.fetchall()
