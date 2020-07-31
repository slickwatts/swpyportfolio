# ============================================
#           Scammer Info Indexer GUI
#
# Author: Slick
# Date  : 6/26/2020
# ===============================================
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.ttk import Notebook
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
        self.file_path = '/home/slick/textFiles/scammer_info.csv'
        self.add_widgets()
        self.load_text()

    def add_widgets(self):
        # create tabs -------------------------------------------------------
        self.tabcontrol = Notebook(self.win)
        self.tab1 = Frame(self.win, bg='black')
        self.tab2 = LabelFrame(self.win, text='Collected Data', bg='black', fg='white')
        self.tabcontrol.add(self.tab1, text='Extract')
        self.tabcontrol.add(self.tab2, text='View')
        self.tabcontrol.pack(expand=1, fill=BOTH)
        # create frames-----------------------------------------------------
        self.topframe = Frame(self.tab1, background='black')
        self.midframe = Frame(self.tab1, background='black')
        self.botframe = Frame(self.tab1, background='black')
        # pack frames
        self.topframe.pack(expand=1, fill=BOTH, padx=5, pady=2)
        self.midframe.pack(expand=1, fill=BOTH, padx=5)
        self.botframe.pack(expand=1, fill=BOTH)

        # add to top frame---------------------------------------------------
        self.title_label = Label(self.topframe, text='Scammer Info Indexer',
                                 font=('fixedsys', 20), bg='black', fg='white')
        self.title_label.pack(anchor='s', pady=28)

        self.url_label = Label(self.topframe, text='URL:',
                               font=('fixedsys', 12), bg='black', fg='white')
        self.url_label.pack(side=LEFT, anchor='n', padx=10, pady=15)

        self.url_variable = StringVar()
        self.entrybox = Entry(self.topframe, width=40, textvariable=self.url_variable,
                              bd=4, font=('times', 11))
        self.entrybox.pack(side=LEFT, anchor='n', pady=15)
        self.entrybox.insert(0, 'techscammersunited.com')

        # add top middle frame-----------------------------------------------------
        self.extr_button = Button(self.midframe, text='Extract', command=self.magic)
        self.clrbutton = Button(self.midframe, text='Clear', command=self.clear,
                                width=7)
        self.extr_button.pack(side=LEFT, pady=15, padx=40)
        self.clrbutton.pack(side=RIGHT, padx=40)

        # add to bottom frame-----------------------------------------------------
        self.scrolltxt = scrolledtext.ScrolledText(self.botframe, height=25,
                                                   width=75,
                                                   font=('courier', 12, 'bold'))
        self.scrolltxt.pack()

        # add to view tab
        self.scrolltxt2 = scrolledtext.ScrolledText(self.tab2, height=18,
                                                   width=75,
                                                   font=('courier', 10, 'bold'))

        self.scrolltxt2.pack(expand=1, fill=BOTH)

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
        if os.path.exists(self.file_path):
            # make a csv reader and writer
            with open(self.file_path) as csv_file_text:
                csv_reader = csv.reader(csv_file_text, delimiter='\t')
                with open(self.file_path, 'a') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter='\t')
                    # making a list of all numbers ALREADY collected
                    file_nums = [row[1] for row in csv_reader if row]
                    # if the phone number isn't already there, add it
                    for row in self.data:
                        type_, num, date = row
                        if ('SCAM' in type_ or 'OTHER' in type_) and \
                            'TOOL' not in type_ and num and \
                            'DEAD' not in type_ and row[1] not in file_nums:
                            csv_writer.writerow(row)
        # if no database file, will create one
        else:
            os.makedirs('/home/slick/textFiles/scammer_info.csv')
            # create a csv writer
            with open(self.file_path, 'a') as csv_file:
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
            self.scrolltxt.insert(INSERT, ('-' * 63) + '\n')
            self.scrolltxt.insert(INSERT, f'{title1:^20}| {title2:^19}| {title3:^18}' + '\n')
            self.scrolltxt.insert(INSERT, ('-' * 63) + '\n')
            for type_, num, date in self.data:
                if num:
                    self.scrolltxt.insert(INSERT, f'{type_:20}| {num:^19}| {date:^18}' + '\n')
                    self.scrolltxt.insert(INSERT, ('-' * 63) + '\n')
            self.scrolltxt.insert(INSERT, f'\n<<{self.url_variable.get()}>>\n')
            self.entrybox.delete(0, END)
            self.load_text()
        else:
            messagebox.showerror(message='Sorry! No Luck...')

    def load_text(self):
        self.scrolltxt2.delete('1.0', END)
        with open(self.file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            seperator = '-'*58
            for row in csv_reader:
                if row:
                    self.scrolltxt2.insert(INSERT, f'{row[0]:20}| {row[1]:^18}| {row[2]:^15}|\n{seperator}\n')

    def magic(self):
        """The whole sha bang"""
        try:
            self.get_webpage()
            self.extract_()
            self.save2file()
            self.display()
        except:
            messagebox.showerror('Error', 'Please enter a full valid url')

    def clear(self):
        self.scrolltxt.delete('1.0', END)


app = NumExtApp()
app.win.mainloop()

