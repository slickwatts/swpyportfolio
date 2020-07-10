#!/usr/bin/python3.6
# ===============================================
#                   Word Tools
#
# Author: Slick
# Date  :
# ===============================================
import string
from pprint import pprint
import time


def load_words_from(filename: str):
    """Displays text from a file"""
    with open(filename) as f:
        text = f.read()
        return text


def save_txt2_newfile(text, filename):
    """Saves text as a new text file"""
    choice = input(f'\nAre you sre you want to make the new file "{filename}"?\n[y/n] > ')
    if choice == 'y' or choice == 'yes':
        with open(filename, 'w') as f:
            f.writelines([line for line in text.split('\n')])
        time.sleep(1)
        print('File saved.')


def save_webpage2_newfile(soupsearch, filename):
    """[IN PROGRESS] Saves a webpage's text to a file"""
    choice = input(f'\nAre you sre you want to make the new file "{filename}"?\n[y/n] > ')
    if choice == 'y' or choice == 'yes':
        with open(filename, 'w') as f:
            f.writelines([line for line in soupsearch])
        time.sleep(1)
        print('File saved.')


def cleantext(text):
    """Removes punctuation and decapitalizes string"""
    subs = text.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\'"@#$%^&*(),”“‘./<->=~—{}[]?|:;`',
                          'abcdefghijklmnopqrstuvwxyz                                           ')
    return text.translate(subs)

def extractwords(text):
    """Prints a sorted table showing all words used in some
       text and the number of occurrences of each."""
    txt = cleantext(text)
    wdls = [w for w in txt.split()]
    # making dictionary of words used
    wddict = {}
    for w in wdls:
        if w in wddict:
            wddict[w] += 1
        else:
            wddict[w] = 1
    # Displaying dictionary data in order
    for ix, (k, v) in enumerate(sorted(wddict.items())):
        if ix % 3 == 0 and ix != 0:
            print(f'{k:<15}|| {v:<5}')
        else:
            print(f'{k:<15}|| {v:<5}', end='\t')
    # End stats
    print('\n')
    print(' Doc Stats '.center(65, '-'))
    print(f'> Total words: {len(wdls)}\n\n> Unique words: {len(wddict)}\n\n> First 5: {wdls[:5]}...\n')
    high = max(wddict.values())
    second = max(sorted(wddict.values())[:-1])
    third = max(sorted(wddict.values())[:-2])
    fourth = max(sorted(wddict.values())[:-3])
    fifth = max(sorted(wddict.values())[:-4])
    for k, v in wddict.items():
        if v == high:
            print(f'> Most frequently used words:\n1. {k:<6}({v:<4} times [{(v/len(wdls))*100:.2f}%])')
    for k, v in wddict.items():
        if v == second:
            print(f'2. {k:<6}({v:<4} times [{(v/len(wdls))*100:.2f}%])')
    for k, v in wddict.items():
        if v == third:
            print(f'3. {k:<6}({v:<4} times [{(v/len(wdls))*100:.2f}%])')
    for k, v in wddict.items():
        if v == fourth:
            print(f'4. {k:<6}({v:<4} times [{(v/len(wdls))*100:.2f}%])')
    for k, v in wddict.items():
        if v == fifth:
            print(f'5. {k:<6}({v:<4} times [{(v/len(wdls))*100:.2f}%])')


def wordcount(text):
    """Returns total number of words in text"""
    return len(cleantext(text).split())


def strip_numbers(wd_ls):
    for w in wd_ls:
        for d in string.digits:
            if d in w:
                wd_ls.remove(w)


def search_linear(text: str, target: str):
    """Returns index of searched characters through text
       Returns -1 if not there"""
    for i, ch in enumerate(text.split()):
        if ch == target:
            return i
    return -1


def search_binary(text: str, target):
    """Returns index of searched characters through SORTED
       text in One string. Returns -1 if not there"""
    start = 0
    end = len(text.split())
    while True:

        if start == end:
            return f'Target: "{target}" found at index[{start}]'

        mid_index = (start + end) // 2
        mid_item = text.split()[mid_index]
        #print(f'ROI[{start}:{end}](size={end-start}), probed="{mid_item}", target="{target}"')

        if mid_item == target:
            return mid_index
        elif mid_item < target:
            start = mid_index+1
        else:
            end = mid_index


def find_unkwn_wds(wd_ls):
    """Returns a list of words that are not in the
       dictionary and gives the option to add them"""
    import os
    os.chdir('/home/slick/textFiles')

    # Read text and display unknown words
    with open('dictionary.txt') as f:
        d_wds = f.readlines()
        dict_wds = [w.strip('\n') for w in d_wds]
    unkwn_wds = []
    for w in wd_ls:
        if w.lower() not in dict_wds:
            unkwn_wds.append(w.lower())

    # Write new words to dictionary file or nah?
    if unkwn_wds:
        print(f'\n"Unknown" words:\n')
        pprint(unkwn_wds)
        add = input('\nAdd all words to dictionary? [y/n] > ')
        if add == 'y' or add == 'yes':
            f = open('dictionary.txt', 'a')
            for w in unkwn_wds:
                if w not in dict_wds:
                    f.write(w + '\n')
            f.close()

            # Artificial work
            print('\nWriting to disk', end='')
            for i in range(4):
                time.sleep(1)
                print('.', end=' ')
            print('Dictionary updated!')
            time.sleep(1)

    # If there are no new words
    else:
        print('\nNo new words found!\n')
