import random as r
import time


class Items:
    """Parent class of all items in game"""

    def __init__(self):
        self.weight = None
        self.name = ''
        self.descrpit = ''
        self.value = None


class Weapon(Items):
    """Items that do damage"""

    def __init__(self, value=50, attack=8, name='Steel Straight Sword'):
        super().__init__()
        self.value = value
        self.attack = attack
        self.name = name

    def __hash__(self):
        return hash((self.attack, self.name))

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self == other


class Gold(Items):
    """In game currency"""

    def __init__(self):
        super().__init__()
        self.name = 'Gold'
        self.descript = 'Got the skills to pay the bills?'

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self == other


class Armor(Items):
    """Items that add defense"""

    def __init__(self, name='Leather Armor', defense=5, value=30):
        super().__init__()
        self.name = name
        self.defense = defense
        self.value = value

    def __hash__(self):
        return hash((self.defense, self.name))

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self == other


class Potions(Items):
    """Items that heal and other effects"""
    pass


class Characters:
    """Parent class of characters in game"""

    def __init__(self):
        self.name = ''
        self.health = None
        self.health_max = None
        self.attack = None
        self.defense = None
        self.state = None
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}

    def kills(self, enemy):
        """Attacking enemy. Returns True if enemy is killed"""
        if enemy.health >= .1:
            damage = r.randint(1, round(self.attack)) - (enemy.defense / 2)
            if damage < 0:
                damage = 0
            enemy.health -= damage
            if damage == 0:
                print(f'{enemy.name} evaded the attack!')
            elif enemy.health <= 0:
                print(f'{self.name} finishes {enemy.name}. {enemy.name} is dead!')
                enemy.state = 'dead'
            else:
                print(f'{self.name} attacks!')
        print(f'{self.name} | {self.health}/{self.health_max}\n{enemy.name} | {enemy.health}/{enemy.health_max}')
        return enemy.health <= 0


