#!/usr/bin/python3.6
# ===========================================================
#          Caesar Cipher Encryption GUI
#
#   Instructions:
#       Encryption -------------------------------------
#       - type text to be encrypted in left text box
#       - set offset (0 offset will have no effect)
#       - if reverse is checked, negative offset will be used
#       - hit 'Encrypt' and encrypted text will appear
#
#       Decryption -------------------------------------
#       - paste encrypted text in the left text box
#       - get offset and reverse info from sender
#       - enter offset and reverse info if applicable
#       - hit 'Decrypt' and decrypted text will appear
#
#
# Author: Slick
# Date  : 7/10/2020
# ===========================================================
from tkinter import *
from tkinter import scrolledtext
from ceasar_cipher import CaesarCipher


class EncryptionApp:
    def __init__(self):
        self.win = Tk()
        self.win.title('Caesar Cipher Text Encryption')
        self.win.geometry('725x500')
        self.win.resizable(False, False)
        self.add_widgets()

    def add_widgets(self):
        # adding frames
        self.topframe = Frame(self.win)
        self.botframe = LabelFrame(self.win, text='Options')
        self.lintopframe = LabelFrame(self.topframe, text='Before')
        self.rintopframe = LabelFrame(self.topframe, text='After')

        self.topframe.pack(expand=1, fill=BOTH)
        self.botframe.pack(expand=1, fill=BOTH)
        self.lintopframe.pack(side=LEFT, expand=1, fill=BOTH)
        self.rintopframe.pack(side=RIGHT, expand=1, fill=BOTH)

        # text boxes
        self.before_text = scrolledtext.ScrolledText(self.lintopframe, height=17, width=28,
                                                     font=('arial', 14), wrap=WORD)
        self.after_text = scrolledtext.ScrolledText(self.rintopframe, height=17, width=28,
                                                    font=('arial', 14), wrap=WORD)
        self.before_text.pack(expand=1, fill=BOTH)
        self.after_text.pack(expand=1, fill=BOTH)

        # options frame
        self.b1 = Button(self.botframe, text='Encrypt', font=('arial', 10), command=self.encrypt)
        self.b2 = Button(self.botframe, text='Decrypt', font=('arial', 10), command=self.decrypt)
        self.b3 = Button(self.botframe, text='Clear', font=('arial', 10), command=self.clear)
        self.reversed_var = BooleanVar()
        self.check_box = Checkbutton(self.botframe, text='Reversed', font=('arial', 11), variable=self.reversed_var)
        self.offset_label = Label(self.botframe, text='Offset', font=('arial', 11))
        self.cipher_index = IntVar()
        self.offset_spin = Spinbox(self.botframe, values=list(range(26)), width=3, font=('arial', 12), textvariable=self.cipher_index)

        self.b1.pack(side=LEFT, padx=20)
        self.b2.pack(side=LEFT, padx=20)
        self.b3.pack(side=LEFT, padx=20)
        self.check_box.pack(side=LEFT, padx=60)
        self.offset_label.pack(side=LEFT, anchor='w')
        self.offset_spin.pack(side=LEFT, anchor='w')

    def encrypt(self):
        self.after_text.delete('1.0', END)
        before_text = CaesarCipher(self.before_text.get('1.0', END))
        after_text = before_text.encrypt(self.cipher_index.get(), self.reversed_var.get())
        self.after_text.insert(INSERT, after_text)

    def decrypt(self):
        self.after_text.delete('1.0', END)
        before_text = CaesarCipher(self.before_text.get('1.0', END))
        after_text = before_text.decrypt(self.cipher_index.get(), self.reversed_var.get())
        self.after_text.insert(INSERT, after_text)

    def clear(self):
        self.after_text.delete('1.0', END)
        self.before_text.delete('1.0', END)


app = EncryptionApp()
app.win.mainloop()
