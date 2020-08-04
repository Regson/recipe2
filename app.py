import database as db

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
        "just separate them with space. e.g item1 item2 item3"
        )


def add_recipe():
    instruction("recipes")
    recipe_name = input("Enter recipe name: ").split(" ")
    db.add_recipe(recipe_name)


def add_ingredients():
    instruction("ingredients")
    ingredient_name = input("Enter ingredient name: ").split(" ")
    db.add_ingredient(ingredient_name)


def add_recipe_ing():
    instruction("ingredients for a recipe")
    recipe_name = input("Recipe name: ")
    ingredient_name = input("Ingredient name: ").split(" ")
    recipeName = db.find_recipe_ing_name(ingredient_name)
    if recipe_name in str(recipeName):
        print(str(recipeName))
        print(f"\n<-- {recipe_name} already has {ingredient_name} -->\n")
    else:
        db.add_recipe_ing(recipe_name, ingredient_name)
        print("\n<-- Data saved successfully -->\n")


def print_all_recipe(header, recipes):
    print(f"<-- {header} Recipes -->")
    _id = 1
    for recipe, in recipes:
        print(f"{_id}. {recipe}")
        _id += 1


def print_all_ingredients(header, ingredients):
    print(f"<-- {header} Ingredients -->")
    _id = 1
    for ingr, in ingredients:
        print(f"{_id}. {ingr}")
        _id += 1


def print_all_recipe_ing():
    name = input("Recipe name: ")
    ingredients = db.get_recipe_ing(name)
    if ingredients:
        print_all_ingredients(name, ingredients)
    else:
        print("No ingredients")
    print("------------\n")


while (user_input := input(menu)) != "7":
    if user_input == "1":
        try:
            add_recipe()
        except Exception as e:
            print(e, "::Error: recipe already exist.::")
    elif user_input == "2":
        try:
            add_ingredients()
        except Exception as e:
            print(e, "::Error: ingredient already exist.::")
    elif user_input == "3":
        recipes = db.get_all_recipe()
        if recipes:
            print_all_recipe("All", recipes)
        else:
            print("No recipe found!")
        print("------------\n")
    elif user_input == "4":
        ingr = db.get_all_ingredients()
        if ingr:
            print_all_ingredients("All", ingr)
        else:
            print("No ingredient found!")
        print("------------\n")
    elif user_input == "5":
        add_recipe_ing()
    elif user_input == "6":
        print_all_recipe_ing()