class Player(Characters):
    """The player character with starter stats"""

    def __init__(self, health=50, health_max=80,
                 state='normal', attack=8, defense=5):
        super().__init__()
        self.health = health
        self.health_max = health_max
        self.state = state
        self.attack = attack
        self.defense = defense

    def quit(self):
        """Quit and exit game"""
        print(f'{self.name} walked into the distance...never to be seen again.')
        self.health = 0

    def help(self):
        """Prints a list of in-game keys"""
        print('Options are:')
        for i, k in enumerate(Commands.keys()):
            if i == len(Commands.keys()) - 1:
                print(k + '.')
            elif i % 3 == 0:
                print(k + ',')
            else:
                print(k, end=', ')

    def show_stats(self):
        """Prints player health, attack, and defense"""
        print(f'\n{self.name}\'s stats: {self.health}/{self.health_max} health')
        print(f'Attack: {self.attack}\nDefense: {self.defense}')

    def get_inventory(self):
        """Prints player inventory"""
        if len(self.inventory) == 0:
            print('My pockets are as empty as my soul...')
        else:
            print('Inventory:')
            for k, v in self.inventory.items():
                print(f'{v:<3} {k.name:<}')

    def get_equipped(self):
        """Prints equipped weapon and armour"""
        print('Equipped:')
        for k, v in self.equipped.items():
            print(f'{k}: {v}')

    def tired(self):
        print(f'{self.name} feels tired.')
        self.health = max(1, self.health - 5)

    def rest(self):
        """Rest to gain hp, may be attacked..."""
        if self.state != 'normal':
            print(f'{self.name} can\'t rest right now!')
            self.enemy_attacks()
        else:
            print(f'{self.name} rests.')
            dice = r.randint(1, 10)
            if dice <= 2:
                self.enemy = Goblin()
                print(f'{self.name} is startled awake!')
                print(f'{self.enemy.name} attacks!')
                self.enemy_attacks()
                self.state = 'fight'
            else:
                print('Slept like a baby...')
                if self.health < self.health_max:
                    print('+15 hp')
                    self.health += 15
                if self.health > self.health_max:
                    print(f'{self.name} slept too much! -10 hp')
                    self.health -= 10

    def flee(self):
        """Run from fights you passafist"""
        if self.state != 'fight':
            print(f'{self.name} tries to flee from nothing...{self.name} is not the brightest torch in the hall.')
            self.tired()
        else:
            if r.randint(1, round(self.health + 5)) > r.randint(1, round(self.enemy.health)):
                print(f'\n{self.name} dipped on {self.enemy.name}!')
                self.enemy = None
                self.state = 'normal'
            else:
                print('\nCouldn\'t escape!')
                self.enemy_attacks()

    def fight(self):
        """After fight messages and boosts...if you win."""
        if self.state != 'fight':
            print(f'{self.name} swats the air, without notable results...')
            self.tired()
        else:
            while self.enemy is not None and self.health > 0:
                # if player kills enemy
                if self.kills(self.enemy):
                    self.enemy = None
                    self.state = 'normal'
                    gold = Gold()
                    if gold in self.inventory.keys():
                        self.inventory[gold] += r.randint(25, 75)
                    else:
                        self.inventory.setdefault(gold, (r.randint(10, 120)))
                    if self.health > self.health_max:
                        self.health = self.health_max
                        self.health_max += 5
                    else:
                        self.health_max += 5
                    if self.health <= self.health_max / 4:
                        print(f'\n{self.name} is victorious! But is also bleeding internally...')
                    if self.health_max / 2 > self.health > self.health_max / 4:
                        print(f'\n{self.name} feels pretty tired after that one!')
                    if self.health_max / 2 < self.health < self.health_max / 1.25:
                        print(f'\n{self.name} feels warmed up now!')
                    if self.health >= self.health_max / 1.25:
                        print(f'\n{self.name} didn\'t even feel a scratch.')
                else:
                    self.enemy_attacks()

    def enemy_attacks(self):
        """Attack from enemy"""
        time.sleep(.5)
        if self.enemy.kills(self):
            print(f"{self.name} was clapped by {self.enemy.name}!!!\n\nR.I.P GAME OVER.")

    def equipw(self):
        """[IN PROGRESS] Equips weapon in inventory"""
        if self.equipped['weapon'] is None:
            for item in self.inventory.keys():
                if isinstance(item, Weapon):
                    self.equipped['weapon'] = item.name
                    self.attack += item.attack
                    print(f'{item.name} equipped!')
            if self.equipped['weapon'] is None:
                print('No weapon equipped')

    def equipa(self):
        """[IN PROGRESS] Equips armor in inventory"""
        if self.equipped['armor'] is None:
            for item in self.inventory.keys():
                if isinstance(item, Armor):
                    self.equipped['armor'] = item.name
                    self.defense += item.defense
                    print(f'{item.name} equipped!')
            if self.equipped['armor'] is None:
                print('No armor equipped')

    def explore(self):
        """The choosy part of the game logic"""
        if self.state != 'normal':
            print(f'{self.name} is too busy right now!')
            self.enemy_attacks()
        else:
            exploring = True
            while exploring:
                if self.health <= 0:
                    break
                try:
                    print('\nWhere do you want to explore?:')
                    area = int(input('[0]exit \n[1]cave \n[2]forest \n[3]city \n> '))
                    if area == 0:
                        exploring = False
                    if area == 1:
                        print(f'\n{self.name} pokes around a dark cave...')
                        spelunking = True
                        message = [f'{self.name} is hearing noises...',
                                   'Into the abyss...',
                                   f'{self.name} isn\'t urinating out of fear right now at all...',
                                   '-...What was that?']
                        while spelunking:
                            dice = r.randint(1, 10)
                            print('\n' + r.choice(message))
                            if dice >= 8:
                                if dice % 2 == 0:
                                    print('Found some Gold!')
                                    gold = Gold()
                                    gold.name = 'Gold'
                                    if gold in self.inventory.keys():
                                        self.inventory[gold] += r.randint(20, 150)
                                    else:
                                        self.inventory.setdefault(gold, r.randint(20, 150))
                                else:
                                    print('Found some armor!')
                                    armor = Armor()
                                    armor.descrpit = 'A light set of armor'
                                    if armor in self.inventory.keys():
                                        self.inventory[armor] += 1
                                    else:
                                        self.inventory.setdefault(armor, 1)
                            else:
                                self.enemy = Goblin()
                                print(f'\n{self.name} found a goblin in the cave!')
                                self.enemy_attacks()
                                self.state = 'fight'
                            if self.state == 'fight':
                                fighting = True
                                while fighting:
                                    fight_or_flee = input('\nStay and fight or flee? > ')
                                    if fight_or_flee == 'fight':
                                        self.fight()
                                        fighting = False
                                    elif fight_or_flee == 'flee':
                                        self.flee()
                                        if self.enemy is not None:
                                            self.fight()
                                            fighting = False
                                        else:
                                            fighting = False
                                    else:
                                        print('Try again.')

                            if self.health <= 0:
                                break
                            choice = input('Go deeper in the cave? [y/n] > ')
                            if choice == 'n':
                                spelunking = False
                    if area == 2:
                        forest_lvl = 1
                        camping = True
                        message = [f'{self.name} frolics through the forest...',
                                   f'{self.name} heads over the medow and through the woods...',
                                   f'{self.name} is stumbling about in the woods...',
                                   f'{self.name} finally feels free in the wilderness...']
                        while camping:
                            dice = r.randint(1, 10)
                            print('\n' + r.choice(message))
                            if forest_lvl % 10 == 0:
                                answer = int(
                                    input('\nA dark fog creeps along the forest floor...\nWill you stick around? '
                                          '\n[1]I ain\'t scared of no fog! \n[2]GET ME OUTTA HERE. \n> '))
                                if answer == 1:
                                    self.enemy = Boss()
                                    print(f'{self.enemy.name} walked menacingly out of the fog.')
                                    self.enemy_attacks()
                                    self.state = 'fight'
                                else:
                                    print('I didn\'t want to know either...')
                                    break
                            elif dice >= 5:
                                print('Had a wonderful time!\n')
                                self.health += r.randint(1, 5)
                            elif dice <= 4:
                                print('Found a goblin in the forest!')
                                self.enemy = Goblin()
                                self.enemy_attacks()
                                self.state = 'fight'
                            if self.state == 'fight':
                                fighting = True
                                while fighting:
                                    fight_or_flee = input('\nStay and fight or flee? > ')
                                    if fight_or_flee == 'fight':
                                        self.fight()
                                        fighting = False
                                    elif fight_or_flee == 'flee':
                                        self.flee()
                                        if self.enemy is not None:
                                            self.fight()
                                            fighting = False
                                        else:
                                            fighting = False
                                    else:
                                        print('Try again.')
                            if self.health <= 0:
                                break
                            choice = input('Go deeper in the forest? [y/n] > ')
                            if choice == 'n':
                                camping = False
                            else:
                                forest_lvl += 1
                    if area == 3:
                        in_town = True
                        print(f'\n{self.name} found a small town...\n')
                        while in_town:
                            dice = r.randint(1, 10)
                            print('Where would you like to go?:')
                            answer = int(
                                input('[0]exit \n[1]Weapon O\'Armor\'s  \n[2]Wasted Widow  \n[3]Smoking Pot \n> '))
                            if answer == 0:
                                break
                            if answer == 1:
                                gold = Gold()
                                shopQ = int(input('Would you like to [1]buy or [2]sell? > '))
                                if shopQ == 1:
                                    if gold in self.inventory.keys():
                                        if self.inventory[gold] >= 150:
                                            print('Bought a sword!')
                                            self.inventory[gold] -= 150
                                            sword = Weapon()
                                            if sword not in self.inventory.keys():
                                                self.inventory.setdefault(sword, 1)
                                            else:
                                                self.inventory[sword] += 1
                                        else:
                                            print('Damn that sword looks, fly. Need mo\' paper though...')
                                if shopQ == 2:
                                    pass
                                    # item = input('What would you like to sell?: ')
                            if answer == 2:
                                if dice <= 9:
                                    gold = Gold()
                                    if self.inventory[gold] < 15:
                                        print(
                                            f'{self.name} was kicked out of the bar for stealing drinks. Need some more gold...')
                                    else:
                                        if 15 <= self.inventory[gold] < 500:
                                            print('Filled up your gut and got some much needed rest.\n-15 Gold')
                                            self.inventory[gold] -= 15
                                            if self.health < self.health_max:
                                                self.health += self.health_max / 4
                                                if self.health > self.health_max:
                                                    self.health = self.health_max
                                        else:
                                            print('Got laid babyyyy!')
                                            self.health_max += r.randint(5, 10)
                                            self.health += self.health_max / 2
                                            if self.health > self.health_max:
                                                self.health = self.health_max
                            if answer == 3:
                                print(
                                    '\nHaven\'t made potions yet...\n-I mean, ye old potions aren\'t hither. *cough* *cough*')
                            choice = input('Stick around town a little longer? [y/n] > ')
                            if choice == 'n':
                                in_town = False
                except ValueError:
                    print('Write a number.')


