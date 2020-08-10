import database as db
import itertools

menu = """Please Select One of the following Options:
1. Add Recipes
2. Add Ingredients
3. View all Recipes
4. View all Ingredients
5. Add Ingredient(s) to Recipe
6. View a Recipe & its Ingredients
7. Exit

your selection: """

welcome = """
    ---------------------------------
    |   WELCOME TO MY RECIPE APP    |
    ---------------------------------
"""
print(welcome)
db.create_tables()


def instruction(item):
    print(
        f"You can enter multiple {item} "
        "just separate them with a , e.g item1,item2,item3"
        )


def check_for_blanks(blank_input):
    """

    :rtype: Checks for an blank inputs and
    prints to console if input is blank.
    """
    return not (blank_input and blank_input.strip())


def add_recipe_ing():
    ingredients_names = input("Ingredient name: ").strip()
    if not check_for_blanks(ingredients_names):
        ingredients = db.find_ingredient_by_name(ingredients_names)
        if ingredients:
            recipes_name = db.find_recipe_ing_name(ingredients_names)
            if recipe_name in itertools.chain(*recipes_name):
                print(f"\n<-- {recipe_name} already has {ingredients_names} -->\n")
            else:
                db.add_recipe_ing(recipe_name, ingredients_names)
                print("\n<-- Data saved successfully -->\n")
        else:
            print(f"{ingredients_names} not found! type n on the next prompt "
                  f"to go to OPTIONS and add {ingredients_names} to database.")
    else:
        print("Inputs CANNOT be Empty!")


def print_all(header, names):
    print(f"<-- {header} -->")
    for _id, (item,) in enumerate(names, start=1):
        print(f"{_id}. {item}")


def print_all_recipe_ing():
    name = input("Recipe name: ")
    recipe = db.find_recipe_by_name(name)
    if recipe:
        ingredients = db.get_recipe_ing(name)
        if ingredients:
            print_all(name, ingredients)
        else:
            print("No ingredients")
        print("------------\n")
    else:
        print(f"{name} not found! please go to OPTIONS and add {name} to database.")


while (user_input := input(menu)) != "7":
    if user_input == "1":
        instruction("recipes")
        recipes_names = input("Enter recipe name: ").strip().split(",")
        db.add_recipe(recipes_names)
    elif user_input == "2":
        instruction("ingredients")
        ingredients_name = input("Enter ingredient name: ").strip().split(",")
        db.add_ingredient(ingredients_name)
    elif user_input == "3":
        recipes = db.get_all_recipe()
        if recipes:
            print_all("All Recipes", recipes)
        else:
            print("No recipe found!")
        print("------------\n")
    elif user_input == "4":
        ingredient = db.get_all_ingredients()
        if ingredient:
            print_all("All Ingredients", ingredient)
        else:
            print("No ingredient found!")
        print("------------\n")
    elif user_input == "5":
        recipe_name = input("Recipe name: ")
        add_ingredient = f""" 
            Would you like to add another ingredient to {recipe_name}? Y/N
            type y if Yes or n if No and press ENTER: """
        if not check_for_blanks(recipe_name):
            add_recipe_ing()
            while (ingredient_input := input(add_ingredient).upper()) != "N":
                if ingredient_input == "Y":
                    add_recipe_ing()
        else:
            print("Inputs CANNOT be Empty!\n")
    elif user_input == "6":
        print_all_recipe_ing()
