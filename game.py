class Game:

	MAX_GUESSES = 6

	def __init__(self, computer_player, user_player):
		self.computer_player = computer_player
		self.user_player = user_player

	def play(self):
		self.wrong_guesses = 0
		self.word = self.find_word()
		self.blank_word = self.get_blank_word(self.word)

		while self.blank_word != self.word and self.wrong_guesses < Game.MAX_GUESSES:
			self.letter = input("Guess a letter:\n")
			changed_tuple = self.replace_letters(self.letter, self.word, self.blank_word)
			changed = changed_tuple[0]

			if changed:
				count = changed_tuple[1]
				print("\nCongratulations! The letter '{}'' occured {} times.".format(self.letter, count))
				print("The mystery word is now: {}\n".format(self.blank_word))
			else:
				print("\nSorry! The letter '{}'' does not appear in the mystery word.".format(self.letter))
				self.wrong_guesses += 1
				print("You've got {} guesses remaining.".format(self.get_remaining_guesses(Game.MAX_GUESSES, self.wrong_guesses)))

		if self.blank_word == self.word:
			print("Woohoo! You guessed the word with {} guesses left! It was '{}'. Thanks for playing!".format(self.get_remaining_guesses(Game.MAX_GUESSES, self.wrong_guesses), self.word))
		else:
			print("Dang - looks like you ran out of guesses! Try again next time. (The word was '{}')".format(self.word))

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

	def get_remaining_guesses(self, max_guesses, wrong_guesses):
		return max_guesses - wrong_guesses





