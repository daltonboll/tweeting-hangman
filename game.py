class Game:

	def __init__(self, computer_player, user_player):
		self.computer_player = computer_player
		self.user_player = user_player

	def play(self):
		self.word = self.find_word()
		self.blank_word = self.get_blank_word(self.word)

		while self.blank_word != self.word:
			self.letter = input("Guess a letter:\n")
			changed_tuple = self.replace_letters(self.letter, self.word, self.blank_word)
			changed = changed_tuple[0]
			if changed:
				count = changed_tuple[1]
				print("\nCongratulations! The letter '{}'' occured {} times.".format(self.letter, count))
				print("The mystery word is now: {}\n".format(self.blank_word))
			else:
				print("\nSorry! The letter '{}'' does not appear in the mystery word. Please try again.".format(self.letter))

		print("Woohoo! You guessed the word! It was '{}'. Thanks for playing!".format(self.word))
		self.end_game()


	def end_game(self):
		print("Game ended.")

	def find_evil_word(self):
		pass

	def find_word(self):
		return "happiness"

	def get_blank_word(self, word):
		blank_word = ""
		for i in range(0, len(word)):
			blank_word = blank_word + "_"
		return blank_word

	def replace_letters(self, character, word, blank_word):
		changed = False
		count = 0

		for index, char in enumerate(word):
			if char == character:
				# TODO: try for evil hangman
				blank_word = self.replace_char_at_index(character, blank_word, index)
				self.set_new_blank_word(blank_word)
				changed = True
				count += 1
		return (changed, count)

	def replace_char_at_index(self, character, word, index):
		word_list = list(word)
		word_list[index] = character
		return ''.join(word_list)

	def set_new_blank_word(self, new_word):
		self.blank_word = new_word






