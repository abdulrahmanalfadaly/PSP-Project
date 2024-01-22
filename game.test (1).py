import random

class Player:
    def __init__(self, name, health=100, attack=15, player_class="", weapon=""):
        self.name = name
        self.health = health
        self.attack = attack
        self.player_class = player_class
        self.weapon = weapon
        self.current_dungeon_level = 1

    def choose_class(self):
        print("Choose your class:")
        print("2. Tactical")
        print("3. Survival")

        choice = input("Enter the number of your choice: ")
        if choice == "1":
            self.player_class = "Brutality"
            self.attack += 15
            self.weapon = "Wooden Sword"
        elif choice == "2":
            self.player_class = "Tactical"
            self.health += 25
            self.attack += 7.5
            self.weapon = "Bow"
        elif choice == "3":
            self.player_class = "Survival"
            self.health += 50
            self.weapon = "Wooden Axe"
        else:
            print("Invalid choice. Defaulting to Brutality.")

    def display_stats(self):
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"Class: {self.player_class}")
        print(f"Weapon: {self.weapon}")
        print(f"Dungeon Level: {self.current_dungeon_level}")

    def attack_enemy(self):
        return random.randint(int(0.6 * self.attack), self.attack)

    def upgrade_attributes(self):
        self.health = int(self.health * 1.5)
        self.attack = int(self.attack * 1.25)

    def encounter_enemy(self):
        enemy_attributes_per_level = {
            1: {"Zombie": {"health": 45, "attack": 10},
                "small slime": {"health": 10, "attack": 5},
                "big slime": {"health": 25, "attack": 7}},
            2: {
                "Zombie": {"health": 45, "attack": 10},
                "Skeleton": {"health": 45, "attack": 13},
                "big slime": {"health": 35, "attack": 15}},
            3: { "Zombie": {"health": 45, "attack": 18},
                 "Skeleton": {"health": 60, "attack": 20},
                 "Spectre" : {"health": 110, "attack": 30},
                 "Ogre": {"health": 90, "attack": 25}},
            4: {"Skeleton": {"health": 90, "attack": 20},
                 "Spectre" : {"health": 150, "attack": 30},
                 "Ogre": {"health": 120, "attack": 25},
                 "ghost" : {"health":200, "attack":50}},
            5: {"huge slime" :{"health":200, "attack":20},
                "big slime":{"health":110, "attack":10},
                "big slime":{"health":110, "attack":10},
                "small slime":{"health":45, "attack":5},
                "small slime":{"health":45, "attack":5},
                "small slime":{"health":45, "attack":5},
                "Zombie": {"health": 150, "attack": 35},

            }
        }

        current_level_enemies = []
        for enemy_type, enemy_info in enemy_attributes_per_level[self.current_dungeon_level].items():
            current_level_enemies.append({"type": enemy_type, "health": enemy_info["health"], "attack": enemy_info["attack"]})

        return current_level_enemies
    
    def weapon_attributes(self, enemy):
        weapon_class_mapping = {
            "Inferno Blade": "Brutality",
            "Frostbite Dagger": "Tactical",
            "Venomous Bow": "Survival",
            "Bloodsucker Sword": "Brutality",
            "Thunderstrike Axe": "Tactical",
        # Add more mappings for other weapons
    }

        if self.weapon in weapon_class_mapping:
            weapon_class = weapon_class_mapping[self.weapon]

        if self.player_class == weapon_class:
            # Apply attributes based on the weapon's class
            if self.weapon == "Inferno Blade":
                # Fire Damage attribute
                fire_damage = random.randint(5, 15)
                enemy['health'] -= fire_damage
                print(f"The {self.weapon} inflicts {fire_damage} fire damage over time!")

            elif self.weapon == "Frostbite Dagger":
                # Freezing Effect attribute
                freeze_chance = random.uniform(0, 1)
                if freeze_chance < 0.2:  # 20% chance to freeze
                    enemy['attack'] -= 5
                    print(f"The {self.weapon} freezes the {enemy['type']}, reducing its attack!")

            elif self.weapon == "Venomous Bow":
                # Poisonous Coating attribute
                poison_damage = random.randint(3, 8)
                enemy['health'] -= poison_damage
                print(f"The {self.weapon} poisons the {enemy['type']}, dealing {poison_damage} poison damage!")

            elif self.weapon == "Bloodsucker Sword":
                # Life Steal attribute
                life_steal = random.randint(10, 20)
                self.health += life_steal
                print(f"The {self.weapon} steals {life_steal} health from the {enemy['type']}!")

            elif self.weapon == "Thunderstrike Axe":
                # Critical Strike Chance attribute
                critical_chance = random.uniform(0, 1)
                if critical_chance < 0.3:  # 30% chance for a critical hit
                    critical_damage = random.randint(15, 25)
                    enemy['health'] -= critical_damage
                    print(f"The {self.weapon} lands a critical hit, dealing {critical_damage} bonus damage!")

                else:
                    print(f"The {self.weapon} doesn't have any special attributes for {self.player_class} class.")

            else:
                print(f"You can't use the {self.weapon} with your current class ({self.player_class}).")

        else:
            print(f"The {self.weapon} isn't mapped to any class-specific attributes.")



    def restart_game(self):
        self.__init__(self.name)

    def scroll(self, chosen_weapon):
        if chosen_weapon == "1" :
            self.attack += int(self.attack * 0.15)
            print("You received a brutality scroll! Your attack is increased by 15%.")
        elif chosen_weapon == "2" :
            self.health += int(self.health * 0.15)
            self.attack += int(self.attack * 0.075)
            print("You received a tactical scroll! Your health is increased by 15 and attack are increased by 5%")
        elif chosen_weapon == "3" :
            self.health += 70
            print("You receive a survival scroll! Your health is increased by 70.")

    def choose_weapon_from_options(self, weapon_options):
        print("\nChoose your weapon:")
        for i, weapon in enumerate(weapon_options, start=1):
            print(f"{i}. {weapon}")

        chosen_weapon_index = int(input("Enter the number of your choice: ")) - 1

        if 0 <= chosen_weapon_index < len(weapon_options):
            self.weapon = weapon_options[chosen_weapon_index]
            print(f"You chose the {self.weapon}!")
            self.weapon_attributes()
        else:
            print("Invalid choice. Defaulting to a random weapon.")
            self.weapon = random.choice(weapon_options)

