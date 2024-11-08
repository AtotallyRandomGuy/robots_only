# game.py

import json
import os
from character import Character
from enemy import enemies_by_location
from combat import combat
from inventory import Item, Inventory  # Ensure Inventory is imported correctly
from shop import Shop
from location import locations

SAVE_DIR = "saves"

def save_game(player):
    """Save the player's data to a file."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    save_data = {
        "name": player.name,
        "class": player.char_class,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "attack": player.attack,
        "defense": player.defense,
        "level": player.level,
        "exp": player.exp,
        "skills": player.skills,
        "inventory": [{
            "name": item.name,
            "description": item.description,
            "type": item.item_type  # Ensure that each item has the "type" field
        } for item in player.inventory.items],
        "gold": player.inventory.gold,
        "location": player.current_location.name if player.current_location else None
    }

    with open(f"{SAVE_DIR}/{player.name}.json", "w") as f:
        json.dump(save_data, f, indent=4)
    print(f"Game saved for {player.name}.")

def load_game(name):
    """Load the player's data from a file."""
    try:
        with open(f"{SAVE_DIR}/{name}.json", "r") as f:
            save_data = json.load(f)

        # Re-create the player character
        player = Character(save_data["name"], save_data["class"])
        player.hp = save_data["hp"]
        player.max_hp = save_data["max_hp"]
        player.attack = save_data["attack"]
        player.defense = save_data["defense"]
        player.level = save_data["level"]
        player.exp = save_data["exp"]
        player.skills = save_data["skills"]
        player.inventory = Inventory()  # Ensure Inventory is initialized

        # Re-load the player's items from the save data (without triggering add_item logic)
        for item_data in save_data["inventory"]:
            item_type = item_data.get("type", "misc")  # Default to "misc" if 'type' is missing
            item = Item(item_data["name"], item_data["description"], item_type)
            player.inventory.items.append(item)  # Directly append to avoid 'add_item' triggering

        player.inventory.gold = save_data["gold"]

        if save_data["location"]:
            player.current_location = locations.get(save_data["location"])
            if player.current_location:
                player.current_location.apply_effect(player)

        print(f"Game loaded for {player.name}.")
        return player
    except FileNotFoundError:
        print("Save file not found.")
        return None
    except KeyError as e:
        print(f"Error: Missing key in save data - {e}")
        return None

# View all saved characters' stats as before
def view_all_saved_stats():
    """Display stats of all saved characters."""
    if not os.path.exists(SAVE_DIR):
        print("No saved characters found.")
        return

    print("\n--- All Saved Characters' Stats ---")
    for filename in os.listdir(SAVE_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(SAVE_DIR, filename), "r") as f:
                save_data = json.load(f)
                print(f"\nCharacter: {save_data['name']}")
                print(f"  Class: {save_data['class']}")
                print(f"  Level: {save_data['level']}")
                print(f"  HP: {save_data['hp']}/{save_data['max_hp']}")
                print(f"  Attack: {save_data['attack']}")
                print(f"  Defense: {save_data['defense']}")
                print(f"  EXP: {save_data['exp']}")
                print(f"  Gold: {save_data['gold']}")
                print(f"  Location: {save_data['location']}")
                print(f"  Skills: {', '.join(save_data['skills']) if save_data['skills'] else 'None'}")
    print("\n--- End of Stats ---")

# Game Menu and Main Loop
def main_menu():
    """Displays the main menu and handles new game or load game options."""
    print("Welcome to the Adventure Game!")
    while True:
        choice = input("Choose an option: [New Game, Load Game, View Saves, Quit]: ").lower()

        if choice == "new game":
            name = input("Enter your character's name: ")
            print("Choose your class: [Warrior, Mage, Rogue, Archer, Paladin, Assassin]")
            char_class = input("Enter class name: ")
            return Character(name, char_class)

        elif choice == "load game":
            name = input("Enter the name of the character to load: ")
            player = load_game(name)
            if player:
                return player  # Successfully loaded character

        elif choice == "view saves":
            view_all_saved_stats()

        elif choice == "quit":
            print("Goodbye!")
            exit()

        else:
            print("Invalid option. Try again.")

def check_win_condition():
    """Check if all enemies in each location have been defeated."""
    for location, enemies in enemies_by_location.items():
        if any(enemy.is_alive() for enemy in enemies):
            return False  # Game is not won yet; enemies still remain
    return True  # All enemies defeated; player wins!

