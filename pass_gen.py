#!/usr/bin/python3.6
# ===============================================
#              Password Generator
#
# Author: Slick
# Date  :
# ===============================================
import random as r
import string
import re
import time


def generate():
    passlen = 0
    while passlen < 8:
        passlen = int(input('Enter desired length of password > '))
        if passlen < 8:
            print('Password needs to be longer than 7 characters!')
    lspass = []
    for i in range(passlen):
        lspass.append(r.choice(string.hexdigits) or r.choice(string.ascii_letters))
    return ''.join(lspass)


def passChecker(password):
    lencheckRegex = re.compile(r'''(
        [a-zA-Z0-9!_]{8,}
        )''',re.VERBOSE)
    uppercheckRegex = re.compile(r'''(
        [A-Z]+
        )''',re.VERBOSE)
    lowercheckRegex = re.compile(r'''(
        [a-z]+
        )''',re.VERBOSE)
    numcheckRegex = re.compile(r'''(
        [0-9]+
        )''',re.VERBOSE)
    if lencheckRegex.findall(password) == []:
        return False
    elif uppercheckRegex.findall(password) == []:
        return False
    elif lowercheckRegex.findall(password) == []:
        return False
    elif numcheckRegex.findall(password) == []:
        return False
    else:
        return True

def createpass():
    pass_ = generate()
    if passChecker(pass_) == True:
        print('New password:', pass_)
    else:
        print('Generated password weak...trying again')
        time.sleep(2)
        createpass()
    choice = input('\nDifferent password [y/n] ? > ')
    if choice == 'y' or choice == 'yes':
        createpass()
    else:
        print('Remember to keep it safe!')


if __name__ == '__main__':

    createpass()


