"""
Author: Dalton Boll
GitHub: https://github.com/daltonboll/tweeting-hangman

USAGE: Run 'python3 tweetingHangman.py' from this project's directory. Interact with the GUI to play!
"""

class User:
	"""
	A User has a Twitter handle that identifies them. We will be tweeting 
	back and forth with the Twitter User.
	"""

	def __init__(self, handle):
		"""
		handle = a Twitter username, excluding the '@'
		"""
		self.handle = handle

	def get_handle(self):
		"""
		Returns this User's Twitter username, excluding the '@'.
		"""
		return self.handle

