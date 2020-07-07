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
import requests
import re


class NumExtApp:
    def __init__(self):
        # main window
        self.win = Tk()
        self.win.title('')
        self.win.configure(background='black')
        self.win.geometry('375x400')
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
                                 font=('fixedsys', 15), bg='black', fg='white')
        self.title_label.pack(anchor='s', pady=35)

        self.url_label = Label(self.topframe, text='URL:',
                               font=('fixedsys', 12), bg='black', fg='white')
        self.url_label.pack(side=LEFT, anchor='n', padx=10, pady=20)

        self.url_variable = StringVar()
        self.entrybox = Entry(self.topframe, width=28, textvariable=self.url_variable,
                              bd=4, font=('times', 11))
        self.entrybox.pack(side=LEFT, anchor='n', pady=20)
        self.entrybox.focus()

        # add top middle frame-----------------------------------------------------
        self.extr_button = Button(self.midframe, text='Extract', command=self.magic)
        self.clrbutton = Button(self.midframe, text='Clear', command=self.clear, width=7)
        self.extr_button.pack(side=LEFT, pady=15, padx=40)
        self.clrbutton.pack(side=RIGHT, padx=40)

        # add to bottom frame------------------------------------------------------
        self.scrolltxt = scrolledtext.ScrolledText(self.botframe, height=18, width=55,
                                                   font=('times', 18, 'bold'))
        self.scrolltxt.pack()

        #A regex match for phone numbers--------------------------------------------
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
        self.numbers = []  # container for phone numbers
        if self.phoneNumRegex.findall(str(self.webpage)):
            for groups in self.phoneNumRegex.findall(self.webpage):
                phonenum = '-'.join([groups[1], groups[3], groups[5]])
                # print(phonenum)
                if phonenum not in self.numbers:
                    self.numbers.append(phonenum)
                else:
                    continue
            self.numbers.sort()

    def display(self):
        """Displays extracted numbers in scroll text widget"""
        if self.numbers:
            self.scrolltxt.insert(INSERT, f'<<{self.url_variable.get()}>>\n')
            self.entrybox.delete(0, END)
            for num in self.numbers:
                self.scrolltxt.insert(INSERT, num + '\n')
            self.scrolltxt.insert(INSERT, ('='*15) + '\n')
        else:
            messagebox.showerror(message='Sorry! No Luck...')

    def magic(self):
        """The whole sha bang"""
        try:
            self.get_webpage()
            self.extract_()
            self.display()
        except:
            messagebox.showerror('Error', 'Please enter a full valid url')

    def clear(self):
        self.scrolltxt.delete('1.0', END)


app = NumExtApp()
app.win.mainloop()
