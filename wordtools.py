#!/usr/bin/python3.6
# ===============================================
#                   Word Tools
#
# Author: Slick
# Date  :
# ===============================================
import requests
import time
import os
from bs4 import BeautifulSoup


def load_words_from(filename: str):
    """Returns text from a file"""
    with open(filename) as f:
        text = f.read()
        return text


def save_txt2_newfile(text, filename):
    """Saves text as a new text file"""
    if os.path.exists(filename):
        choice = input(f"File already exists, overwrite {filename}?\n[y/n] > ")
        if choice == 'y' or choice == 'yes':
            with open(filename, 'w') as f:
                f.writelines([line for line in text.split('\n')])
                time.sleep(1)
                print('File saved.')
    else:
        choice = input(f'\nAre you sre you want to make the new file "{filename}"?\n[y/n] > ')
        if choice == 'y' or choice == 'yes':
            with open(filename, 'w') as f:
                f.writelines([line for line in text.split('\n')])
            time.sleep(1)
            print('File saved.')


def get_text_from_webpage(url):
    """Returns a webpage's text"""
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser').get_text()
    return soup


def cleantext(text, whitelist=[" "]):
    """Removes all punctuation (by default) and decapitalizes string
       param: pass_chars - list of numbers or punctuation to whitelist from cleaning"""
    washed = ''.join([lett.lower() for lett in text if lett.isalpha() or lett.isspace() or lett in whitelist])
    return washed


def get_dict_of_words(text):
    """Returns a dictionary containing all words and number of occurrences"""
    txt = cleantext(text, ["\n"])
    wdls = [w for w in txt.split()]
    # making dictionary of words used
    wddict = {}
    for w in wdls:
        if w in wddict:
            wddict[w] += 1
        else:
            wddict[w] = 1

    return wddict


def get_ls_of_words(text):
    wd_dict = get_dict_of_words(text)
    return list(wd_dict.keys())


def display_wd_dict(word_dictionary):
    """Displays a table showing all words and occurences plust extra stats"""
    # Displaying dictionary data in order
    wdls = list(word_dictionary.keys())
    for i, (k, v) in enumerate(sorted(word_dictionary.items())):
        if i % 3 == 0 and i:
            print(f'{k:<15}|| {v:<5}')
        else:
            print(f'{k:<15}|| {v:<5}', end='\t')
    # End stats
    print('\n')
    print(' Doc Stats '.center(65, '-'))
    print(f'> Total words: {sum(list(word_dictionary.values()))}\n\n> Unique words: {len(list(set(wdls)))}\n\n> First 5: {wdls[:5]}...\n')
    print("> Most frequently used words:")
    high   = max(list(set(list(word_dictionary.values()))))
    second = max(list(set(list(word_dictionary.values())))[:-1])
    third  = max(list(set(list(word_dictionary.values())))[:-2])
    fourth = max(list(set(list(word_dictionary.values())))[:-3])
    fifth  = max(list(set(list(word_dictionary.values())))[:-4])

    for k, v in word_dictionary.items():
        if v == high:
            print(f'1. {k:<10}({v:<3} times' +
                  f'[{(v / len(wdls)) * 100:.2f}%])'.rjust(10, ' '))
    for k, v in word_dictionary.items():
        if v == second:
            print(f'2. {k:<10}({v:<3} times' +
                  f'[{(v / len(wdls)) * 100:.2f}%])'.rjust(10, ' '))
    for k, v in word_dictionary.items():
        if v == third:
            print(f'3. {k:<10}({v:<3} times' +
                  f'[{(v / len(wdls)) * 100:.2f}%])'.rjust(10, ' '))
    for k, v in word_dictionary.items():
        if v == fourth:
            print(f'4. {k:<10}({v:<3} times' +
                  f'[{(v / len(wdls)) * 100:.2f}%])'.rjust(10, ' '))
    for k, v in word_dictionary.items():
        if v == fifth:
            print(f'5. {k:<10}({v:<3} times' +
                  f'[{(v / len(wdls)) * 100:.2f}%])'.rjust(10, ' '))


def wordcount(text):
    """Returns total number of words in text"""
    return len(cleantext(text, ["'"]).split())


def strip_numbers(text):
    """Takes numbers out of text"""
    wd_ls = get_ls_of_words(text)
    for w in wd_ls:
        for lett in w:
            if lett.isdigit():
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
        #print(f'ROI[{start}:{end}](size={end-start}),
        # probed="{mid_item}", target="{target}"')

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

    # Read text and extract unknown words
    with open('wd_dict.txt') as f:
        d_wds = f.readlines()
        dict_wds = [w.strip('\n') for w in d_wds]
    unkwn_wds = [w for w in wd_ls if w.lower() not in dict_wds]

    # Write new words to dictionary file or nah?
    if unkwn_wds:
        print(f'\n{len(unkwn_wds)} unknown words found!\n"Unknown" words:\n')
        for w in unkwn_wds:
            print(w)

        print('\nAdd all, some, or none of the words to dictionary?')
        choice = input("[1] All\n[2] Some\n[3] None\n> ").lower()

        if choice == '1' or choice == 'all':
            with open('dictionary.txt', 'a') as f:
                for w in unkwn_wds:
                    if w not in dict_wds:
                        f.write(w.lower() + '\n')

            # Artificial work
            print('\nWriting to disk', end='')
            for i in range(4):
                time.sleep(1)
                print('.', end=' ')
            print('Dictionary updated!')
            time.sleep(1)

        elif choice == '2' or choice == 'some':
            chosen = []
            # loop through and pick the ones you want to keep
            for w in unkwn_wds:
                choice = input(f'Keep "{w}"? [y/n] > ').lower()
                if choice == 'y':
                    chosen.append(w)
            print("\nFinished! Adding words...")
            with open('wd_dict.txt', 'a') as f:
                for w in chosen:
                    if w not in dict_wds:
                        f.write(w.lower() + '\n')
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
