from modules import user_logic as ul
from modules.user_menu import *


print(welcome)  # prints the welcome string

# delete menu dictionary, with each key pointing to a function
dict_del_menu = {
    '1': ul.del_recipe, '2': ul.del_ingredient,
    '3': ul.del_all_recipes, '4': ul.del_all_ingredients,
}


def del_menu():
    """
        This is the Delete function
        accessing the {dict_del_menu} dictionary
    """
    while (user_input := input(delete_menu)) != "5":
        if user_input in dict_del_menu:
            dict_del_menu[user_input]()


# Main menu dictionary, with each key pointing to a function
dict_menu = {
    '1': ul.add_recipe, '2': ul.add_ingredient,
    '3': ul.show_recipes, '4': ul.show_ingredients,
    '5': ul.add_ingredient_to_recipe,
    '6': ul.print_all_recipe_ing,
    '7': del_menu
}


def main_menu():
    """
        This is the Main menu function
        accessing the {dict_menu} dictionary
    """
    while (user_input := input(menu)) != "8":
        if user_input in dict_menu:
            dict_menu[user_input]()


if __name__ == "__main__":
    main_menu()
