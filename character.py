# character.py

from inventory import Inventory
import random


class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.hp = 100  # Starting health points
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.level = 1
        self.exp = 0
        self.skills = []
        self.inventory = Inventory()  # Initialize inventory with starting gold and items

        # Define character classes with unique stats and skills
        if char_class == "Warrior":
            self.hp += 20
            self.attack += 5
            self.skills = ["Power Strike", "Shield Bash"]
        elif char_class == "Mage":
            self.hp -= 10
            self.attack += 10
            self.skills = ["Fireball", "Ice Spike"]
        elif char_class == "Rogue":
            self.attack += 3
            self.defense += 2
            self.skills = ["Backstab", "Smoke Bomb"]
        elif char_class == "Archer":
            self.attack += 4
            self.skills = ["Arrow Shot", "Camouflage"]
        elif char_class == "Paladin":
            self.hp += 15
            self.defense += 5
            self.skills = ["Holy Light", "Divine Shield"]
        elif char_class == "Assassin":
            self.attack += 8
            self.hp -= 5
            self.skills = ["Shadow Strike", "Vanish"]

        self.current_location = None  # Track the player's current location for location-based effects

    def attack_enemy(self, enemy):
        """Method to attack an enemy, calculating damage with random critical hits."""
        if enemy.hp <= 0:
            print(f"{enemy.name} has already been defeated.")
            return

        damage = self.attack + random.randint(-3, 3)  # Random variation in attack power
        critical_hit_chance = 0.2  # 20% chance for critical hit
        if random.random() < critical_hit_chance:
            damage *= 2
            print("Critical hit!")

        enemy.take_damage(damage)
        print(f"{self.name} attacks {enemy.name} for {damage} damage.")

        if enemy.hp <= 0:
            print(f"{enemy.name} has been defeated!")
            self.gain_exp(enemy.exp_reward)
        else:
            print(f"{enemy.name} has {enemy.hp} HP remaining.")

    def level_up(self):
        """Increases character stats upon leveling up, with experience scaling."""
        self.level += 1
        self.exp = 0  # Reset experience for next level
        self.hp += 10  # Increase maximum health points
        self.attack += 2  # Increase attack power
        self.defense += 1  # Increase defense stat
        self.max_hp += 10  # Max HP increases with level up
        print(f"{self.name} leveled up to level {self.level}!")
        print(f"New stats - HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}")

    def gain_experience(self, amount):
        """Gain experience and level up if enough experience is acquired."""
        self.exp += amount
        required_exp = 50 * (1.5 ** (self.level - 1))  # Scaling experience needed to level up
        if self.exp >= required_exp:
            self.level_up()
            self.exp -= required_exp  # Carry over extra experience

    def take_damage(self, amount):
        """Reduces character HP based on incoming damage."""
        actual_damage = max(amount - self.defense, 0)  # Defense mitigates damage
        self.hp -= actual_damage
        if self.hp <= 0:
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} took {actual_damage} damage, remaining HP: {self.hp}")

    def use_skill(self, skill_name, target):
        """Uses a skill in combat, with skill effects based on the character class."""
        if skill_name not in self.skills:
            print(f"{self.name} doesn't know {skill_name}.")
            return

        if skill_name == "Power Strike":
            damage = self.attack * 1.5
            target.take_damage(damage)
            print(f"{self.name} used {skill_name} on {target.name}, dealing {damage} damage!")
        elif skill_name == "Fireball":
            damage = self.attack * 2
            target.take_damage(damage)
            print(f"{self.name} cast {skill_name}, dealing {damage} fire damage to {target.name}!")
        elif skill_name == "Backstab":
            damage = self.attack * 2.5
            target.take_damage(damage)
            print(f"{self.name} used {skill_name}, dealing {damage} critical damage to {target.name}!")
        elif skill_name == "Holy Light":
            self.hp = min(self.max_hp, self.hp + 15)
            print(f"{self.name} used {skill_name} and healed for 15 HP.")
        # Additional skills can be added with specific effects as needed

    def __repr__(self):
        return (f"{self.name} (Class: {self.char_class}, Level: {self.level}, HP: {self.hp}, "
                f"Attack: {self.attack}, Defense: {self.defense}, Gold: {self.inventory.gold})")

    def equip_item(self, item):
        """Equips an item, applying its stats if it's a weapon or armor."""
        if item.item_type in ["Weapon", "Armor"]:
            # If an item is already equipped, replace it and reset stats
            if item.item_type == "Weapon" and hasattr(self, "equipped_weapon"):
                print(f"Unequipping {self.equipped_weapon.name}.")
                self.attack -= self.equipped_weapon.attack_bonus
                self.inventory.add_item(self.equipped_weapon)
            elif item.item_type == "Armor" and hasattr(self, "equipped_armor"):
                print(f"Unequipping {self.equipped_armor.name}.")
                self.defense -= self.equipped_armor.defense_bonus
                self.inventory.add_item(self.equipped_armor)

            # Equip new item and apply its bonuses
            if item.item_type == "Weapon":
                self.equipped_weapon = item
                self.attack += item.attack_bonus
            elif item.item_type == "Armor":
                self.equipped_armor = item
                self.defense += item.defense_bonus

            print(f"{self.name} has equipped {item.name}!")
            self.inventory.remove_item(item)
        else:
            print(f"{item.name} cannot be equipped.")# inventory.py

class Item:
    def __init__(self, name, description, item_type, price=0, attack_bonus=0, defense_bonus=0):
        self.name = name
        self.description = description
        self.item_type = item_type  # E.g., 'heal', 'boost', 'Weapon', 'Armor', etc.
        self.price = price  # Price for buying/selling
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus

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

    def equip_item(self, item_name, character):
        """Equips a weapon or armor, if possible, and applies its bonuses."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                if item.item_type not in ["Weapon", "Armor"]:
                    print(f"{item.name} cannot be equipped.")
                    return
                # Handle equipping item by applying its bonuses
                if item.item_type == "Weapon":
                    if hasattr(character, "equipped_weapon"):
                        # Unequip the existing weapon
                        character.attack -= character.equipped_weapon.attack_bonus
                        self.add_item(character.equipped_weapon)
                        print(f"Unequipped {character.equipped_weapon.name}.")
                    character.equipped_weapon = item
                    character.attack += item.attack_bonus
                elif item.item_type == "Armor":
                    if hasattr(character, "equipped_armor"):
                        # Unequip the existing armor
                        character.defense -= character.equipped_armor.defense_bonus
                        self.add_item(character.equipped_armor)
                        print(f"Unequipped {character.equipped_armor.name}.")
                    character.equipped_armor = item
                    character.defense += item.defense_bonus

                # Remove item from inventory after equipping
                self.remove_item(item_name)
                print(f"{character.name} has equipped {item.name}!")
                return
        print(f"{item_name} not found in inventory.")

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

    def display_stats(self):
        """Displays the character's current stats."""
        print("\n===== Player Stats =====")
        print(f"Name: {self.name}")
        print(f"Class: {self.char_class}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Level: {self.level}")
        print(f"Experience: {self.exp}")
        print(f"Gold: {self.inventory.gold}")
        print("Skills: " + ", ".join(self.skills) if self.skills else "None")
        print("Current Location: " + self.current_location.name if self.current_location else "None")
        print("========================\n")