import tweepy
import time
from user import User

class TwitterConnection:
	KEYS_FILE = "keys"
	HANGMAN_HANDLE = "@TweetingHangman "

	def __init__(self, user):
		self.keys = {}
		self.consumer_key = ""
		self.consumer_secret = ""
		self.access_token = ""
		self.access_token_secret = ""
		self.auth = ""
		self.api = ""
		self.user = user
		self.last_tweet_id = -1

		self.get_keys()
		self.set_auth()
		self.set_api()

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

	def tweet_at_user(self, message):
		user_handle = self.user.get_handle()
		tweet = "@" + user_handle + " " + message
		success = False
		time_to_wait = 0
		failed_text = " - TH :)"

		while not success:
			try:
				self.api.update_status(status=tweet)
				success = True
			except tweepy.error.TweepError as e:
				time_to_wait += 3
				print("Twitter returned an error: {}\n".format(e))
				print("Trying again in {} seconds...".format(time_to_wait))
				time.sleep(time_to_wait)
				if failed_text in tweet:
					tweet = tweet.replace(failed_text, "")
				else:
					tweet = tweet + failed_text

	def get_user_response(self):
		user_handle = self.user.get_handle()
		received_new_tweet = False
		max_wait = 35
		starting_wait = 1
		times_checked = 0

		print("Waiting for user response - checking every {} seconds for {} seconds...".format(starting_wait, max_wait))

		while not received_new_tweet:
			if times_checked >= max_wait:
				break
			latest_tweet_lst = self.api.user_timeline(id=user_handle, count=1)
			if len(latest_tweet_lst) > 0:
				tweet = latest_tweet_lst[0]
				tweet_id = tweet.id
				if tweet_id != self.last_tweet_id and TwitterConnection.HANGMAN_HANDLE in tweet.text:
					self.last_tweet_id = tweet_id
					return tweet.text.replace(TwitterConnection.HANGMAN_HANDLE, "")
				else:
					time.sleep(starting_wait)
					times_checked += 1
			else:
				time.sleep(starting_wait) # the user has no tweets
				times_checked += 1

		return None






connection = TwitterConnection(User("google"))
latest_tweet = connection.get_user_response()

print("latest tweet: {}".format(latest_tweet))

