
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
