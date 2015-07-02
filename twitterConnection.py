"""
Author: Dalton Boll
GitHub: https://github.com/daltonboll/tweeting-hangman

USAGE: Run 'python3 tweetingHangman.py' from this project's directory. Interact with the GUI to play!
"""

import tweepy # for connecting to the Twitter API
import time # for polling the Twitter API in intervals
import random # for generating random integers
import string # for grabbing all legal alphabetical characters
import sys # for exiting the program
from user import User # for access to the User that we are tweeting to

class TwitterConnection:
	"""
	The TwitterConnection class provides utilization of the tweepy library to 
	communicate with the Twitter API.
	"""

	# the name of the file where the Twitter authorization keys are stored
	KEYS_FILE = "keys" # NOTE: not hosted on GitHub - must be provided
	HANGMAN_HANDLE = "@TweetingHangman " # the Twitter handle of the account held for the Tweeting Hangman program

	def __init__(self, user, twitter_mode):
		"""
		user = a User object, which we are tweeting at
		twitter_mode = a boolean, True if we should try and connect to Twitter. 
			When False, the TwitterConnection object is stagnant and does nothing.
			This behavior is useful when we are playing a game via the terminal, not 
			over Twitter.
		"""
		self.keys = {} # a dictionary that maps the Twitter authorization keys
		self.consumer_key = "" # Twitter consumer key
		self.consumer_secret = "" # Twitter consumer secret key
		self.access_token = "" # Twitter access token key
		self.access_token_secret = "" # Twitter access token secret key
		self.auth = "" # tweepy auth
		self.api = "" # tweepy api
		self.user = user # the Twitter user we are tweeting at
		self.twitter_mode = twitter_mode # true if we are actively connecting to Twitter

		if self.twitter_mode: # if we should connect to Twitter, set up our connection
			self.get_keys() # grab our authentication keys from the file specified in KEYS_FILE
			self.set_auth() # set the tweepy auth
			self.set_api() # set the tweepy api
			# grab the id of the last tweet of our User
			self.last_tweet_id = self.get_users_previous_tweet_id() # used to determine if the user's last tweet was for us or not

	def get_keys(self):
		"""
		Grabs our authorization keys from the file specified in KEYS_FILE. We need:
		- consumer key
		- consumer secret key
		- access token key
		- access token secret key

		The KEYS_FILE should contain one key on each line, of the format:
		key_name = key
		Where key_name is one of (consumer_key, consumer_secret, access_token, access_token_secret), 
		and key is the actual passkey correlating to the key_name.

		NOTE: the KEYS_FILE associated with the @TweetingHangman Twitter account is not 
		kept on GitHub. This game can be run with any Twitter user with developer keys, 
		however, so as long as you have a Twitter account and a valid KEYS_FILE file, 
		the game should still run fine.
		"""
		keys_file = open(TwitterConnection.KEYS_FILE, "r") # open the keys file
		keys_list = keys_file.read().splitlines() # create a list with each 'key_name = key' string

		for line in keys_list: # for each 'key_name = key':
			setting = line.split(" = ") # split the string between the equals sign
			key_name = setting[0] # grab the key name
			key_value = setting[1] # grab the passkey
			self.keys[key_name] = key_value # put the key pair into our keys dictionary
		keys_file.close() # close the KEYS_FILE file

		# set our variables to be associated with the passkey values
		self.consumer_key = self.keys["consumer_key"]
		self.consumer_secret = self.keys["consumer_secret"]
		self.access_token = self.keys["access_token"]
		self.access_token_secret = self.keys["access_token_secret"]

	def set_auth(self):
		"""
		Sets the tweepy authorization using OAuthHandler. Uses the developer keys
		we grabbed from KEYS_FILE.

		NOTE: All of our developer keys must already be set before calling this 
		function (i.e. self.consumer_key, self.consumer_secret, self.access_token, 
		and self.access_token_secret). These keys should be set by calling the 
		get_keys() function.
		"""
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)

	def set_api(self):
		"""
		Sets the tweepy api using the authorization we set in the set_auth() function. 

		NOTE: set_auth must be called first before this function.
		"""
		self.api = tweepy.API(self.auth)

	def get_auth(self):
		"""
		Returns the tweepy authorization instance.
		"""
		return self.auth

	def get_api(self):
		"""
		Returns the tweepy api instance.
		"""
		return self.api

	def get_users_previous_tweet_id(self):
		"""
		Returns the tweet id of the self.user's last tweet. This is useful for 
		determining if the user has actually tweeted us yet, or if they have 
		tweets left over from their last game. Returns -1 if the user has no 
		tweets.
		"""
		user_handle = self.user.get_handle() # sets the username of self.user
		# try to communicate with Twitter
		try:
			print("Checking the id of the @{}'s last tweet...".format(user_handle))
			previous_tweet_lst = self.api.user_timeline(id=user_handle, count=1) # gets a list containing the user's last tweet (count=1 denotes 1 tweet)
			if len(previous_tweet_lst) > 0: # check to see if the user actually has any tweets
				tweet = previous_tweet_lst[0] # grab the only tweet in the list
				tweet_id = tweet.id # return the id of the user's last tweet
				return tweet_id
			else: # if the user has no tweets, return -1
				return -1
		# if we encounter an error while communicating with Twitter, quit the program
		# the API's error codes are too finicky for the user to try and correct them, so it's 
		# best to just restart the game
		except tweepy.error.TweepError as e:
			print("Twitter returned an error: {}\n".format(e.__dict__))
			self.quit()

	def tweet_at_user(self, message, reply_to_status_id=None):
		"""
		Sends a tweet containing the text in message. Attempts to reply to the 
		user's last tweet if reply_to_status_id is set, otherwise just sends 
		a new tweet.
		"""
		user_handle = self.user.get_handle() # grab the user's twitter handle
		tweet =  "@" + user_handle + " " + message # format the message
		tweet_copy = tweet[:] # make a copy of the tweet message
		success = False # when True, sending the message was successful
		time_to_wait = 0 # time to wait between retrying tweeting if it fails
		max_time_to_wait = 16 # maximum time to wait between retries
		
		while not success: # while we haven't succeeded at tweeting:
			# if we tried multiple times and it still failed, quit because Twitter is blocking our communication
			if time_to_wait > max_time_to_wait:
				print("Can't successfully tweet user - too many timeouts.")
				self.quit()
			# try to tweet
			try:
				custom_hash = self.get_duplicate_avoider_hash() + " " # create a hash to avoid Twitter blocking us for duplicate tweets
				if reply_to_status_id != None: # if we have a tweet to reply to, tweet a reply!
					self.api.update_status(status=(custom_hash + tweet), in_reply_to_status_id=reply_to_status_id)
				else: # otherwise, start a new conversation with a tweet
					self.api.update_status(status=(custom_hash + tweet))

				print("Successfully tweeted @{}: '{}'".format(user_handle, (custom_hash + tweet)))
				success = True # we succeeded at sending a tweet

			# if we get an error, try tweeting again in a little bit
			except tweepy.error.TweepError as e:
				time_to_wait += 3 # increment our waiting time between retries
				print("Twitter returned an error: {}\n".format(e.__dict__))
				print("Trying again in {} seconds...".format(time_to_wait))
				time.sleep(time_to_wait) # sleep for a bit

	def get_duplicate_avoider_hash(self):
		"""
		Returns a 3-character hash string of the folowing format: 'XYX', where X 
		is a letter from a to z and Y is a number from 0 to 9.
		"""
		letters = string.ascii_lowercase # grab all legal alphabetical characters
		numbers = "0123456789" # all numbers
		custom_hash = "" # initialize our custom hash

		# grab a random letter and add it to the hash
		rand_num = random.randint(0, 25)
		custom_hash += letters[rand_num]

		# grab a random number and add it to the hash
		rand_num = random.randint(0, 9)
		custom_hash += numbers[rand_num]

		# grab a random letter and add it to the hash
		rand_num = random.randint(0, 25)
		custom_hash += letters[rand_num]

		return custom_hash

	def get_user_response(self):
		"""
		Returns a tuple containing (user's tweet text, user's tweet id). The user's 
		tweet is a tweet in reply to @TweetingHangman's last tweet.
		"""
		user_handle = self.user.get_handle() # get the User's username
		received_new_tweet = False # True when we've received a response tweet from the user
		max_wait = 7 # the maximum amount of times we will check for a new tweet
		starting_wait = 5 # the number of seconds to wait before checking again
		times_checked = 0 # times checked will be incremented until it reaches max_wait

		print("\nWaiting for user response - checking every {} seconds for {} seconds... ".format(starting_wait, max_wait * starting_wait))

		while not received_new_tweet: # while we haven't received a tweet response yet:
			if times_checked >= max_wait: # stop checking once we've checked max_wait
				break # it's necessary to quit to reduce API requests (too many = Twitter ban for 15 mins)

			latest_tweet_lst = self.api.user_timeline(id=user_handle, count=1) # grab the user's latest tweet
			if len(latest_tweet_lst) > 0: # if the user has a tweet:
				tweet = latest_tweet_lst[0] # get the tweet
				tweet_id = tweet.id # grab the tweet id

				# if the tweet references @TweetingHangman and was not the same as the user's last tweet before starting playing:
				if tweet_id != self.last_tweet_id and TwitterConnection.HANGMAN_HANDLE in tweet.text:
					self.last_tweet_id = tweet_id # reset the last tweet id
					tweet_text = tweet.text.replace(TwitterConnection.HANGMAN_HANDLE, "").lower() # make the response lowercase
					print("@{} responded: '{}'".format(user_handle, tweet_text))
					return (tweet_text, tweet_id) # return the text and tweet id
				else: # otherwise, keep waiting for a new tweet in response to @TweetingHangman
					print(times_checked, end=", ")
					times_checked += 1 # checked once more
					time.sleep(starting_wait) # sleep for starting_wait seconds
					sys.stdout.flush() # necessary to provide continuous console output on the same line
			else: # the user has no tweets, keep waiting for a tweet response
				print(times_checked, end=", ")
				times_checked += 1 # checked once more
				time.sleep(starting_wait) # sleep for starting_wait seconds
				sys.stdout.flush() # necessary to provide continuous console output on the same line

		print("User response timed out.")
		return None # we didn't receive a response tweet from the user

	def quit(self):
		"""
		Quits the program.
		"""
		print("Qutting game.")
		sys.exit()
