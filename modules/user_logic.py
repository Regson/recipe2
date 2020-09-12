import itertools

from modules import database as db

db.create_tables()  # Creates tables for the database


# this function is used as a hint for Adding of recipe and ingredients
def instruction(item):
    print(
        f"You can enter multiple {item} "
        "just separate them with a , e.g item1,item2,item3"
    )


# prints all Recipes or Ingredients depending on where it is called
def print_all_items(header, names):
    print(f"<-- {header} -->")
    if names:
        for _id, (item,) in enumerate(names, start=1):
            print(f"{_id}. {item}")
    else:
        print(f"No {header} found!")

    print("------------\n")


# prints all ingredients for the selected recipe
def print_all_recipe_ing():
    name = input("Recipe name: ").strip()
    recipe = db.find_recipe_by_name(name)

    if recipe:
        ingredients = db.get_recipe_ing(name)

        if ingredients:
            print_all_items(name + " ingredients", ingredients)
        else:
            print("No ingredients")

    else:
        print(
            f"{name} not found! please go to OPTIONS and add {name}"
            " to Kitchen."
        )


def add_recipe():
    add_item(db.add_recipe, "recipe")


def add_ingredient():
    add_item(db.add_ingredient, "ingredient")


def add_item(func, item_title):
    """
        DISC: This function handles both adding of recipes and ingredients.
    """
    instruction(item_title)
    item_name = input(f"Enter {item_title} name: ").strip()
    if item_name:
        new_name = item_name.split(",")
        new_name = list(filter(None, new_name))
        func(new_name)
    else:
        print("Input CANNOT be blank!\n")


def show_recipes():
    header = "All Recipes"
    recipes = db.get_all_recipe()
    print_all_items(header, recipes)


def show_ingredients():
    header = "All Ingredients"
    ingredients = db.get_all_ingredients()
    print_all_items(header, ingredients)


def add_ingredient_to_recipe():
    """
    This function checks availability of a recipe, if exist,
    it calls the add_recipe_ing function.
    """
    recipe_name = input("Recipe name: ").strip()

    prompt_add_ingredient = f""" Would you like to add another
    ingredient to {recipe_name}? Y/N
    type y if Yes or n if No and press ENTER: """

    if recipe_name:
        add_recipe_ing(recipe_name)
        while (
                ingredient_input := input(prompt_add_ingredient).upper()
        ) != "N":
            if ingredient_input == "Y":
                add_recipe_ing(recipe_name)
    elif not db.find_recipe_by_name(recipe_name):
        print(f"{recipe_name} does not exist!")
    else:
        print("\nInputs CANNOT be Empty!\n")


def add_recipe_ing(recipe_name):
    """
    This function, checks if ingredient exist, checks if ingredient already added to the
    recipe_name entered by user in "add_ingredient_to_recipe" function. If not exist,
    data is saved to the database.
    """
    ingredients_names = input("Ingredient name: ").strip()
    if ingredients_names:
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

    else:
        print("\nInputs CANNOT be Empty!\n")


# calls the delete function
def del_recipe():
    del_item("recipe name", db.del_recipe, db.find_recipe_by_name)


def del_ingredient():
    del_item("ingredient name", db.del_ingredient, db.find_ingredient_by_name)


def del_item(header, func, get_func):
    item_name = input(f"Enter {header} to delete: ").strip()

    if item_name:
        if get_func(item_name):
            func(item_name)
            print(f"{item_name} deleted successfully")
        else:
            print(f"\n{item_name} does not exist!\n")
    else:
        print("\nInput CANNOT be Empty!\n")


def del_all_recipes():
    del_all_item("RECIPES", db.del_all_recipe)


def del_all_ingredients():
    del_all_item("INGREDIENTS", db.del_all_ingredient)


def del_all_item(header, func):
    del_prompt = input(f"Are you sure you want to delete ALL {header} y/n?: ").upper()
    if del_prompt == "Y":
        func()
        print(f"All {header} deleted successfully!")
    elif del_prompt == "N":
        pass  # do I use pass or break?
    else:
        print("Invalid choice! Try again.")
