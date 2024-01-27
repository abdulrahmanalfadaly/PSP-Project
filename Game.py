import json
import random
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
class Character:
    def __init__(self, name, char_class, health, attack):
        self.name = name
        self.char_class = char_class
        self.health = health
        self.max_health = health
        self.attack = attack
        self.inventory = ["Sword"]
        self.obtained_weapons = []
        self.current_dungeon = 1

def equip_weapon(character, weapon_name, attack_modifier, health_modifier):
    character.inventory.append(weapon_name)
    character.obtained_weapons.append(weapon_name)
    character.attack += attack_modifier
    character.max_health += health_modifier
    character.health = min(character.health + health_modifier, character.max_health)
    print(f"You equipped {weapon_name}! Your attack is now {character.attack} and your health is now {character.health}")

def get_weapon_by_name(character, weapon_name):
    for weapon in load_json_data('weapons.json'):
        if weapon['name'] == weapon_name and weapon_name in character.inventory:
            return weapon
    return None

def apply_special_abilities(character, enemy):
    inferno_blade = get_weapon_by_name(character, "Inferno Blade")
    shieldbreaker = get_weapon_by_name(character, "Shieldbreaker")
    frost_bite_dagger = get_weapon_by_name(character, "Frost Bite Dagger")

    #Inferno Blade ability
    if inferno_blade and 'special_ability' in inferno_blade:
        burn_chance = inferno_blade['special_ability']['chance']
        if random.randint(1, 100) <= burn_chance:
            burn_damage = inferno_blade['special_ability']['damage']
            enemy.health -= burn_damage
            print(f"The {enemy.name} is burned for {burn_damage} damage!")
            time.sleep(1)

    #Shieldbreaker ability
    if shieldbreaker and 'special_ability' in shieldbreaker:
        defense_break_chance = shieldbreaker['special_ability']['chance']
        if random.randint(1, 100) <= defense_break_chance:
            defense_reduction = shieldbreaker['special_ability']['reduction']
            adjusted_enemy_damage = max(0, enemy.attack - defense_reduction)
            print(f"The {enemy.name}'s defense is broken! Enemy damage reduced from {enemy.attack} to {adjusted_enemy_damage}.")
            time.sleep(1)
        else:
            adjusted_enemy_damage = enemy.attack
    else:
        adjusted_enemy_damage = enemy.attack 

    #Frost Bite Dagger ability
    if frost_bite_dagger and 'special_ability' in frost_bite_dagger:
        freeze_chance = frost_bite_dagger['special_ability']['chance']
        if random.randint(1, 100) <= freeze_chance:
            print(f"The {enemy.name} is frozen and cannot attack!")
            time.sleep(1)
            return adjusted_enemy_damage, True  
    
    return adjusted_enemy_damage, False 
    
class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def create_character():
    clear()
    name = input("\nEnter your character's name: ").strip()
    clear()
    print("\nChoose your class:\n1. Brutality (Health: 30, Attack: 70)\n2. Tactical (Health: 50, Attack: 50)\n3. Survival (Health: 70, Attack: 30)")
    class_choice = input("Enter your choice (1/2/3): ").strip()
    
    if class_choice == '1':
        return Character(name, "Brutality", 30, 70)
    elif class_choice == '2':
        return Character(name, "Tactical", 50, 50)
    elif class_choice == '3':
        return Character(name, "Survival", 70, 30)
    else:
        print("Invalid choice.")
        return create_character()

def dungeon_exploration(character):
    clear()
    dungeons = load_json_data('dungeons.json')
    current_dungeon = dungeons[f"Dungeon Level {character.current_dungeon}"]
    print(f"You have entered Dungeon Level {character.current_dungeon}")

    for _ in range(current_dungeon['enemies']):
        clear()
        enemy = random.choice(load_json_data('enemies.json'))
        enemy_obj = Enemy(enemy['name'], enemy['health'], enemy['attack'])
        result = combat(character, enemy_obj)

        if result == 'defeated':
            return 'defeated'
        elif character.health <= 0:
            print("You have been defeated!")
            return 'defeated'
        elif result:
            print("You have exited the dungeon.")
            return False

    character.current_dungeon += 1
    obtained_weapon = None
    while obtained_weapon is None or obtained_weapon in character.obtained_weapons:
        weapon = random.choice(load_json_data('weapons.json'))
        obtained_weapon = weapon['name']
    
    
    equip_weapon(character, weapon['name'], weapon['attack_modifier'], weapon['health_modifier'])
    character.obtained_weapons.append(obtained_weapon)
    clear()
    print(f"\nCongratulations! You passed the dungeon and got {weapon['name']}")
    time.sleep(3)
    return False

