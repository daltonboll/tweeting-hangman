import tweepy

class TwitterConnection:
	KEYS_FILE = "keys"

	def __init__(self):
		self.keys = {}
		self.consumer_key = ""
		self.consumer_secret = ""
		self.access_token = ""
		self.access_token_secret = ""
		self.auth = ""
		self.api = ""
		self.user = ""

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

	def tweet_at_user(self, user):
		# TODO: implement tweeting
		user_handle = user.get_handle()


connection = TwitterConnection()
api = connection.get_api()
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

api.update_status(status="hello")