import random
import string

class Game:

	MAX_GUESSES = 6 # the maximum guesses a User can have before the game ends
	WORD_FILE_PATH = "wordProcessor/words.txt" # the path of the word dictionary
	debug = True # when debug is True, print extra output to the console for debugging use

	def __init__(self, computer_player, user_player):
		"""
		Initialize the game. Set computer_player and user_player variables.

		computer_player = the User that is the computer player
		user_player = the User that is the human player
		"""
		self.computer_player = computer_player
		self.user_player = user_player
		self.word_dictionary = {}

	def play(self, evil_mode=False):
		"""
		The 'brain' of the game. Handles collecting input and keeps the game flowing.
		The mode is default to 'easy', which is normal hangman. When the mode is 'evil',
		the computer player will be smart about its words and try to make the User lose 
		at all costs.

		evil_mode = a boolean, defaulted to False. When true, play the game in 'evil' mode.
		"""
		self.letters_guessed = [] # letters the User has already guessed
		self.word_list = self.load_words() # grab a list of every word in our dictionary
		self.word_list_length = len(self.word_list) # the number of words in our dictionary
		self.wrong_guesses = 0 # the number of times the User has guessed incorrectly
		word_tuple = self.find_word() # a tuple containing (mystery word chosen, mystery word chosen with spaces for formatting)
		self.word = word_tuple[0] # the mystery word chosen for the user to guess
		self.word_with_spaces = word_tuple[1] # the mystery word with spaces
		self.blank_word = self.add_spaces_to_word(self.get_blank_word(self.word)) # the mystery word in space and underscore format (_ _ _...)

		# If debugging, display the mystery word info to the console
		if Game.debug:
			print("word: " + self.word)
			print("word with spaces: '{}'".format(self.word_with_spaces))

		print("Here's the mystery word: " + self.blank_word) # show the user the mystery word blank spaces

		# while the user hasn't guessed every letter AND the user still has guesses remaining:
		while self.blank_word != self.word_with_spaces and self.wrong_guesses < Game.MAX_GUESSES:
			if Game.debug:
				print("word with spaces: " + self.word_with_spaces)
				print("word: " + self.word)
				print("blank_word: " + self.blank_word)
			self.letter = input("Guess a letter:\n").lower() # ask the user for input, convert to lowercase


			# check to see if the user gave valid input (a single alphabetical letter)
			if not self.string_is_single_letter(self.letter):
				print("Uh oh, that's not a valid input. Try single alphabetical letters please!")
				continue

			# check to see if the user has already guessed that letter before
			if self.letter in self.letters_guessed:
				print("Woops! You already guessed the letter '{}'.".format(self.letter))
				continue
			else:
				self.letters_guessed.append(self.letter) # if not, add the letter to letters_guessed
				if Game.debug:
					print("Letters guessed so far: {}".format(self.letters_guessed))

			# grab a tuple with (boolean of whether or not the user's letter was in the word, count of how many times the letter appeared in the word, and the blank word with letters replaced)
			changed_tuple = self.replace_letters(self.letter, self.word_with_spaces, self.blank_word)
			changed = changed_tuple[0] # get the boolean
			blank_word_with_letters_replaced = changed_tuple[2]

			if changed and evil_mode: # if the user guessed a valid letter, notify them
				evil_word = self.find_evil_word(self.blank_word)
				if evil_word != None:
					if Game.debug:
						print("Found a new evil word: {}\n".format(evil_word))
					new_blank_word = self.add_spaces_to_word(self.get_blank_word(evil_word)) # set the new blank_word to the formatted evil word
					self.word = evil_word
					self.word_with_spaces = self.add_spaces_to_word(evil_word)
					self.set_new_blank_word(new_blank_word) # set our updated blank_word
					changed = False

			if changed: # if the letter was changed or we failed to find a new evil word:
				count = changed_tuple[1]
				self.set_new_blank_word(blank_word_with_letters_replaced) # set our updated blank_word
				print("\nCongratulations! The letter '{}'' occured {} times.".format(self.letter, count))
				print("The mystery word is now: {}\n".format(self.blank_word))

			if not changed: # else, decrease their guesses remaining and notify them
				print("\nSorry! The letter '{}'' does not appear in the mystery word.".format(self.letter))
				self.wrong_guesses += 1
				print("You've got {} guesses remaining.".format(self.get_remaining_guesses(Game.MAX_GUESSES, self.wrong_guesses)))
				print("Here's the mystery word: " + self.blank_word)

		# once the guessing has stopped, check to see if the game finished because of winning or losing
		if self.blank_word == self.word_with_spaces:
			print("Woohoo! You guessed the word with {} guesses left! It was '{}'. Thanks for playing!".format(self.get_remaining_guesses(Game.MAX_GUESSES, self.wrong_guesses), self.word))
		else:
			print("Dang - looks like you ran out of guesses! Try again next time. (The word was '{}')".format(self.word))
		self.end_game() # end the game by closing interactions with Twitter, asking to play again, etc.

	def load_words(self):
		"""
		Returns a list of all of our possible words in our dictionary that we could use as
		the mystery word.
		"""
		print("Loading dictionary...", end="")
		word_file = open(Game.WORD_FILE_PATH, "r") # open the dictionary file for read-only use
		word_list = word_file.readlines() # add each word in the file to a list
		word_list = word_list[:-1] # remove the last blank line from the list
		word_file.close() # make sure to close the dictionary file

		for word in word_list: # for each in word in the dictionary:
			word = word[:-1] # remove the trailing \n character from the word
			word_length = len(word)
			if word_length in self.word_dictionary: # store a mapping from word length to a list of words
				self.word_dictionary[word_length].append(word)
			else:
				self.word_dictionary[word_length] = [word]
		
		print(" done! Let's begin.")
		return word_list

	def end_game(self):
		"""
		TODO: End the game by closing connections with Twitter, asking the user if they'd like
		to play again, etc.
		"""
		# TODO: add more functionality
		print("Game ended.")

	def find_evil_word(self, current_word):
		"""
		TODO: Returns a word in an 'evil' way. Finds a word in our dictionary that we could
		secretly replace the mystery word with, given the user just guessed a letter that would
		reveal extra spaces in our mystery word. E.g. current mystery word = 'pour'. Currently,
		the user sees 'p _ _ _'. The user guesses 'o'. We secretly replace the mystery word with
		'ping' to make the user think that 'o' was not in the mystery word. Note that the new evil
		mystery word must contain all letters that have already been revealed to the user. If no 
		evil word is found, return None

		current_word = a string containing the current word that we are trying to replace, of the 
			format '_ a _ _ ...'
		"""
		word_length = len(current_word.replace(" ", "")) # the length of the current word without spaces
		list_of_possible_words = self.word_dictionary[word_length]
		cutoff = 0

		for word in list_of_possible_words:
			cutoff += 1 # keep track of the cutoff so we don't have to re-check again in the future
			if self.can_replace(current_word, word) and word != self.word: # if the new word is a valid replacement and it's not equal to the previous word:
				self.word_dictionary[word_length] = list_of_possible_words[cutoff:] # remove invalid replacements
				print("found a new evil word: {}!".format(word))
				return word # return the evil word that we found

		self.word_dictionary[word_length] = [] # there are no possible words to change to
		return None

	def can_replace(self, spaced_word, word):
		"""
		Given a spaced_word of the format 'p _ _ r', and a word of the format 'pour', 
		will return true if the '_ _' can be filled in behind the scenes with the new 
		word. In this case, it would return True because 'p' and 'r' are already set 
		in both words, and there are two blank spaces that are left to be filled in 
		by any letter.

		spaced_word = a string of the format 'p _ _ r'
		word = a string of the format 'pour'
		"""
		#TODO: make sure the letters in the new word weren't previously guessed
		print("in can_replace| comparing {} to {}".format(word, spaced_word))
		word_to_replace = self.add_spaces_to_word(word)
		found_valid_letter = False

		for index, letter in enumerate(spaced_word):
			if letter != ' ':
				if word_to_replace[index] in self.letters_guessed and word_to_replace[index] not in spaced_word:
					print("The letter '{}' was already guessed before!".format(word_to_replace[index]))
					return False
				if letter == word_to_replace[index] or letter == '_':
					print("The letter '{}' matched!".format(letter))
					found_valid_letter = True
					continue
				else:
					print("The word '{}' DID NOT match '{}'".format(word_to_replace, spaced_word))
					return False
		if found_valid_letter:
			print("The word '{}' did match '{}'".format(word_to_replace, spaced_word))
			return True
		else:
			print("The word '{}' DID NOT match '{}'".format(word_to_replace, spaced_word))


	def find_word(self, mode="easy"):
		"""
		Returns a tuple with (a random word from our dictionary, that word with spaces
		for formatting). TODO: when mode="evil", set out to find an evil word.

		mode = a string containing either "easy" or "evil"
		"""
		random_number = random.randint(0, self.word_list_length - 1) # generate a random number between 0 and the length of our word list - 1
		word = self.word_list[random_number] # get the random word
		word = word[:-1] # remove the trailing \n character from the word
		word_with_spaces = self.add_spaces_to_word(word) # get the word with spaces
		return (word, word_with_spaces)

	def add_spaces_to_word(self, word):
		"""
		Returns word with spaces in between. E.g. if word="hello", returns "h e l l o".

		word = a string containing a single word
		"""
		word_with_spaces = ""
		for char in word:
			word_with_spaces = word_with_spaces + char + " "
		word_with_spaces = word_with_spaces[:-1] # remove trailing space
		return word_with_spaces

	def get_blank_word(self, word):
		"""
		Given a word, returns a string with only underscores (blank spaces). E.g. if
		the word is "hello", returns "_____".

		word = a string containing a single word
		"""
		blank_word = ""
		for i in range(0, len(word)):
			blank_word = blank_word + "_"
		return blank_word

	def replace_letters(self, character, word, blank_word):
		"""
		Returns a tuple with (a boolean of whether or not the character was found in the word/blank_word, 
		the count with the number of times that character occured).
		
		character = a single alphabetical character
		word = a single word
		blank_word = a form of word with underscores (_) having replaced certain characters
		"""
		changed = False
		count = 0

		for index, char in enumerate(word): # keep track of each index and character in the word
			if char == character: # if we found the character in the word:
				# TODO: try for evil hangman
				if Game.debug:
					print("In replace_letters| character = {}, blank_word = {}, index = {}\n".format(character, blank_word, index))
				blank_word = self.replace_char_at_index(character, blank_word, index) # put the character into the blank_word at the index it was found
				changed = True # update our boolean because the character was found
				count += 1 # increment the number of times the character was found
		return (changed, count, blank_word)

	def replace_char_at_index(self, character, word, index):
		"""
		Returns the replacement of a character at a specific index of a word.

		character = the character to insert into the word
		word = the word to have a character replaced
		index = the index of the word in which to replace the character
		"""
		word_list = list(word) # convert the word into a list
		word_list[index] = character # replace the character at that index with the new character
		return ''.join(word_list) # convert the list back into a string

	def set_new_blank_word(self, new_word):
		"""
		Replaces self.blank_word with new_word.

		new_word = the new word to set the blank_word to
		"""
		self.blank_word = new_word

	def get_remaining_guesses(self, max_guesses, wrong_guesses):
		"""
		Returns the number of guesses that the user has remaining.

		max_guesses = the limit to how many guesses the user can have (e.g. 6)
		wrong_guesses = the number of wrong guesses the user already has (e.g. 3)
		"""
		return max_guesses - wrong_guesses

	def string_is_single_letter(self, str):
		"""
		Returns True if the input str is a single character, and a 
		valid alphabetical character only.

		str = a string of any format
		"""
		alphabet = string.ascii_lowercase # a string containing each lowercase letter of the alphabet

		return len(str) == 1 and str in alphabet




