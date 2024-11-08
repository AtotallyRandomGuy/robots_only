# inventory.py

class Item:
    def __init__(self, name, description, item_type, price=0):
        self.name = name
        self.description = description
        self.item_type = item_type  # E.g., 'heal', 'boost', 'passive', etc.
        self.price = price  # Price for buying/selling

    def __repr__(self):
        return f"{self.name} - {self.description} (Type: {self.item_type}, Price: {self.price} gold)"


class Inventory:
    def __init__(self):
        self.items = []
        self.gold = 100  # Starting gold for the player

    def add_item(self, item):
        self.items.append(item)
        print(f"{item.name} added to inventory.")

    def remove_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                print(f"{item.name} removed from inventory.")
                return
        print("Item not found in inventory.")

    def use_item(self, item_name, character):
        """Use an item, applying its effect based on type."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                if item.item_type == "heal":
                    character.hp = min(character.max_hp, character.hp + 20)
                    print(f"{character.name} used {item.name} and restored HP!")
                elif item.item_type == "boost":
                    character.attack += 5
                    print(f"{character.name} used {item.name}, increasing attack!")
                self.items.remove(item)
                return
        print("Item not found in inventory.")

    def sort_items(self):
        self.items.sort(key=lambda x: x.name)
        print("Inventory sorted by item name.")

    def display_inventory(self):
        print(f"Gold: {self.gold}")
        if not self.items:
            print("Inventory is empty.")
        else:
            for item in self.items:
                print(item)

    def sell_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.gold += item.price
                self.items.remove(item)
                print(f"Sold {item.name} for {item.price} gold.")
                return
        print("Item not found in inventory.")