def main():
    player = main_menu()  # Start at the main menu
    shop = Shop()  # Initialize the shop

    def change_location(location_name):
        if player.current_location:
            player.current_location.remove_effect(player)

        new_location = locations.get(location_name)
        if not new_location:
            print("Unknown location.")
            return

        print(f"\nYou travel to {new_location.name}. {new_location.description}")
        new_location.apply_effect(player)
        player.current_location = new_location
        print()  # Extra space after location change

    # Game loop
    while player.hp > 0:
        action = input(
            "\nWhat would you like to do? [Explore, Check Inventory, Travel, Visit Shop, Use Skill, Save, View Stats, Quit]: ").lower()

        if action == "explore":
            if player.current_location:
                location_enemies = enemies_by_location.get(player.current_location.name)
                if location_enemies:
                    combat(player, location_enemies)  # Engage in combat

                    # Check for win condition after combat
                    if check_win_condition():
                        print("\nCongratulations! You have defeated all enemies in each location and won the game!")
                        print("Thank you for playing!")
                        break  # End the game loop if player has won
                else:
                    print(f"There are no enemies in the {player.current_location.name}.")
            else:
                print("You need to be in a location to explore!")
            print()  # Added blank line for spacing


        elif action == "check inventory":
            while True:
                player.inventory.display_inventory()
                sub_action = input("Manage inventory: [Sort, Discard, Sell, Use Item, Exit]: ").lower()
                if sub_action == "sort":
                    player.inventory.sort_items()
                elif sub_action == "discard":
                    item_name = input("Enter item name to discard: ")
                    player.inventory.remove_item(item_name)
                elif sub_action == "sell":
                    item_name = input("Enter item name to sell: ")
                    player.inventory.sell_item(item_name)
                elif sub_action == "use item":
                    item_name = input("Enter item name to use: ")
                    item = player.inventory.get_item(item_name)  # Retrieve the item from inventory
                    if item:
                        player.inventory.use_item(item)  # Assuming there's a `use_item` method in `Inventory`
                        print()  # Extra space after using item
                    else:
                        print(f"Item '{item_name}' not found in your inventory.")
                elif sub_action == "exit":
                    print("Exiting inventory.")
                    break
                else:
                    print("Invalid inventory management action. Please choose again.")
                    print()  # Extra space after an invalid action

        elif action == "travel":
            print("Available locations: " + ", ".join(locations.keys()))
            location_choice = input("Enter the name of the location you want to travel to, or type 'exit' to cancel: ")
            if location_choice.lower() == "exit":
                print("Travel canceled.")
            else:
                change_location(location_choice)

        elif action == "visit shop":
            while True:
                shop.display_items()
                shop_action = input("Would you like to buy or sell? [Buy, Sell, Exit]: ").lower()
                if shop_action == "buy":
                    item_name = input("Enter item name to buy, or type 'exit' to cancel: ")
                    if item_name.lower() == "exit":
                        print("Purchase canceled.")
                    else:
                        shop.buy_item(item_name, player)
                elif shop_action == "sell":
                    item_name = input("Enter item name to sell, or type 'exit' to cancel: ")
                    if item_name.lower() == "exit":
                        print("Sale canceled.")
                    else:
                        player.inventory.sell_item(item_name)
                elif shop_action == "exit":
                    print("Exiting shop.")
                    break
                else:
                    print("Invalid shop action. Please choose again.")
                    print()  # Extra space after shop actions

        elif action == "use skill":
            print(f"Available skills: {', '.join(player.skills)}")
            skill_choice = input("Enter skill to use, or type 'exit' to cancel: ")
            if skill_choice.lower() == "exit":
                print("Skill usage canceled.")
            elif player.current_location:
                location_enemies = enemies_by_location.get(player.current_location.name)
                if location_enemies:
                    enemy = choice(location_enemies)
                    player.use_skill(skill_choice, enemy)
                    print()  # Extra space after using skill
                else:
                    print(f"No enemies in {player.current_location.name} to use skills on.")
                    print()  # Extra space after no enemies found
            else:
                print("You need to be in a location to use skills!")
                print()  # Extra space after error

        elif action == "save":
            save_game(player)
            print()  # Extra space after saving

        elif action == "view stats":
            view_all_saved_stats()

        elif action == "quit":
            print("Thanks for playing!")
            break

        else:
            print("Invalid action. Try again.")
            print()  # Extra space after invalid action

if __name__ == "__main__":
    main()