class Boss(Characters):
    """Extra strong enemy"""

    def __init__(self):
        super().__init__()
        self.name = 'The Big Boss'
        self.health_max = 200
        self.health = r.randint(50, self.health_max)
        self.attack = 20
        self.defense = 8
        self.state = 'fight'


class Goblin(Characters):
    """Enemy Character"""
    name_ls = ['Garwald', 'Griffin', 'Lit Savage', 'Boony', 'Frantros',
               'Harthor', 'Kevin', 'Trempan', 'Grobble', 'Wunsum']

    def __init__(self):
        super().__init__()
        self.name = f'{r.choice(Goblin.name_ls)} the Goblin'
        self.health_max = 50
        self.health = r.randint(10, self.health_max)
        self.attack = 10.5
        self.defense = 3
        self.state = 'fight'


Commands = {
    'quit': Player.quit,
    'help': Player.help,
    'inventory': Player.get_inventory,
    'stats': Player.show_stats,
    'rest': Player.rest,
    'explore': Player.explore,
    'attack': Player.fight,
    'flee': Player.flee,
    'equipw': Player.equipw,
    'equipa': Player.equipa,
    'equipcheck': Player.get_equipped
}

p = Player()
p.name = input('What\'s your hero\'s name?: ')
print('Type "help" to get a list of actions\n')
print(f'{p.name}... You are the chosen one. You are the sexy one. Go on and do... HERO THINGS!')


def replay_start():
    global p
    p = Player()
    p.name = input('What\'s your hero\'s name?: ')
    print('Type "help" to get a list of actions\n')
    print(f'''{p.name}... Now YOU are the chosen one.
You are the sexy one. Go on and do... EVEN MORE HERO THINGS!''')


def game_loop():
    global p
    try:
        print('Would you like to play again? [1]Yes or [2]No > ')
        ans = int(input('> '))
        if ans == 1:
            replay_start()
            main()
        else:
            p.quit()
    except ValueError:
        print('Pick either 1 or 2')
        game_loop()


def main():
    global p
    while p.health > 0:
        line = input('> ')
        args = line.split()
        if len(args) > 0:
            command_found = False
            for c in Commands.keys():
                if args[0] == c[:len(args[0])]:
                    Commands[c](p)
                    command_found = True
                    break
            if not command_found:
                print('Doesn\'t understand the suggestion. If stuck, type "help".')
    game_loop()


main()
# Ideas to add:
# -------------
# potions
# potion shop

# more weapoms & armor(that affects stats)

# multiple enemy fight

# unequip weapons and armor
