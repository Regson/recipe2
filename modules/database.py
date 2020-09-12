import sqlite3
import functools
import sys

CREATE_TABLE_RECIPE = """CREATE TABLE IF NOT EXISTS recipe (
    name TEXT NOT NULL,
    PRIMARY KEY(name)
)"""
CREATE_TABLE_INGREDIENTS = """CREATE TABLE IF NOT EXISTS ingredients (
    name TEXT NOT NULL,
    PRIMARY KEY(name)
)"""
CREATE_TABLE_RECIPE_ING = """CREATE TABLE IF NOT EXISTS recipe_ing (
    recipe_name TEXT,
    ingredient_name TEXT,
    FOREIGN KEY (recipe_name) REFERENCES recipe(name) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_name) REFERENCES ingredients(name) ON DELETE CASCADE
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

INGREDIENT_BY_NAME = "SELECT * FROM ingredients WHERE ingredients.name = ?;"

RECIPE_ING_BY_NAME = """SELECT recipe_name FROM recipe_ing WHERE
    recipe_ing.ingredient_name = ?;"""

DELETE_RECIPE = "DELETE FROM recipe WHERE name = ?;"
DELETE_INGREDIENT = "DELETE FROM ingredients WHERE name = ?;"
DELETE_ALL_RECIPE = "DELETE FROM recipe"
DELETE_ALL_INGREDIENT = "DELETE FROM ingredients"

connection = sqlite3.connect("recipeDB.db")


# Error exception handling
def deco_err_handling(func):

    @functools.wraps(func)
    def err_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Seems the return statement works better here.
        except sqlite3.IntegrityError as err:
            print(f"An IntegrityError occurred.\n {err}")
        except sqlite3.OperationalError as err:
            sys.exit(f"OperationalError Occurred!\n {err}")
        except sqlite3.NotSupportedError as err:
            sys.exit(f"Error: {err}")
        except sqlite3.Error as err:
            print(f"Error: {err}")
        except sqlite3.InternalError as err:
            print(f"Error: {err}")

        """ Without return func(*args, **kwargs), you get a 
        TypeError: 'NoneType' object is not iterable for functions 
        involving iterations"""

        # return func(*args, **kwargs)
    return err_handler


@deco_err_handling
def create_tables():
    with connection:
        connection.execute(CREATE_TABLE_RECIPE)
        connection.execute(CREATE_TABLE_INGREDIENTS)
        connection.execute(CREATE_TABLE_RECIPE_ING)
        connection.execute("PRAGMA foreign_keys = ON;")


@deco_err_handling
def find_recipe_by_name(name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(RECIPE_BY_NAME, (name,))
        return cursor.fetchone()


@deco_err_handling
def find_ingredient_by_name(name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(INGREDIENT_BY_NAME, (name,))
        return cursor.fetchone()


@deco_err_handling
def find_recipe_ing_name(name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(RECIPE_ING_BY_NAME, (name,))
        return cursor.fetchall()


# With this you can add multiple recipe at once
@deco_err_handling
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
    if (not existed) and new_recipe:
        print(f"\n{new_recipe} added to kitchen successfully!\n")
    elif existed and (not new_recipe):
        print(f"\n{existed} already exist!\n")
    else:
        print(f"\n{new_recipe} added to kitchen successfully!\n")
        print(f"\n{existed} already exist!\n")


@deco_err_handling
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


@deco_err_handling
def add_recipe_ing(recipe_name, ingredient_names):
    with connection:
        connection.execute(
            ADD_RECIPE_ING, (recipe_name, ingredient_names)
            )


@deco_err_handling
def get_all_recipe():
    with connection:
        cursor = connection.cursor()
        cursor.execute(VIEW_ALL_RECIPE)
        return cursor.fetchall()


@deco_err_handling
def get_all_ingredients():
    with connection:
        cursor = connection.cursor()
        cursor.execute(VIEW_ALL_INGREDIENTS)
        return cursor.fetchall()


@deco_err_handling
def get_recipe_ing(recipe_name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(VIEW_RECIPE_ING, (recipe_name,))
        return cursor.fetchall()


@deco_err_handling
def del_recipe(name):
    with connection:
        connection.execute(DELETE_RECIPE, (name,))


@deco_err_handling
def del_ingredient(name):
    with connection:
        connection.execute(DELETE_INGREDIENT, (name,))


@deco_err_handling
def del_all_recipe():
    with connection:
        connection.execute(DELETE_ALL_RECIPE)


@deco_err_handling
def del_all_ingredient():
    with connection:
        connection.execute(DELETE_ALL_INGREDIENT)
