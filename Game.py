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
        self.current_dungeon = 1

def equip_weapon(character, weapon_name, attack_modifier, health_modifier):
    character.inventory.append(weapon_name)
    character.attack += attack_modifier
    character.max_health += health_modifier
    character.health = min(character.health + health_modifier, character.max_health)
    print(f"You equipped {weapon_name}! Your attack is now {character.attack} and your health is now {character.health}")

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
    weapon = random.choice(load_json_data('weapons.json'))
    equip_weapon(character, weapon['name'], weapon['attack_modifier'], weapon['health_modifier'])
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
            enemy.health -= character.attack
        elif action == 'H':
            character.health = min(character.health + 10, character.max_health)
            print("\nHealing...")
            time.sleep(2)
            clear()
        elif action == 'R':
            print("\nEscaping the Dungeon...")
            time.sleep(2)
            return True
        else:
            clear()
            continue

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
        'current_dungeon': character.current_dungeon
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
            time.sleep(2)
        elif choice == '3':
            save_game(character)
            print("\nGame Saved.")
            time.sleep(2)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    while True:
        character = main_menu()
        main_game_loop(character)
