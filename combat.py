# combat.py
from random import choice

def combat(player, location_enemies):
    """Simulate combat against all enemies in a specific location."""
    print(f"A hostile creature from the {player.current_location.name} approaches!")

    # Loop through each enemy in the location until either player or enemies are all defeated
    for enemy in location_enemies:
        if not enemy.is_alive():
            continue  # Skip already defeated enemies

        print(f"\nYou encounter a {enemy.name}!")
        while player.hp > 0 and enemy.hp > 0:
            print(f"\n{player.name} HP: {player.hp} | {enemy.name} HP: {enemy.hp}")
            action = input("Choose an action: [1] Attack [2] Power Attack [3] Defend [4] Use Item: ")

            if action == "1":  # Basic attack
                print()  # Extra space
                player.attack_enemy(enemy)

            elif action == "2":  # Power attack with higher risk
                print()  # Extra space
                damage = player.attack * 1.5
                actual_damage = max(1, damage - enemy.defense)
                enemy.hp -= actual_damage
                print(f"{player.name} performs a Power Attack on {enemy.name} for {actual_damage} damage!")
                # Player loses some defense on next enemy turn
                player.defense -= 2
                print(f"{player.name} feels more vulnerable after the Power Attack.")

            elif action == "3":  # Defend to boost defense temporarily
                print()  # Extra space
                player.defense += 5
                print(f"{player.name} takes a defensive stance, raising defense by 5.")

            elif action == "4":  # Use item
                print()  # Extra space
                item_name = input("Enter item name to use: ")
                player.inventory.use_item(item_name, player)

            else:
                print()  # Extra space
                print("Invalid action. Please choose a number between 1 and 4.")

            # Enemy's turn to attack if it's still alive
            if enemy.is_alive():
                enemy.attack_player(player)

            # Reset defense modifications after each turn
            if action == "3":
                player.defense -= 5
            elif action == "2":
                player.defense += 2

        # Check if the enemy has been defeated
        if player.hp > 0 and not enemy.is_alive():
            print(f"{enemy.name} has been defeated!")
            xp_reward = enemy.exp_reward()
            print(f"{player.name} gains {xp_reward} experience points!")
            player.gain_experience(xp_reward)  # Add XP reward to player

            # Check for item drops
            item_drop = enemy.drop_item()
            if item_drop:
                player.inventory.add_item(item_drop)
                print(f"{player.name} has acquired {item_drop.name} from {enemy.name}!")

        # Check if the player is defeated
        if player.hp <= 0:
            print("You have been defeated...")
            break

    # Final message if the player survives the encounter
    if player.hp > 0:
        print("All enemies in this location have been defeated!")
