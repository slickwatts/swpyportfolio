#!/usr/bin/python3.6
# ===============================================
#           Phone Number Extractor GUI
#
# Author: Slick
# Date  : 6/26/2020
# ===============================================
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import numpy as np
import datetime
import requests
import bs4
import csv
import re
import os


class NumExtApp:
    def __init__(self):
        # main window
        self.win = Tk()
        self.win.title('')
        self.win.configure(background='black')
        self.win.geometry('525x500')
        self.win.resizable(False, False)
        # the goods
        self.add_widgets()

    def add_widgets(self):
        # create frames-----------------------------------------------------
        self.topframe = Frame(self.win, background='black')
        self.midframe = Frame(self.win, background='black')
        self.botframe = Frame(self.win, background='black')
        # pack frames
        self.topframe.pack(expand=1, fill=BOTH, padx=5, pady=2)
        self.midframe.pack(expand=1, fill=BOTH, padx=5)
        self.botframe.pack(expand=1, fill=BOTH)

        # add to top frame---------------------------------------------------
        self.title_label = Label(self.topframe, text='# Extractor 3000',
                                 font=('fixedsys', 20), bg='black', fg='white')
        self.title_label.pack(anchor='s', pady=35)

        self.url_label = Label(self.topframe, text='URL:',
                               font=('fixedsys', 12), bg='black', fg='white')
        self.url_label.pack(side=LEFT, anchor='n', padx=10, pady=20)

        self.url_variable = StringVar()
        self.entrybox = Entry(self.topframe, width=43, textvariable=self.url_variable,
                              bd=4, font=('times', 11))
        self.entrybox.pack(side=LEFT, anchor='n', pady=20)
        self.entrybox.focus()

        # add top middle frame-----------------------------------------------------
        self.extr_button = Button(self.midframe, text='Extract', command=self.magic)
        self.clrbutton = Button(self.midframe, text='Clear', command=self.clear,
                                width=7)
        self.extr_button.pack(side=LEFT, pady=15, padx=40)
        self.clrbutton.pack(side=RIGHT, padx=40)

        # add to bottom frame-----------------------------------------------------
        self.scrolltxt = scrolledtext.ScrolledText(self.botframe, height=18,
                                                   width=75,
                                                   font=('arial', 12, 'bold'))
        self.scrolltxt.pack()

        #A regex match for phone numbers------------------------------------------
        self.phoneNumRegex = re.compile(r'''(
            (\d{3}|\(\d{3}\))
            (\s|-|\.)?
            (\d{3})
            (\s|-|\.)
            (\d{4})
            )''', re.VERBOSE)

    def get_webpage(self):
        """Grabs a webpage's HTML and saves it as text"""
        if 'https:' in self.url_variable.get().split('/'):
            self.webpage = requests.get(self.url_variable.get()).text
        else:
            self.webpage = requests.get('https://' + self.url_variable.get()).text

    def extract_(self):
        """Extracts phone numbers from saved webpage and
           saves them in a list"""
        # creating Beautiful soup object
        self.scammer_soup = bs4.BeautifulSoup(self.webpage, features="html.parser")
        # selecting info from page
        self.urls_and_nums = self.scammer_soup.select('div span a')
        self.scammer_types = self.scammer_soup.select('div span span')
        # making container to hold data
        self.data_list = []
        # displaying scam heading info
        for i in range(len(self.urls_and_nums) - 3):
            for data in self.urls_and_nums[i + 3]:
                self.data_list.append(data)
        # making container to hold scam types
        self.type_list = []
        for i in range(len(self.scammer_types) - 3):
            for data in self.scammer_types[i + 3]:
                self.type_list.append(data)
        # making container to hold numbers
        self.scammer_numbers = []
        for line in self.data_list:
            if self.phoneNumRegex.search(line):
                self.scammer_numbers.append(self.phoneNumRegex.search(line).group())
            else:
                self.scammer_numbers.append(None)

        self.scam_types = []
        for line in self.type_list:
            if line:
                self.scam_types.append(str(line.upper()))
            else:
                self.scam_types.append(None)

        # making arrays out of separated data
        self.scams = np.array(self.scam_types).reshape(len(self.scam_types), 1)
        self.nums = np.array(self.scammer_numbers[:-1]).reshape(len(self.scammer_numbers) - 1, 1)
        self.dates = np.array([str(datetime.date.today()) for x in self.nums]).reshape(len(self.scam_types), 1)

        # taking all data and matching attributes together (scam_type, phone_num,
        # and date)
        self.data = np.hstack([self.scams, self.nums, self.dates])

    def save2file(self):
        """Saves extracted data to .csv file"""
        if os.path.exists('/home/slick/textFiles/scammer_info.csv'):
            # make a csv reader and writer
            with open('/home/slick/textFiles/scammer_info.csv') as csv_file_text:
                csv_reader = csv.reader(csv_file_text, delimiter='\t')
                with open('/home/slick/textFiles/scammer_info.csv', 'a') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter='\t')
                    # making a list of all numbers ALREADY collected
                    file_nums = [row[1] for row in csv_reader]
                    # if the phone number isn't already there, add it
                    for row in self.data:
                        type_, num, date = row
                        if 'SCAM' in type_ and 'TOOL' not in type_ and num and \
                                num not in file_nums:
                            csv_writer.writerow(row)
        # if no database file, will create one
        else:
            # create a csv writer
            with open('/home/slick/textFiles/scammer_info.csv', 'a') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter='\t')
                # add categories
                csv_writer.writerow(['Scam Type', 'Phone Number', 'Date'])
                # add all collected data
                for row in self.data:
                    type_2, num2, date2 = row
                    if 'SCAM' in type_2 and 'TOOL' not in type_2 and num2:
                        csv_writer.writerow(row)

    def display(self):
        """Displays extracted numbers in scroll text widget"""
        if len(self.data) > 0:
            self.scrolltxt.insert(INSERT, f'<<{self.url_variable.get()}>>\n\n')
            title1, title2, title3 = ['Type', 'Phone Number', 'Date']
            self.scrolltxt.insert(INSERT, ('-' * 50) + '\n')
            self.scrolltxt.insert(INSERT, f'{title1:^21}| {title2:^15}| {title3:^8}' + '\n')
            self.scrolltxt.insert(INSERT, ('-' * 50) + '\n')
            for type_, num, date in self.data:
                if num:
                    self.scrolltxt.insert(INSERT, f'{type_:<21}| {num:15}| {date:8}' + '\n')
                    self.scrolltxt.insert(INSERT, ('-'*50) + '\n')
            self.scrolltxt.insert(INSERT, f'\n<<{self.url_variable.get()}>>\n')
            self.entrybox.delete(0, END)
        else:
            messagebox.showerror(message='Sorry! No Luck...')

    def magic(self):
        """The whole sha bang"""
        #try:
        self.get_webpage()
        self.extract_()
        self.save2file()
        self.display()
        #except:
        #    messagebox.showerror('Error', 'Please enter a full valid url')

    def clear(self):
        self.scrolltxt.delete('1.0', END)


app = NumExtApp()
app.win.mainloop()