def combat(character, enemy):
    print(f"\nA {enemy.name} appears!")
    while enemy.health > 0 and character.health > 0:
        # Display both player's and enemy's current stats
        print(f"\nEnemy Health: {enemy.health}, Enemy Attack: {enemy.attack}")
        print(f"Your Health: {character.health}, Your Attack: {character.attack}")

        action = input("\nDo you want to (A)ttack, (H)eal or (R)un? ").strip().upper()

        if action == 'A':
            min_damage = int(0.7 * character.attack)
            max_damage = character.attack
            player_damage = random.randint(min_damage, max_damage)
            enemy.health -= player_damage
            print(f"\nYou dealt {player_damage} damage to the {enemy.name}!")
            time.sleep(1)  

            # Check for special abilities 
            adjusted_enemy_damage, freeze_triggered = apply_special_abilities(character, enemy)

            if freeze_triggered:
                continue  

        elif action == 'H':
            character.health = min(character.health + 10, character.max_health)
            print("\nHealing...")
            time.sleep(1)
            clear()
        elif action == 'R':
            print("\nEscaping the Dungeon...")
            time.sleep(1)
            return True
        else:
            clear()
            continue

        enemy_damage = random.randint(int(0.6 * adjusted_enemy_damage), adjusted_enemy_damage)
        character.health -= enemy_damage
        print(f"\nThe {enemy.name} dealt {enemy_damage} damage to you!")

        character.health -= enemy.attack
        if character.health <= 0:
            print("\nYou have been defeated!")
            time.sleep(2)
            return 'defeated'
        if enemy.health <= 0:
            print(f"\nYou defeated the {enemy.name}!")
            time.sleep(2)

    return False

def save_game(character):
    save_data = {
        'name': character.name,
        'health': character.health,
        'attack': character.attack,
        'player_class': character.char_class,
        'inventory': character.inventory,
        'current_dungeon': character.current_dungeon,
        'obtained_weapons': character.obtained_weapons
    }
    with open('game_save.json', 'w') as file:
        json.dump(save_data, file)

def load_game():
    try:
        with open('game_save.json', 'r') as file:
            save_data = json.load(file)
        character = Character(save_data['name'], save_data['player_class'], save_data['health'], save_data['attack'])
        character.inventory = save_data        ['inventory']
        character.current_dungeon = save_data['current_dungeon']
        return character
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        return create_character()

def main_menu():
    clear()
    choice = input("\nWelcome to the Dungeon Adventure Game!\n\n-Do you want to (N)ew game or (L)oad game? ").strip().upper()
    if choice == 'L':
        return load_game()
    elif choice == 'N':
        return create_character()
    else:
        print("Invalid choice. Please enter 'N' for New Game or 'L' for Load Game.")
        return main_menu()

def main_game_loop(character):
    while True:
        clear()
        print(f"\nName: {character.name}\nClass: {character.char_class}\nHealth: {character.health}\nAttack: {character.attack}\nInventory: {character.inventory}\nCurrent Dungeon: {character.current_dungeon}")
        choice = input("\nWhat would you like to do?  1) Dungeons  2) Rest  3) Save: ").strip()

        if choice == '1':
            result = dungeon_exploration(character)
            if result == 'defeated':
                print("\nYou have been defeated! Restarting the current dungeon level...")
                character.health = character.max_health  # Reset health
                # No change to character.current_dungeon
                continue  # Continue the loop to retry the current dungeon level
        elif choice == '2':
            character.health = character.max_health
            print("\nResting...")
            time.sleep(1)
        elif choice == '3':
            save_game(character)
            print("\nGame Saved.")
            time.sleep(1)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    while True:
        character = main_menu()
        main_game_loop(character)
