#!/usr/bin/python3.6
# ===========================================
#            Caesar Cipher Class
#
#    Turn your text into Cipher objects!
#     Each instance can be encrypted or
#      decrypted with the Caesar Cipher
#          with using 2 parameters.
#
#    - cipher index:
#        the number of letters to displace
#        text by
#
#    - reverse:
#        a boolean value determines if
#        the cipher translates to letters
#        going in regular or reverse
#        order.
#
# Author: Slick
# Date  : 7/10/2020
# ===========================================
import string


class CaesarCipher:
    def __init__(self, text=None):
        self.text = self.clean_text(text)
        self.lett2num_dict = {lett: index for index, lett in enumerate(string.ascii_lowercase)}
        self.num2lett_dict = {index: lett for index, lett in enumerate(string.ascii_lowercase)}
        self.lett2num_dict[' '] = ' '
        self.num2lett_dict[' '] = ' '

    def __str__(self):
        return self.text

    @staticmethod
    def increment(num, to_add):
        """Increases numbers in the range of 0-25"""
        num = num
        for i in range(to_add):
            num += 1
            if num == 26:
                num = 0
        return num

    @staticmethod
    def decrement(num, to_sub):
        """Decreases numbers in the range of 0-25"""
        num = num
        for i in range(to_sub):
            num -= 1
            if num == -1:
                num = 25
        return num

    @staticmethod
    def clean_text(text):
        """Removes punctuation and decapitalizes string"""
        subs = text.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\'"@#$%^&*(),”“‘./<->=~—{}[]?|:;`',
                              'abcdefghijklmnopqrstuvwxyz                                           ')
        return text.translate(subs)

    def encrypt(self, cipher_index=0, reverse=False):
        if not reverse:
            num_message = [self.increment(self.lett2num_dict[lett], cipher_index) if lett != ' ' else ' ' for lett in
                           self.text]
            encrypt_text = ''.join([self.num2lett_dict[num] if num != ' ' else ' ' for num in num_message])
            return CaesarCipher(encrypt_text)
        else:
            num_message = [self.decrement(self.lett2num_dict[lett], cipher_index) if lett != ' ' else ' ' for lett
                           in self.text]
            encrypt_text = ''.join([self.num2lett_dict[num] if num != ' ' else ' ' for num in num_message])
            return CaesarCipher(encrypt_text)

    def decrypt(self, cipher_index=0, reverse=False):
        if not reverse:
            num_message = [self.decrement(self.lett2num_dict[lett], cipher_index) if lett != ' ' else ' ' for lett in
                           self.text]
            decrypt_text = ''.join([self.num2lett_dict[num] if num != ' ' else ' ' for num in num_message])
            return CaesarCipher(decrypt_text)
        else:
            num_message = [self.increment(self.lett2num_dict[lett], cipher_index) if lett != ' ' else ' ' for lett
                           in self.text]
            decrypt_text = ''.join([self.num2lett_dict[num] if num != ' ' else ' ' for num in num_message])
            return CaesarCipher(decrypt_text)


if __name__ == '__main__':
    # message
    text = 'Super Secret message alert!Get to the choppah'
    message = CaesarCipher(text)
    print('Original message:\n', message, '\n')

    # encrypted message
    secret = message.encrypt(15, True)
    print('Encrypted text:\n', secret, '\n')

    # decrypted message
    not_secret = secret.decrypt(15, True)
    print('Decrypted text:\n', not_secret, '\n')