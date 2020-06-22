#-------------------------------------------------------------------------------
# Name:        MapIt
#
# Author:      Slick
# Created:     20/04/2020
#-------------------------------------------------------------------------------
'''Takes an address and shows it to you on google maps'''
import os, webbrowser, pyperclip

print(' '*25+'Where would you like to see?')
address = input('Look for address or place > ').split()
websearch = '+'.join(address)


def main():
    location = input('Is this an [1]address or a [2]place? > ')
    if location == '1':
        webbrowser.open(f'https://www.google.com/maps/place/{websearch}')
    if location == '2':
        webbrowser.open(f'https://www.google.com/maps/search/{websearch}')
    else:
        print('Enter 1 or 2 to choose.')
        main()

main()


