# location.py

class Location:
    def __init__(self, name, description, environment_effect, required_item=None):
        """
        Initialize a location with a name, description, environment effect, and an optional required item
        to counteract the environment effect.
        """
        self.name = name
        self.description = description
        self.environment_effect = environment_effect  # e.g., {'damage_debuff': 0.8} or {'defense_buff': 1.2}
        self.required_item = required_item  # An item name that can counteract the effect

    def apply_effect(self, player):
        """
        Apply the environmental effect to the player unless they have the required item.
        """
        if self.required_item and any(item.name == self.required_item for item in player.inventory.items):
            print(f"{self.required_item} protects {player.name} from {self.name}'s harsh conditions!")
            return  # Effect is countered by the required item

        # Apply debuffs/buffs based on environment effect
        for attribute, multiplier in self.environment_effect.items():
            if attribute == 'damage_debuff':
                player.attack = int(player.attack * multiplier)
                print(f"{player.name}'s attack power is reduced due to the {self.name} environment.")
            elif attribute == 'defense_buff':
                player.defense = int(player.defense * multiplier)
                print(f"{player.name} feels more resilient in the {self.name}.")

    def remove_effect(self, player):
        """
        Revert any effects applied to the player when they leave the location.
        """
        for attribute, multiplier in self.environment_effect.items():
            if attribute == 'damage_debuff':
                player.attack = int(player.attack / multiplier)
            elif attribute == 'defense_buff':
                player.defense = int(player.defense / multiplier)


# Define specific locations
winter_forest = Location(
    name="Winter Forest",
    description="A cold, snowy forest where the temperature is bitterly low.",
    environment_effect={'damage_debuff': 0.8},  # 20% reduction in attack power
    required_item="Winter Coat"
)

desert = Location(
    name="Desert",
    description="A hot, dry desert with relentless sun beating down.",
    environment_effect={'damage_debuff': 0.9},  # 10% reduction in attack power
    required_item="Sun Hat"
)

cave = Location(
    name="Dark Cave",
    description="A dark, damp cave where stealth is easier.",
    environment_effect={'defense_buff': 1.2}  # 20% increase in defense
)

# Location registry (could be expanded as needed)
locations = {
    "Winter Forest": winter_forest,
    "Desert": desert,
    "Cave": cave
}
