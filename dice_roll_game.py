#!/usr/bin/python3.6
# ===============================================
#                 Dice Roll Game
#
# Author: Slick
# Date  :
# ===============================================
import random

rolls = {}


def play():
    try:
        global rolls
        playing = True
        players = int(input('How many players? > '))
        while playing:
            for i in range(1, players+1):
                print(f'\nPlayer {i} your turn! Roll them dice (press enter)')
                input()
                roll = random.randint(1, 6)
                rolls[f'Player {i}'] = roll
                print(f'Player {i}, you rolled a', str(roll) + '!')
            for k, v in rolls.items():
                if rolls[k] == max(rolls.values()):
                    print(f'\n{k} wins with a {v}!')
            choice = input('Play again? (yes/no) > ')
            if choice == 'y' or choice == 'yes':
                play()
            else:
                print('Bye!')
                playing = False
    except ValueError:
        print('Only enter numbers! Try again')
        play()


if __name__ == '__main__':
    play()
