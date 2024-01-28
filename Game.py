# *********************************************************
# Program: Dungeon Adventure Game.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL4L?
# Year: 2024/25 Trimester 2
# Names: Abdelrahman | Amir | Kumarish | Nizam | 
# IDs: 1221104939 | 1221106717 | 1221109491 | 1221206115
# Emails: 1221104939@student.mmu.edu.my | 1221106717@student.mmu.edu.my | 1221109491@student.mmu.edu.my | 1221206115@student.mmu.edu.my
# Phones: 0194853195 | 0194476225 | 0189292447 | 0104436121
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
        self.inventory = ["Sword"]  
        self.current_dungeon = 1
        self.weapon_effects = []  

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
        self.apply_weapon_effects()  
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
                    self.attack += 5  
                elif effect['effect'] == 'reduce_enemy_attack':
                    print("Your weapon's shieldbreaker effect is ready, but needs implementation.")
                elif effect['effect'] == 'prevent_enemy_attack':
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
   
    new_weapons = [weapon for weapon in weapons if weapon['name'] not in character.inventory]
    
    
    if not new_weapons:
        print("You already have all available weapons.")
        return
    

    weapon = random.choice(new_weapons)
    character.inventory.append(weapon['name'])
    character.attack += weapon['attack_modifier']
    character.max_health += weapon['health_modifier']
    character.health = min(character.health + weapon['health_modifier'], character.max_health)
    character.load_weapon_effects()  # Load effects whenever a new weapon is equipped
    print(f"\nYou found {weapon['name']}! Your attack and health is now increased")
    time.sleep(3)

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)
        
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
        
         
    clear()
    print(f"\nCongratulations, {character.name}! You have successfully passed Dungeon Level {character.current_dungeon}!")
    time.sleep(2)

    character.current_dungeon += 1
    weapons = load_json_data('weapons.json')
    if not weapons:
        return 'error'
    

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
            character.heal(10)  

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
            character.inventory = ["Sword"]  
            character.load_weapon_effects()  
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

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def boss_fight(character):
    boss_data = load_json_data('lastboss.json')
    print("Boss Data:", boss_data)  
    if boss_data and isinstance(boss_data, list) and len(boss_data) > 0:
        boss = boss_data[0]  
        boss_name = boss.get('name')
        boss_health = boss.get('health')
        boss_attack = boss.get('attack')

        while boss_health > 0 and character.health > 0:
            clear()
            print(f"\n{character.name}: {character.health} HP | {boss_name}: {boss_health} HP\n")
            print(f"\nYour Attack: {character.attack}, Enemy Attack: {boss_attack}")
        
            action = input("\nDo you want to (A)ttack, (H)eal, or (R)un? ").strip().upper()
            if action == 'A':
                min_damage = int(0.7 * character.attack)
                max_damage = character.attack
                player_damage = random.randint(min_damage, max_damage)
                boss_health -= player_damage
                print(f"\nYou dealt {player_damage} damage to the {boss_name}!")
                time.sleep(1)  

                character_damage = random.randint(int(0.7 * boss_attack), boss_attack)
                if character.health - character_damage <= 1:
                    character.health = 1
                    print("Nihilus the Titan's attack brings you to the brink of death!")
                    time.sleep(2)
                    trigger_cutscene(character)
                    break
                else:
                    character.health -= character_damage
                    print(f"\nNihilus the Titan attacked you, dealing {character_damage} damage!")
                    time.sleep(1)

            elif action == 'H':
                character.health = min(character.health + 10, character.max_health)
                print("\nHealing...")
                time.sleep(1)
                clear()

            elif action == 'R':
                print("\nYou attempted to flee from it!")
                print("\nNihilus the Titan: Foolish creature!")
                print("\nYou cannot flee from the it!")
                time.sleep(3)
                clear()
                        
    if character.health == 1:
        trigger_cutscene(character)

def trigger_cutscene(character):
    clear()

    print("*You still managed to survive but only 1 hp left*")
    print("*Nihilus the Titan is about to deliver its final strike*")
    input("Press Enter to continue...")
    clear()
    print("*Suddenly, someone in full armor jumps in front of you and blocks the attack*")
    input("Press Enter to continue...")
    clear()
    print("Nihilus the Titan: Impossible! How can a mere creature manage to block my attack!")
    input("Press Enter to continue...")
    clear()
    print("*The armored figure makes a full swing with his greatsword and manages to kill Nihilus the Titan with just one strike*")
    input("Press Enter to continue...")
    clear()
    print(f"{character.name}: [Shocked] Is that...? No, it can't be...")
    input("Press Enter to continue...")
    clear()
    print("Armor Figure: [Turn Around] Pathetic.")
    input("Press Enter to continue...")
    clear()
    print(f"{character.name}: [In disbelief] It's you...")
    input("Press Enter to continue...")
    clear()
    print("Armor Figure: The Demon Lord ask me to end you right now before it's too late.")
    input("Press Enter to continue...")
    clear()
    print(f"{character.name}: [Confused] So he somehow manage to know that I'm still alive then....")
    input("Press Enter to continue...")
    clear()
    print("Armor Figure: [Cynical Face] If I end you right now, it'll not be fun.")
    input("Press Enter to continue...")
    clear()
    print(f"{character.name}: [Resolute] I'll save you from his magic, my friend.")
    input("Press Enter to continue...")
    clear()
    print("Armor Figure: [Little Laughing] We'll meet again in Level 50, then it'll be more entertaining to kill you there.")
    input("Press Enter to continue...")
    clear()
    print("*Armor Figure vanishes within shadows*")
    input("Press Enter to continue...")
    clear()
    print(f"{character.name}: [Sigh] I'll make you know your place again like before, Zod, or maybe should I say, The current Demon King.")
    input("Press Enter to continue...")
    clear()
    input("Press Enter to end the game...")
    clear()

def main_game_loop(character):
    while True:
        clear()
        print(f"\nName: {character.name}\nClass: {character.char_class}\nHealth: {character.health}\nAttack: {character.attack}\nInventory: {character.inventory}\nCurrent Dungeon: {character.current_dungeon}")
        choice = input("\nWhat would you like to do?  1) Dungeons  2) Rest  3) Save: ").strip()

        if choice == '1':
            if character.current_dungeon < 10:
                result = dungeon_exploration(character)
                if result == 'defeated':
                    print("\nYou have been defeated! Restarting the current dungeon level...")
                    character.health = character.max_health  
                    continue 
                if character.current_dungeon == 10:
                    print("\nYou have reached the final dungeon level. Prepare for the ultimate challenge!")
                    input("Press Enter to continue...")
                    boss_fight(character)  
        elif choice == '2':
            character.health = character.max_health
            print("\nResting...")
            time.sleep(1)
        elif choice == '3':
            save_game(character)
            print("\nGame Saved.")
            time.sleep(2)


if __name__ == "__main__":
    while True:
        character = main_menu()
        character.load_weapon_effects()  
        main_game_loop(character)
