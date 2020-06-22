#-------------------------------------------------------------------------------
# Name:        Phone Number Extractor
#
# Author:      Slick
# Created:     13/04/2020
# Copyright:   (c) Slick 2020
#-------------------------------------------------------------------------------
import requests, os, re
def main():
    def getPhoneNumbers(text):
        '''Goes through text and extracts phone numbers'''
        phoneNumRegex = re.compile(r'''(
            (\d{3}|\(\d{3}\))
            (\s|-|\.)?
            (\d{3})
            (\s|-|\.)
            (\d{4})
            )''', re.VERBOSE)

        numbers = []
        if phoneNumRegex.findall(str(text)) != []:
            for groups in phoneNumRegex.findall(text):
                phonenum = '-'.join([groups[1],groups[3],groups[5]])
                #print(phonenum)
                if phonenum not in numbers:
                    numbers.append(phonenum)
                else:
                    continue
            numbers.sort()
            print(f'\nNumbers Found: {len(numbers)}')
            print('\n        Scammer Numbers')
            print('_'*32)
            try:
                for num in range(0,len(numbers),2):
                    print(f'{numbers[num]:>14} | {numbers[num+1]:>14} |')
                print('-'*32,'\nHave fun... :)')
            except IndexError:
                print(f'{numbers[num]:>14} |                |')
                print('-'*32,'\nHave fun... :)')
                ans = input('\nNICE, want to do another?[y/n] > ')
                if ans == 'y':
                    webpage = requests.get((input('Search URL > ')))
                    getPhoneNumbers(webpage.text)
                else:
                    print('\nCool, no worries.')
        else:
            ans = input('\nNo matches...try another?[y/n] > ')
            if ans == 'y':
                webpage = requests.get((input('Search URL > ')))
                getPhoneNumbers(webpage.text)
            else:
                print('Good luck out there')


    webpage = requests.get((input('Search URL > ')))
    #getPhoneNumbers(webpage.content.decode('utf-8'))
    getPhoneNumbers(webpage.text)
    #print(webpage.content)
    #getPhoneNumbers(webpage)
    #webpage = ''' '''
main()