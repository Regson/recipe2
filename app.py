import itertools
from sqlite3 import Error

from modules import database as db
from modules.menu import *

try:
    db.create_tables()
except Error as e:
    print(e)


def instruction(item):
    print(
        f"You can enter multiple {item} "
        "just separate them with a , e.g item1,item2,item3"
    )


def check_for_blanks(blank_input):
    """

    :rtype: Checks for a blank inputs and
    prints to console if input is blank.
    """
    return not (blank_input and blank_input.strip())


def add_recipe_ing(recipe_name):
    ingredients_names = input("Ingredient name: ").strip()
    if ingredients_names == "":
        print("\nInputs CANNOT be Empty!\n")
    else:
        ingredients = db.find_ingredient_by_name(ingredients_names)
        if ingredients:
            recipes_name = db.find_recipe_ing_name(ingredients_names)
            if recipe_name in itertools.chain(*recipes_name):
                print(f"\n<-- {recipe_name} already has {ingredients_names} -->")
            else:
                db.add_recipe_ing(recipe_name, ingredients_names)
                print("\n<-- Data saved successfully -->")
        else:
            print(f"{ingredients_names} not found! type n on the next prompt "
                  f"to go to OPTIONS and add {ingredients_names} to database.")


def print_all(header, names):
    print(f"<-- {header} -->")
    for _id, (item,) in enumerate(names, start=1):
        print(f"{_id}. {item}")


def print_all_recipe_ing():
    name = input("Recipe name: ").strip()
    recipe = db.find_recipe_by_name(name)
    if recipe:
        ingredients = db.get_recipe_ing(name)
        if ingredients:
            print_all(name, ingredients)
        else:
            print("No ingredients")
        print("------------\n")
    else:
        print(f"{name} not found! please go to OPTIONS and add {name} to Kitchen.")


print(welcome)


def main_menu():
    while (user_input := input(menu)) != "8":
        if user_input == "1":
            instruction("recipes")
            recipes_names = input("Enter recipe name: ").strip()
            if recipes_names == "":
                print("Input no go fit de blank!\n")
            else:
                new_name = recipes_names.split(",")
                new_name = list(filter(None, new_name))
                try:
                    db.add_recipe(new_name)
                except Error as err:
                    print(err)
        elif user_input == "2":
            instruction("ingredients")
            ingredients_name = input("Enter ingredient name: ").strip()
            if ingredients_name == "":
                print("\nInputs CANNOT be Empty!\n")
            else:
                new_name = ingredients_name.split(",")
                new_name = list(filter(None, new_name))
                try:
                    db.add_ingredient(new_name)
                except Error as err:
                    print(err)
        elif user_input == "3":
            try:
                recipes = db.get_all_recipe()
            except Error as err:
                print(err)
            else:
                if recipes:
                    print_all("All Recipes", recipes)
                else:
                    print("No recipe found!")
                print("------------\n")
        elif user_input == "4":
            try:
                ingredient = db.get_all_ingredients()
            except Error as err:
                print(err)
            else:
                if ingredient:
                    print_all("All Ingredients", ingredient)
                else:
                    print("No ingredient found!")
                print("------------\n")
        elif user_input == "5":
            recipe_name = input("Recipe name: ")
            add_ingredient = f""" Would you like to add another ingredient to {recipe_name}? Y/N 
            type y if Yes or n if No and press ENTER: """
            if recipe_name == "":
                print("\nInputs CANNOT be Empty!\n")
            elif not db.find_recipe_by_name(recipe_name):
                print(f"{recipe_name} does not exist!")
            else:
                add_recipe_ing(recipe_name)
                while (ingredient_input := input(add_ingredient).upper()) != "N":
                    if ingredient_input == "Y":
                        add_recipe_ing(recipe_name)
        elif user_input == "6":
            print_all_recipe_ing()
        elif user_input == "7":
            del_menu()


def del_menu():
    while (delete_input := input(delete_menu)) != "5":
        if delete_input == "1":
            recipe_name = input("Enter name of recipe to delete: ").strip()
            if recipe_name == "":
                print("\nInput CANNOT be Empty!\n")
            elif not db.find_recipe_by_name(recipe_name):
                print(f"\n{recipe_name} does not exist!\n")
            else:
                try:
                    db.del_recipe(recipe_name)
                except Error as err:
                    print(err)
                print("\nDeleted!\n")

        elif delete_input == "2":
            ingredient_name = input("Enter ingredient to delete: ").strip()
            if ingredient_name == "":
                print("\nInput CANNOT be Empty!\n")
            elif not db.find_ingredient_by_name(ingredient_name):
                print(f"\n{ingredient_name} does not exist!\n")
            else:
                try:
                    db.del_ingredient(ingredient_name)
                except Error as err:
                    print(err)
                print("\nDeleted!\n")
        elif delete_input == "3":
            try:
                db.del_all_recipe()
            except Error as err:
                print(err)
            else:
                print("All recipes deleted successfully!")
        elif delete_input == "4":
            try:
                db.del_all_ingredient()
            except Error as err:
                print(err)
            else:
                print("All recipes deleted successfully!")


main_menu()
