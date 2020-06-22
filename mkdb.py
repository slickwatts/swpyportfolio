#!/usr/bin/python3.6
# ==================================================
#              Making Shelve Database
#         (Persistent data storage [offline])
#
# Author: Slick
# Date  : 05/19/2020
# ==================================================
import shelve


class Employee:
    def __init__(self, name=None, age=18, pay=10, job='cashier'):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job

    def __str__(self):
        return f'{self.name:>10} (age {self.age}):\t{self.job:<5}\t|  ${self.pay}/hour'

    def surname(self):
        return self.name.split()[-1]

    def giveRaise(self, percent=2):
        self.pay = round(self.pay * ((percent/100) + 1), 2)
        return self.pay


class Manager(Employee):
    def __init__(self, name, age=25, pay=18, job='manager'):
        super().__init__(name, age, pay, job)

    def giveRaise(self, percent=5):
        self.pay = round(self.pay * ((percent/100) + 1), 2)


sally = Manager('Sally Tucker', 30, 18)
tom = Employee('Tom Hayworth', 23, 14, 'stocker')
jerry = Employee('Jerry Smith', 38)
april = Employee('April Domski', 22, 11)

"""
# ====================================Making Shelve Database========================================

# Shelve databases work just like dictionaries...but easier!
# Just with an extra open/close call
db = shelve.open('worker_shelve')
db['sally'] = sally
db['tom']   = tom
db['jerry'] = jerry
db['april'] = april
db.close()

# ======================================Updating Database=============================================

# updating the database is a bit...different. See below.

db = shelve.open('worker_shelve')
Before the update:
# printing all data
for k in db:
    print(db[k])

# getting a specific worker by key
april = db['april']

# using the method to give raise
april.giveRaise()

# saving it back into the database ***IMPORTANT***STEP***
db['april'] = april
db.close()

After update:
print('='*55)
db = shelve.open('worker_shelve')
for k in db:
    print(db[k])
"""

if __name__ == '__main__':
    import shelve
    import time
    import os

    os.chdir(r'/home/slick/textFiles/wkrshlv')
    db = shelve.open('worker_shelve')
    fieldnames = ('name', 'age', 'job', 'pay')
    max_field  = max(len(f) for f in fieldnames)
    deleting   = False
    searching  = False
    updating   = False
    running    = True

    while running:
        try:
            print('\n' + '=' * 40 + '\n' + 'Employees'.center(40, '-'))
            i = 1
            for k in db:
                if i % 5 == 0:
                    print(k, '\n')
                else:
                    print(k, end='   ')
                i += 1
            print('\n\n')
            choice = input('\n\nPress "q" to quit\nDo you want to (s)earch, (u)pdate, or (d)elete from database? > ')
            if choice == 'q' or choice == 'quit':
                print('Exiting...')
                time.sleep(2)
                print('Done.')
                db.close()
                running = False
            elif choice == 'u' or choice == 'update':
                updating = True
                while updating:
                    print('\nEnter "q" to quit\n**MAKE SURE LETTERS ARE IN QUOTES**\n')
                    key = input('Enter a key with NO QUOTES to update or add > ')
                    if not key or key == 'quit' or key == 'q':
                        updating = False
                        break
                    elif key in db:
                        choice = input('Update file?[y/n] > ')
                        if choice == 'y' or choice == 'yes':
                            record = db[key]
                        else:
                            continue
                    else:
                        record = Employee(name='?', age=18)
                    for field in fieldnames:
                        currval = getattr(record, field)
                        new_txt = input(f'\t[{field}] = {currval}\n\t\tNew? > ')
                        if new_txt == 'no' or new_txt == 'n':
                            setattr(record, field, eval(f'db[key].{field}'))
                            continue
                        elif new_txt:
                            setattr(record, field, eval(new_txt))
                    print('\nEntry has been added/updated!\n')
                    db[key] = record
                #db.close()
            elif choice == 's' or choice == 'search' or choice == 'searching':
                searching = True
                while searching:
                    try:
                        key = input('\nEnter "q" to quit\nEnter key to search > ')
                        if not key or key == 'q' or key == 'quit':
                            searching = False
                        elif key in db:
                            print('\n')
                            print(db[key])
                        else:
                            print(f'\nKey: <*{key}*> not found!')
                    except KeyError:
                        print('There was a problem with the key used. Try again.')
            elif choice == 'd' or choice == 'delete':
                deleting = True
                while deleting:
                    key = input('Enter "q" to quit\nEnter key to delete > ')
                    if key == 'q' or key == 'quit':
                        deleting = False
                    elif key in db:
                        warn = input(f'Are you sure you want to delete <*{key}*> [y/n] ? > ')
                        if warn == 'y' or word == 'yes':
                            del db[key]
                            time.sleep(1)
                            print('\nPoof! The file has been deleted.\n')
                        else:
                            print('Try again.')
                    else:
                        print(f'{key} not found!\nCan\'t lose what you don\'t have...Try again.')

            else:
                print('\nNot a valid option.\n\nEnter:\n\ts for search mode\n\tu for update mode\n\td for delete mode')
        except KeyError:
            print('\nSomething went wrong...try again.')