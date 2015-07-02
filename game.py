"""
Author: Dalton Boll

USAGE: Run 'python3 tweetingHangman.py' from this project's directory. Interact with the GUI to play!
"""

import random # for random number generation
import string # for grabbing all legal alphabetical characters
import tweepy # for connecting to Twitter
import sys # for exiting the program

class Game:
	"""
	The Game class is the 'control' of TweetingHangman. It loops and gathers 
	user input, and directs interaction with the User.
	"""

	MAX_GUESSES = 6 # the maximum guesses a User can have before the game ends
	WORD_FILE_PATH = "wordProcessor/words.txt" # the path of the word dictionary
	debug = False # when debug is True, print extra output to the console for debugging use

	def __init__(self, computer_player, user_player, twitter_connection, twitter_mode=True):
		"""
		Initialize the game.

		computer_player = the User that is the computer player
		user_player = the User that is the human player
		twitter_connection = an instance of the TwitterConnection class
		twitter_mode = when true, we are sending tweets over Twitter and not playing through the terminal
		"""
		self.computer_player = computer_player
		self.user_player = user_player
		self.word_dictionary = {} # used in 'evil' mode - maps word length to a list of words of that length
		self.twitter_connection = twitter_connection
		self.twitter_mode = twitter_mode

	def play(self, evil_mode=False):
		"""
		The 'brain' of the game. Handles collecting input and keeps the game flowing.
		The evil_mode argument is defaulted to False, which is normal hangman. When True,
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
		self.last_user_tweet_id = -1 # the id of the user's last tweet
		# a list of possible welcome messages, used to keep Twitter duplicate tweet detection away
		self.intro_messages = ["Let's play! Guess a letter from the mystery word: {}".format(self.blank_word), \
			"Welcome to Twitter Hangman! Here's the mystery word: {}. Guess a letter!".format(self.blank_word), \
			"Guess a letter (Here's the mystery word: {})".format(self.blank_word)]

		# If debugging, display the mystery word info to the console
		if Game.debug:
			print("word: " + self.word)
			print("word with spaces: '{}'".format(self.word_with_spaces))

		random_intro = self.intro_messages[random.randint(0, len(self.intro_messages) - 1)] # choose a random intro message
		self.message(random_intro) # show the user the mystery word blank spaces
		timeout = False # timeout is True when we haven't received a user response in a while

		# while the user hasn't guessed every letter AND the user still has guesses remaining:
		while self.blank_word != self.word_with_spaces and self.wrong_guesses < Game.MAX_GUESSES:
			
			if Game.debug: # print debugging statements if we are in debug mode
				print("--------------------")
				print("word with spaces: " + self.word_with_spaces)
				print("word: " + self.word)
				print("blank_word: " + self.blank_word)
				print("--------------------\n")

			self.letter = self.get_user_input() # ask the user for input

			if self.twitter_mode and self.letter != None: # if we are in twitter mode and we have a user response:
				self.last_user_tweet_id = self.letter[1] # set the tweet id of the response
				self.letter = self.letter[0] # set the text of the tweet response

			if self.letter == None: # if we have don't have a user response:
				if timeout: # if this is the second time in a row without a response on the same turn, end the game
					print("Game ended due to lack of user response.")
					self.end_game()
				else:
					timeout = True # set the timeout variable for a possible game termination next turn if there is no response again
					# rempromp the user for input, and continue on
					self.message("Do you still want to play? If so, guess a letter! Otherwise, game will timeout in 35 secs.")
					continue
			else: # we received a response, end the timeout cycle
				timeout = False

			# quit the game if the user asks
			if self.letter == "quit":
				print("User asked to quit the game.")
				self.end_game()

			# check to see if the user gave valid input (a single alphabetical letter)
			if not self.string_is_single_letter(self.letter):
				self.message("Invalid input. Try single alphabetical letters please! Guess a letter!")
				continue

			# check to see if the user has already guessed that letter before
			if self.letter in self.letters_guessed:
				self.message("Woops! You already guessed the letter '{}'. Guess a new letter!".format(self.letter))
				continue
			else:
				self.letters_guessed.append(self.letter) # if not, add the letter to letters_guessed
				if Game.debug:
					print("Letters guessed so far: {}".format(self.letters_guessed))

			# grab a tuple with (boolean of whether or not the user's letter was in the word, count of how many times the letter appeared in the word, and the blank word with letters replaced)
			changed_tuple = self.replace_letters(self.letter, self.word_with_spaces, self.blank_word)
			changed = changed_tuple[0] # get the boolean
			blank_word_with_letters_replaced = changed_tuple[2] # get the blank word with letters replaced 

			if changed and evil_mode: # if the user guessed a valid letter and we're in evil mode:
				evil_word = self.find_evil_word(self.blank_word) # find a possible evil word for the current game layout
				if evil_word != None: # if we found an evil word:
					if Game.debug:
						print("Found a new evil word: {}\n".format(evil_word))
						print("Old mystery word: {}; Old word_with_spaces: {}; Old blank_word: {}\n".format(self.word, self.word_with_spaces, self.blank_word))
					# reset the word to the evil word
					self.word = evil_word
					self.word_with_spaces = self.add_spaces_to_word(evil_word)
					if Game.debug:
						print("New mystery word: {}; New word_with_spaces: {}; New blank_word: {}\n".format(self.word, self.word_with_spaces, self.blank_word))
					changed = False # the user 'did not' (hehe) guess a correct letter!

			if changed: # if the user guessed a correct letter and/or we failed to find a new evil word:
				count = changed_tuple[1] # the number of times the letter appeared in the word
				self.set_new_blank_word(blank_word_with_letters_replaced) # set our updated blank_word
				self.message("Congratulations! The letter '{}'' occured {} times. The mystery word is now: {}".format(self.letter, count, self.blank_word))

			if not changed: # else, decrease their guesses remaining by incrementing wrong guesses and notify them
				self.wrong_guesses += 1
				self.message("The letter '{}' doesn't appear. {} guesses remaining. Mystery word: {}. Guess a letter!".format(self.letter, self.get_remaining_guesses(Game.MAX_GUESSES, self.wrong_guesses), self.blank_word))

		# once the guessing has stopped, check to see if the game finished because of winning or losing
		if self.blank_word == self.word_with_spaces:
			self.message("Woohoo! You guessed the word with {} guesses left! It was '{}'. Thanks for playing!".format(self.get_remaining_guesses(Game.MAX_GUESSES, self.wrong_guesses), self.word))
		else:
			self.message("Dang - looks like you ran out of guesses! Try again next time. (The word was '{}')".format(self.word))

		self.end_game() # end the game once the guessing has stopped

	def load_words(self):
		"""
		Returns a list of all of the possible words in our dictionary that we could use as
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
		Quits the game and exits the program.
		"""
		print("Ending the game.")
		sys.exit()

	def find_evil_word(self, current_word):
		"""
		Returns a word in an 'evil' way. Finds a word in our dictionary that we could
		secretly replace the mystery word with, given the user just guessed a letter that would
		reveal extra spaces in our mystery word. E.g. current mystery word = 'pour'. Currently,
		the user sees 'p _ _ _'. The user guesses 'o'. We secretly replace the mystery word with
		'ping' to make the user think that 'o' was not in the mystery word. Note that the new evil
		mystery word must contain all letters that have already been revealed to the user. If no 
		evil word is found, return None.

		current_word = a string containing the current word that we are trying to replace, of the 
			format '_ a _ _ ...'
		"""
		word_length = len(current_word.replace(" ", "")) # the length of the current word without spaces
		list_of_possible_words = self.word_dictionary[word_length] # the possible words we could replace the current_word with

		while len(list_of_possible_words) > 1: # while we still have possible evil words left:
			index = random.randint(0, len(list_of_possible_words) - 1) # randomly select a possible word to prevent patterns
			word = list_of_possible_words[index]
			list_of_possible_words.remove(word) # remove that possible words from our list so we don't pick it again
			if self.can_replace(current_word, word) and word != self.word: # if the new word is a valid replacement and it's not equal to the previous word:
				self.word_dictionary[word_length] = list_of_possible_words # remove invalid replacements
				if Game.debug:
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
		if Game.debug:
			print("in can_replace| comparing {} to {}".format(word, spaced_word))
		word_to_replace = self.add_spaces_to_word(word) # add spaces to the regular word for easier comparison
		found_valid_letter = False # True when we find a letter that can be replaced

		for index, letter in enumerate(spaced_word):
			if letter != ' ': # we don't care about spaces
				# if the current letter has already been guessed and it's not in the spaced_word (which has already been partially revealed to the user):
				if word_to_replace[index] in self.letters_guessed and word_to_replace[index] not in spaced_word:
					if Game.debug:
						print("The letter '{}' was already guessed before!".format(word_to_replace[index]))
					return False # this word isn't a valid replacement
				# if the letters match up or are equal to underscores, keep searching through the word because we might have a match
				if letter == word_to_replace[index] or letter == '_':
					if Game.debug:
						print("The letter '{}' matched!".format(letter))
					found_valid_letter = True # the current letter is a valid one
					continue
				else:
					if Game.debug:
						print("The word '{}' DID NOT match '{}'".format(word_to_replace, spaced_word))
					return False # otherwise, stop looking in this word because it can't be a match
		if found_valid_letter: # return True if this word is a valid match and can replace the current word 'evily'
			if Game.debug:
				print("The word '{}' did match '{}'".format(word_to_replace, spaced_word))
			return True
		else:
			if Game.debug:
				print("The word '{}' DID NOT match '{}'".format(word_to_replace, spaced_word))
			return False

	def find_word(self):
		"""
		Returns a tuple with (a random word from our dictionary, that word with spaces
		for formatting).
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
		word_with_spaces = "" # start out with a blank word
		for char in word: # for each character in the word:
			word_with_spaces = word_with_spaces + char + " " # add spaces!
		word_with_spaces = word_with_spaces[:-1] # remove trailing space
		return word_with_spaces

	def get_blank_word(self, word):
		"""
		Given a word, returns a string with only underscores (blank spaces). E.g. if
		the word is "hello", returns "_____".

		word = a string containing a single word
		"""
		blank_word = "" # start out with a blank word
		for i in range(0, len(word)): # add (length of the word)-underscores to the blank word
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
		return max_guesses - wrong_guesses # guesses remaining = guesses allowed minus guesses used

	def string_is_single_letter(self, str):
		"""
		Returns True if the input str is a single character, and a 
		valid alphabetical character only.

		str = a string of any format
		"""
		alphabet = string.ascii_lowercase # a string containing each lowercase letter of the alphabet
		return len(str) == 1 and str in alphabet # the input has to be a single alphabetical character

	def message(self, text):
		"""
		Communicates with the player via the print command over the terminal, or via Twitter - 
		depending on which mode the program is running in (based on self.twitter_mode).

		text = the text to communicate to the user
		"""
		if self.twitter_mode: # if we are communicating over Twitter:
			print("Tweeting @{}...    ".format(self.user_player.get_handle()), end="")
			try: # try to tweet at the user
				if self.last_user_tweet_id != -1: # reply to the user's last tweet if it exists
					self.twitter_connection.tweet_at_user(text, reply_to_status_id=self.last_user_tweet_id)
				else: # otherwise, send the user a new tweet conversation
					self.twitter_connection.tweet_at_user(text)
			# if we get an error, print it to the console and end the game
			# error messages are very finicky, which is why there are not current plans to allow the user to try and fix them
			except tweepy.error.TweepError as e: 
				print("Twitter connection returned error: {}".format(e.__dict__))
				self.end_game()
		else: # otherwise, if we're using the terminal, just print the message text via the console
			print(text + "\n")

	def get_user_input(self):
		"""
		Requests new user replies from Twitter if self.twitter_mode is True, otherwise 
		requests new user input from the console.
		"""
		if self.twitter_mode: # if we are in Twitter mode:
			try: # try to get a user response from Twitter
				return self.twitter_connection.get_user_response()
			# if we get an error, exit the game because tweepy/Twitter API errors are finicky
			except tweepy.error.TweepError as e:
				print("Twitter connection returned error: {}".format(e.__dict__))
				self.end_game()
		else: # otherwise, if we're using the terminal, just ask for input via the console
			return input("Guess a letter:\n").lower()

