# enemy.py
from inventory import Item
from random import choice

class Enemy:
    def __init__(self, name, hp, attack, defense, location, drop_items=None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.location = location  # Location where the enemy can be found
        self.drop_items = drop_items or []

    def attack_player(self, player):
        damage = max(1, self.attack - player.defense)
        player.hp -= damage
        print(f"{self.name} attacks {player.name} for {damage} damage!")

    def take_damage(self, damage):
        """Reduces the enemy's HP by the specified damage amount."""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} takes {damage} damage. Remaining HP: {self.hp}")

    def drop_item(self):
        """Randomly select an item from the enemy's drop list if available."""
        if self.drop_items:
            return choice(self.drop_items)
        return None

    def is_alive(self):
        """Returns True if the enemy is still alive, False otherwise."""
        return self.hp > 0

    def exp_reward(self):
        """
        Calculate experience reward based on the enemy's stats.
        A higher HP, attack, and defense results in a higher experience reward.
        """
        base_xp = 10  # Base XP for the simplest enemy
        xp = base_xp + (self.hp * 0.2) + (self.attack * 1.5) + (self.defense * 1.2)
        return int(xp)

# Define specific enemies for each location
goblin = Enemy(
    name="Goblin",
    hp=30,
    attack=10,
    defense=2,
    location="Dark Cave",  # Change to match location name used in the game
    drop_items=[
        Item("Torch", "Illuminates dark areas.", "passive"),
        Item("Small Potion", "Restores 10 HP.", "heal")
    ]
)

snow_wolf = Enemy(
    name="Snow Wolf",
    hp=45,
    attack=15,
    defense=4,
    location="Winter Forest",
    drop_items=[
        Item("Winter Coat", "Protects against cold weather debuffs.", "passive"),
        Item("Fur Pelt", "Can be sold or traded.", "misc")
    ]
)

sand_scorpion = Enemy(
    name="Sand Scorpion",
    hp=40,
    attack=12,
    defense=3,
    location="Desert",
    drop_items=[
        Item("Sun Hat", "Protects against heat debuffs.", "passive"),
        Item("Scorpion Venom", "Used for crafting poisons.", "misc")
    ]
)

# Enemy registry for easier access
enemies_by_location = {
    "Dark Cave": [goblin],
    "Winter Forest": [snow_wolf],
    "Desert": [sand_scorpion]
}
