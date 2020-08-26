import itertools
import sqlite3
import sys

from modules import database as db


# Error exception handling
def db_error_handling(arg):
    try:
        arg
    except sqlite3.IntegrityError as err:
        print(f"Error: {err}")
    except sqlite3.OperationalError as err:
        sys.exit(f"Error: {err}")
    except sqlite3.NotSupportedError as err:
        sys.exit(f"Error: {err}")
    except sqlite3.Error as err:
        print(f"Error: {err}")
    except sqlite3.InternalError as err:
        print(f"Error: {err}")
    return arg


db_error_handling(db.create_tables())  # Creates tables for the database


# this function is used as a hint for Adding of recipe and ingredients
def instruction(item):
    print(
        f"You can enter multiple {item} "
        "just separate them with a , e.g item1,item2,item3"
    )


# prints all Recipes or Ingredients depending on where it is called
def print_all_items(header, names):
    print(f"<-- {header} -->")
    for _id, (item,) in enumerate(names, start=1):
        print(f"{_id}. {item}")


# prints all ingredients for the selected recipe
def print_all_recipe_ing(user_input):
    if user_input:
        name = input("Recipe name: ").strip()
        recipe = db_error_handling(db.find_recipe_by_name(name))
        if recipe:
            ingredients = db_error_handling(db.get_recipe_ing(name))
            if ingredients:
                print_all_items(name, ingredients)
            else:
                print("No ingredients")
            print("------------\n")
        else:
            print(
                f"{name} not found! please go to OPTIONS and add {name}"
                " to Kitchen."
            )


def add_item(user_input):
    """
        DISC: This function handles both adding of recipes and ingredients.
    """
    if user_input:
        if user_input == "1":
            item_title = "Recipe"
            query = db.add_recipe
        else:
            item_title = "Ingredient"
            query = db.add_ingredient
        instruction(item_title)
        item_name = input(f"Enter {item_title} name: ").strip()
        if item_name == "":
            print("Input CANNOT be blank!\n")
        else:
            new_name = item_name.split(",")
            new_name = list(filter(None, new_name))
            db_error_handling(query(new_name))


def show_item(user_input):
    """
        This function calls the "print_all_items"
        function to display all recipes or all ingredients,
        depending on what should be displayed.
    """
    if user_input:
        if user_input == "3":
            item_title = "All Recipes"
            item_names = db_error_handling(db.get_all_recipe())
        else:
            item_title = "All Ingredients"
            item_names = db_error_handling(db.get_all_ingredients())
        print_all_items(item_title, item_names)
    else:
        print(f"No {item_title} found!")
    print("------------\n")


# logic that checks availability of recipe or ingredient before adding ingredients to the selected recipe.
def add_ingredient_to_recipe(user_input):
    if user_input:
        recipe_name = input("Recipe name: ").strip()
        prompt_add_ingredient = f""" Would you like to add another
        ingredient to {recipe_name}? Y/N
        type y if Yes or n if No and press ENTER: """
        if recipe_name == "":
            print("\nInputs CANNOT be Empty!\n")
        elif not db.find_recipe_by_name(recipe_name):
            print(f"{recipe_name} does not exist!")
        else:
            add_recipe_ing(recipe_name)
            while (
                    ingredient_input := input(prompt_add_ingredient).upper()
            ) != "N":
                if ingredient_input == "Y":
                    add_recipe_ing(recipe_name)


def add_recipe_ing(recipe_name):
    ingredients_names = input("Ingredient name: ").strip()
    if ingredients_names == "":
        print("\nInputs CANNOT be Empty!\n")
    else:
        ingredients = db_error_handling(db.find_ingredient_by_name(ingredients_names))
        if ingredients:
            recipes_name = db_error_handling(db.find_recipe_ing_name(ingredients_names))
            if recipe_name in itertools.chain(*recipes_name):
                print(f"\n<-- {recipe_name} already has {ingredients_names} -->")
            else:
                db_error_handling(db.add_recipe_ing(recipe_name, ingredients_names))
                print("\n<-- Data saved successfully -->")
        else:
            print(f"{ingredients_names} not found! type n on the next prompt "
                  f"to go to OPTIONS and add {ingredients_names} to database.")


# calls the delete function
def del_item(user_input):
    if user_input:
        if user_input == "1":
            item_title = "Recipe"
            del_query = db.del_recipe
            get_query = db.find_recipe_by_name
        else:
            item_title = "Ingredient"
            del_query = db.del_ingredient
            get_query = db.find_ingredient_by_name
        item_name = input(f"Enter name of {item_title} to delete: ").strip()
        if item_name == "":
            print("\nInput CANNOT be Empty!\n")
        elif not get_query(item_name):
            print(f"\n{item_name} does not exist!\n")
        else:
            db_error_handling(del_query(item_name))
            print("\nDeleted!\n")


def del_all_item(user_input):
    if user_input:
        if user_input == "3":
            item_title = "recipes"
            query = db.del_all_recipe
        else:
            item_title = "ingredient"
            query = db.del_all_ingredient

        db_error_handling(query())
        print(f"All {item_title} deleted successfully!")
