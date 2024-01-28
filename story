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