def welcome_message():
    print("Welcome to the Text-Based RPG Game!")

def scroll_print():
    print("\nCongratulations! You found a chest containing a scroll! Choose your reward:")
    print("1. Brutality")
    print("2. Tactical")
    print("3. Survival")

def setup_player():
    player_name = input("Enter your name: ")
    player = Player(player_name)
    player.choose_class()
    return player

def main():
    welcome_message()

    player = setup_player()
    player.display_stats()

    # Game loop
    while player.health > 0:
        input("\nPress Enter to explore the next dungeon level.")

        enemies = player.encounter_enemy()
        print(f"\nYou encounter the following enemies in Dungeon Level {player.current_dungeon_level}:")
        print("=" *40)
        for enemy in enemies:
            print(f"{enemy['type']} - Health: {enemy['health']} | Attack: {enemy['attack']}")
            player.weapon_attributes()  
            player.display_stats()            

        for enemy in enemies:
            while player.health > 0 and enemy['health'] > 0:
                print("=" *40)
                print(f"Current enemy attacking: {enemy['type']}")
                print("Choose your action:")
                print("1. Attack")
                print("2. Heal")
                print("3. Restart Dungeon program")
                print("=" * 40)
               
                action = input("Enter the number of your choice: ")

                if action == "1" or action.lower() == "attack":
                    player_damage = player.attack_enemy()
                    enemy['health'] -= player_damage
                    print(f"\nYou attack the {enemy['type']} and deal {player_damage} damage!")
                    print(f"{enemy['type']}'s remaining health: {enemy['health']}")
                    print("=" * 40)

                elif action == "2" or action.lower() == "heal":
                    player.health += 20
                    print(f"\nYou heal yourself for 20")
                    print(f"Your remaining health is {player.health}")

                elif action == "3" or action.lower() == "restart":
                    print("\nYou restart the dungeon level.")
                    player.restart_game()
                    break

                if enemy['health'] <= 0:
                    print(f"You defeated the {enemy['type']}!")
                    break

                elif action not in ["1", "2", "3", "attack", "heal", "restart"]:
                    print("Invalid choice. Try again.")
                    continue  

                if enemy['health'] <= 0:
                    print(f"You defeated the {enemy['type']}!")
                    break

                enemy_damage = enemy['attack']
                player.health -= enemy_damage
                print("=" * 40)
                print(f"\nThe {enemy['type']} attacks you and deals {enemy_damage} damage!")
                print(f"Your remaining health is {player.health}\n")
                print("=" * 40)

        player.current_dungeon_level += 1

        if player.current_dungeon_level % 4 == 0 or player.current_dungeon_level % 7 == 0 or player.current_dungeon_level % 10 == 0:
            player.upgrade_attributes()
            print(f"\nNow entering dungeon level {player.current_dungeon_level}")

            weapon_options = {
                "Brutality": ["undead sword", "ghost sword", "Mace", "Warhammer", "Halberd"],
                "Tactical": ["Bow", "Crossbow", "Dagger", "Throwing Knives", "Longbow"],
                "Survival": ["Spear", "Club", "Bolas", "Boomerang", "Whip"]
            }

            chosen_weapons = random.sample(weapon_options.get(player.player_class, []), k=3)
            print("Congratulations! You found a chest containing 3 weapons:")
            for i, weapon in enumerate(chosen_weapons, start=1):
                print("=" * 40)
                print(f"{i}. {weapon}")
                print("=" * 40)

            player.choose_weapon_from_options(chosen_weapons)
            player.display_stats()

        elif 2 <= player.current_dungeon_level <= 5:
            player.upgrade_attributes()
            print(f"\nNow entering dungeon level {player.current_dungeon_level}")

            scroll_print()

            chest_choice = input("Enter the number of your choice: ")
            player.scroll(chest_choice)
            player.display_stats()



    print("Game Over! You were defeated.")

if __name__ == "__main__":
    main()

