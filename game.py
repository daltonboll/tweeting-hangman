import random
import string

class Game:

	MAX_GUESSES = 6
	WORD_FILE_PATH = "wordProcessor/words.txt"

	def __init__(self, computer_player, user_player):
		self.computer_player = computer_player
		self.user_player = user_player

	def play(self, mode="easy"):
		self.letters_guessed = []
		self.word_list = self.load_words()
		self.word_list_length = len(self.word_list)
		self.wrong_guesses = 0
		word_tuple = self.find_word()
		self.word = word_tuple[0]
		self.word_with_spaces = word_tuple[1]
		self.blank_word = self.add_spaces_to_word(self.get_blank_word(self.word))

		print("word: " + self.word)
		print("word with spaces: '{}'".format(self.word_with_spaces))
		print("Here's the mystery word: " + self.blank_word)

		while self.blank_word != self.word_with_spaces and self.wrong_guesses < Game.MAX_GUESSES:
			self.letter = input("Guess a letter:\n").lower()

			if not self.string_is_single_letter(self.letter):
				print("Uh oh, that's not a valid input. Try single alphabetical characters please!")
				continue

			if self.letter in self.letters_guessed:
				print("Woops! You already guessed the letter '{}'.".format(self.letter))
				continue
			else:
				self.letters_guessed.append(self.letter)

			changed_tuple = self.replace_letters(self.letter, self.word_with_spaces, self.blank_word)
			changed = changed_tuple[0]

			if changed:
				count = changed_tuple[1]
				print("\nCongratulations! The letter '{}'' occured {} times.".format(self.letter, count))
				print("The mystery word is now: {}\n".format(self.blank_word))
			else:
				print("\nSorry! The letter '{}'' does not appear in the mystery word.".format(self.letter))
				self.wrong_guesses += 1
				print("You've got {} guesses remaining.".format(self.get_remaining_guesses(Game.MAX_GUESSES, self.wrong_guesses)))
				print("Here's the mystery word: " + self.blank_word)

		if self.blank_word == self.word_with_spaces:
			print("Woohoo! You guessed the word with {} guesses left! It was '{}'. Thanks for playing!".format(self.get_remaining_guesses(Game.MAX_GUESSES, self.wrong_guesses), self.word))
		else:
			print("Dang - looks like you ran out of guesses! Try again next time. (The word was '{}')".format(self.word))
		self.end_game()

	def load_words(self):
		print("Loading dictionary...", end="")
		word_file = open(Game.WORD_FILE_PATH, "r") # open word file for read-only use
		word_list = word_file.readlines() # add each word in the file to a list
		word_list = word_list[:-1] # remove blank line from list
		word_file.close()
		print(" done! Let's begin.")
		return word_list

	def end_game(self):
		print("Game ended.")

	def find_evil_word(self):
		pass

	def find_word(self, mode="easy"):
		random_number = random.randint(0, self.word_list_length - 1)
		word = self.word_list[random_number] # get the random word
		word = word[:-1] # remove the trailing \n character
		word_with_spaces = self.add_spaces_to_word(word)
		return (word, word_with_spaces)

	def add_spaces_to_word(self, word):
		word_with_spaces = ""
		for char in word:
			word_with_spaces = word_with_spaces + char + " "
		word_with_spaces = word_with_spaces[:-1] # remove trailing space
		return word_with_spaces

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

	def string_is_single_letter(self, str):
		alphabet = string.ascii_lowercase

		return len(str) == 1 and str in alphabet




