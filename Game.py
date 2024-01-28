# *********************************************************
# Program: Dungeon Adventure Game.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL4L?
# Year: 2024/25 Trimester 2
# Names: Abdelrahman | Amir | Kumarish | 
# IDs: 1221104939 | 1221106717 | 1221109491
# Emails: 1221104939@student.mmu.edu.my | 1221106717@student.mmu.edu.my | 1221109491@student.mmu.edu.my
# Phones: 0194853195 | 0194476225 | 0189292447
# *********************************************************

import json
import random
import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_json_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
        time.sleep(2)
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_name}.")
        time.sleep(2)
        return None

def input_with_prompt(prompt, valid_options=None):
    while True:
        user_input = input(prompt).strip().upper()
        if valid_options and user_input not in valid_options:
            continue
        return user_input

class Character:
    def __init__(self, name, char_class, health, attack):
        self.name = name
        self.char_class = char_class
        self.health = health
        self.max_health = health
        self.attack = attack
        self.inventory = ["Sword"]  # Default weapon, ensure to load weapon details including effects
        self.current_dungeon = 1
        self.weapon_effects = []  # Added to store weapon effects

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
        clear()
        print("\nHealing...")
        time.sleep(1)
        print(f"\nYour health is now {self.health}")
        time.sleep(1)

    def take_damage(self, amount):
        self.health -= amount
        print(f"\nYou took {amount} damage! Your health is now {self.health}")
        time.sleep(1)

    def attack_enemy(self, enemy):
        self.apply_weapon_effects()  # Apply effects before calculating damage
        min_damage = int(0.7 * self.attack)
        max_damage = self.attack
        player_damage = random.randint(min_damage, max_damage)
        enemy.health -= player_damage
        clear()
        print(f"\nYou dealt {player_damage} damage to the {enemy.name}!")
        time.sleep(1)
        return player_damage
    
    def load_weapon_effects(self):
        for weapon in load_json_data('weapons.json'):
            if weapon['name'] in self.inventory:
                self.weapon_effects = weapon.get('effects', [])
    def apply_weapon_effects(self):
        for effect in self.weapon_effects:
            if random.randint(1, 100) <= effect['chance']:
                if effect['effect'] == 'increase_player_attack':
                    print("Your weapon's inferno blaze increases your attack!")
                    self.attack += 5  # Example modifier, adjust as needed
                elif effect['effect'] == 'reduce_enemy_attack':
                    # This effect would need to be considered in the enemy attack logic
                    print("Your weapon's shieldbreaker effect is ready, but needs implementation.")
                elif effect['effect'] == 'prevent_enemy_attack':
                    # This effect would need to be considered in the enemy attack logic
                    print("Your weapon's frost bite effect is ready, but needs implementation.")



class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, amount):
        self.health -= amount
        print(f"\nThe {self.name} took {amount} damage! Its health is now {self.health}")

def create_character():
    clear()
    name = input("\nEnter your character's name: ").strip()
    clear()
    print("\nChoose your class:\n1. Brutality (Health: 30, Attack: 70)\n2. Tactical (Health: 50, Attack: 50)\n3. Survival (Health: 70, Attack: 30)")
    class_choice = input_with_prompt("Enter your choice (1/2/3): ", ['1', '2', '3'])
    
    if class_choice == '1':
        return Character(name, "Brutality", 30, 70)
    elif class_choice == '2':
        return Character(name, "Tactical", 50, 50)
    elif class_choice == '3':
        return Character(name, "Survival", 70, 30)

def equip_weapon(character, weapons):
    # This function now also triggers loading of weapon effects
    # Filter out weapons already in the inventory
    new_weapons = [weapon for weapon in weapons if weapon['name'] not in character.inventory]
    
    # If all weapons are already in inventory, print a message and return
    if not new_weapons:
        print("You already have all available weapons.")
        return
    
    # Randomly choose a new weapon from the filtered list
    weapon = random.choice(new_weapons)
    character.inventory.append(weapon['name'])
    character.attack += weapon['attack_modifier']
    character.max_health += weapon['health_modifier']
    character.health = min(character.health + weapon['health_modifier'], character.max_health)
    character.load_weapon_effects()  # Load effects whenever a new weapon is equipped
    print(f"\nYou found {weapon['name']}! Your attack and health is now increased")
    time.sleep(3)

