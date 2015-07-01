import tweepy
import time
import random
import string
import sys
from user import User

class TwitterConnection:
	KEYS_FILE = "keys"
	HANGMAN_HANDLE = "@TweetingHangman "

	def __init__(self, user, twitter_mode):
		self.keys = {}
		self.consumer_key = ""
		self.consumer_secret = ""
		self.access_token = ""
		self.access_token_secret = ""
		self.auth = ""
		self.api = ""
		self.user = user
		self.twitter_mode = twitter_mode

		if self.twitter_mode:
			self.get_keys()
			self.set_auth()
			self.set_api()

			self.last_tweet_id = self.get_users_previous_tweet_id()

	def get_keys(self):
		keys_file = open(TwitterConnection.KEYS_FILE, "r")
		keys_list = keys_file.read().splitlines()

		for line in keys_list:
			setting = line.split(" = ")
			key_name = setting[0]
			key_value = setting[1]
			self.keys[key_name] = key_value
		keys_file.close()

		self.consumer_key = self.keys["consumer_key"]
		self.consumer_secret = self.keys["consumer_secret"]
		self.access_token = self.keys["access_token"]
		self.access_token_secret = self.keys["access_token_secret"]

	def set_auth(self):
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)

	def set_api(self):
		self.api = tweepy.API(self.auth)

	def get_auth(self):
		return self.auth

	def get_api(self):
		return self.api

	def get_users_previous_tweet_id(self):
		user_handle = self.user.get_handle()
		try:
			print("Checking the id of the @{}'s last tweet...".format(user_handle))
			previous_tweet_lst = self.api.user_timeline(id=user_handle, count=1)
			if len(previous_tweet_lst) > 0:
				tweet = previous_tweet_lst[0]
				tweet_id = tweet.id
				return tweet_id
			else:
				return -1
		except tweepy.error.TweepError as e:
			print("Twitter returned an error: {}\n".format(e.__dict__))
			self.quit()

	def tweet_at_user(self, message, reply_to_status_id=None):
		user_handle = self.user.get_handle()
		tweet =  "@" + user_handle + " " + message
		tweet_copy = tweet[:]
		success = False
		time_to_wait = 0
		max_time_to_wait = 16
		

		while not success:
			if time_to_wait > max_time_to_wait:
				print("Can't successfully tweet user - too many timeouts.")
				self.quit()
			try:
				custom_hash = self.get_duplicate_avoider_hash() + " "
				if reply_to_status_id != None:
					self.api.update_status(status=(custom_hash + tweet), in_reply_to_status_id=reply_to_status_id)
				else:
					self.api.update_status(status=(custom_hash + tweet))

				print("Successfully tweeted @{}: '{}'".format(user_handle, (custom_hash + tweet)))
				success = True

			except tweepy.error.TweepError as e:
				time_to_wait += 3
				print("Twitter returned an error: {}\n".format(e.__dict__))
				print("Trying again in {} seconds...".format(time_to_wait))
				time.sleep(time_to_wait)


	def get_duplicate_avoider_hash(self):
		letters = string.ascii_lowercase
		numbers = "0123456789"
		custom_hash = ""

		rand_num = random.randint(0, 25)
		custom_hash += letters[rand_num]
		rand_num = random.randint(0, 9)
		custom_hash += numbers[rand_num]
		rand_num = random.randint(0, 25)
		custom_hash += letters[rand_num]

		return custom_hash

	def get_user_response(self):
		user_handle = self.user.get_handle()
		received_new_tweet = False
		max_wait = 7
		starting_wait = 5
		times_checked = 0

		print("Waiting for user response - checking every {} seconds for {} seconds... ".format(starting_wait, max_wait * starting_wait))

		while not received_new_tweet:
			if times_checked >= max_wait:
				break
			latest_tweet_lst = self.api.user_timeline(id=user_handle, count=1)
			if len(latest_tweet_lst) > 0:
				tweet = latest_tweet_lst[0]
				tweet_id = tweet.id
				if tweet_id != self.last_tweet_id and TwitterConnection.HANGMAN_HANDLE in tweet.text:
					self.last_tweet_id = tweet_id
					tweet_text = tweet.text.replace(TwitterConnection.HANGMAN_HANDLE, "").lower()
					print("@{} responded: '{}'".format(user_handle, tweet_text))
					return (tweet_text, tweet_id)
				else:
					print(times_checked, end=", ")
					times_checked += 1
					time.sleep(starting_wait)
					sys.stdout.flush()
			else:
				print(times_checked, end=", ")
				times_checked += 1
				time.sleep(starting_wait) # the user has no tweets
				sys.stdout.flush()

		print("User response timed out.")
		return None

	def quit(self):
		print("Qutting game.")
		sys.exit()
