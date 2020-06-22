class Hangman:
	def __init__(self):
		import random as r
		self.words = ['take','sharp','cake','pumpkin','candy',
    						'purple','apple','coding','cheese','floppy',
    						'network','directory','byte','whisper']	
		self.word = r.choice(self.words)
		self.hidden_word = ['_' for letter in self.word]
		self.tries = len(self.word) + 5
		self.guess_right = 0
		self.game_won = False
	def a(self):
		print('	o') 
	def b(self):
		print('	o')
		print('	|') 
	def c(self):
		print('	o')
		print('	|')
		print('	|')		  		
	def d(self):
		print('	o')
		print('	|')
		print('	|\\')
	def e(self): 
		print('       \o')	  
		print('	|')  		
		print('	|\\')  
	def f(self):
		print('       \o')
		print('	|7')
		print('	|\\')
	def g(self):
		print('       \oj')
		print('	|7')
		print('	|\\')	
	def greet(self):
		return 'Let\'s play Hangman!'.center(45,'-') + '\n\nHere is your word:'		
	def replace_(self, index, found_letter):
			del self.hidden_word[index]
			self.hidden_word.insert(index, found_letter)	
	def guess(self):
		guess = input('\nGuess a letter or the word > ')
		if len(guess) == 1:
			if guess in self.word:
				index = 0
				right = 0
				print('It\'s here!')
				for lett in self.word:
					if lett == guess:
						self.replace_(index, guess)
						if lett not in self.hidden_word:
							self.guess_right += 1
					index += 1
			else:
				print('No luck...')
		elif guess == self.word:
			print('Nice, you win!')
			self.game_won = True							
		self.tries -= 1
		print(self.hidden_word, f'\n\nTries left: {self.tries}')
		if self.tries == 7: self.a()
		elif self.tries == 6: self.b()
		elif self.tries == 5: self.c()
		elif self.tries == 4: self.d()
		elif self.tries == 3: self.e()
		elif self.tries == 2: self.f()
		elif self.tries == 1: self.g()
			
def main():
	import time
	game = Hangman()
	print(game.greet())
	print(game.hidden_word)
	while not game.game_won and game.tries >= 1:
		game.guess()
	if game.tries == 0 and game.guess_right < len(game.word) and game.game_won == False and '_' in game.hidden_word:
		message = ['\nYou LOSE!','The word...',f'Was {game.word}!']
		for w in message:
			print(w)
			time.sleep(1)
	else:
		message = ['\nYou win!','The word...',f'Was {game.word}!']
		for w in message:
			print(w)
			time.sleep(1)
	choice = input('Play again? [y/n] > ')
	if choice == 'y':
		main()
	else:
		print('Bye!')
					
main()