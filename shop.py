# shop.py

from inventory import Item

class Shop:
    def __init__(self):
        self.items_for_sale = [
            Item("Potion", "Heals 20 HP.", "heal", price=10),
            Item("Sword", "Increases attack by 5.", "boost", price=50),
            Item("Shield", "Increases defense by 5.", "boost", price=50),
            Item("Winter Coat", "Protects against cold debuff.", "passive", price=75)
        ]

    def display_items(self):
        print("Welcome to the shop! Here are the items for sale:")
        for item in self.items_for_sale:
            print(item)

    def buy_item(self, item_name, player):
        for item in self.items_for_sale:
            if item.name.lower() == item_name.lower():
                if player.inventory.gold >= item.price:
                    player.inventory.gold -= item.price
                    player.inventory.add_item(item)
                    print(f"{item.name} purchased for {item.price} gold.")
                else:
                    print("Not enough gold to purchase this item.")
                return
        print("Item not found in the shop.")