def dungeon_exploration(character):
    clear()
    dungeons = load_json_data('dungeons.json')
    if not dungeons:
        return 'error'
    current_dungeon = dungeons.get(f"Dungeon Level {character.current_dungeon}")
    if not current_dungeon:
        print("Error: Dungeon data is missing or corrupted.")
        time.sleep(2)
        return 'error'
    
    print(f"\nYou have entered Dungeon Level {character.current_dungeon}")
    time.sleep(2)

    for _ in range(current_dungeon['enemies']):
        clear()
        enemies = load_json_data('enemies.json')
        if not enemies:
            return 'error'
        enemy = random.choice(enemies)
        enemy_obj = Enemy(enemy['name'], enemy['health'], enemy['attack'])
        result = combat(character, enemy_obj)

        if result == 'defeated':
            print("\nRestarting from Dungeon 1...")
            character.current_dungeon = 1
            character.health = character.max_health
            time.sleep(2)
            return 'defeated'
        elif result == 'escaped':
            return 'escaped'
        
         # Player has passed the dungeon, announce it here
    clear()
    print(f"\nCongratulations, {character.name}! You have successfully passed Dungeon Level {character.current_dungeon}!")
    time.sleep(2)

    character.current_dungeon += 1
    weapons = load_json_data('weapons.json')
    if not weapons:
        return 'error'
    
    # Pass the entire list of weapons to equip_weapon
    equip_weapon(character, weapons)
    clear()
    time.sleep(2)
    return 'victory'

def combat(character, enemy):
    print(f"\nA {enemy.name} appears!")
    time.sleep(1)

    while enemy.health > 0 and character.health > 0:
        print(f"\nEnemy Health: {enemy.health}, Enemy Attack: {enemy.attack}")
        print(f"Your Health:  {character.health}, Your Attack: {character.attack}")

        action = input_with_prompt("\nDo you want to (A)ttack, (H)eal or (R)un? ", ['A', 'H', 'R'])

        if action == 'A':
            character.attack_enemy(enemy)

        elif action == 'H':
            character.heal(10)  # Assume a fixed healing amount or a calculation based on character stats

        elif action == 'R':
            clear()
            print("\nEscaping the Dungeon...")
            time.sleep(2)
            return 'escaped'

        if enemy.health > 0:
            enemy_damage = random.randint(int(0.7 * enemy.attack), enemy.attack)
            character.take_damage(enemy_damage)

        if character.health <= 0:
            print("\nYou have been defeated!")
            character.inventory = ["Sword"]  # Reset inventory to default weapon
            character.load_weapon_effects()  # Reload weapon effects for the default weapon
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
        character.inventory = save_data['inventory']
        character.current_dungeon = save_data['current_dungeon']
        return character
    except (FileNotFoundError, json.JSONDecodeError) as e:
        clear()
        print("\nNo saved game found or there's an error with the save file. Starting a new game.")
        time.sleep(2)
        return create_character()

def main_menu():
    clear()
    choice = input_with_prompt("\nWelcome to the Dungeon Adventure Game!\n\n-Do you want to (N)ew game or (L)oad game? ", ['N', 'L'])
    if choice == 'L':
        return load_game()
    elif choice == 'N':
        return create_character()

def main_game_loop(character):
    while True:
        clear()
        print(f"\nName: {character.name}\nClass: {character.char_class}\nHealth: {character.health}\nAttack: {character.attack}\nInventory: {character.inventory}\nCurrent Dungeon: {character.current_dungeon}")
        choice = input_with_prompt("\nWhat would you like to do?  1) Dungeons  2) Rest  3) Save: ", ['1', '2', '3'])

        if choice == '1':
            result = dungeon_exploration(character)
            if result in ['defeated']:
                character.current_dungeon = max(1, character.current_dungeon - 1)
                character.heal(character.max_health)
        elif choice == '2':
            character.heal(character.max_health)
        elif choice == '3':
            save_game(character)
            print("\nGame Saved.")
            time.sleep(2)

if __name__ == "__main__":
    while True:
        character = main_menu()
        character.load_weapon_effects()  # Ensure effects are loaded at game start
        main_game_loop(character)