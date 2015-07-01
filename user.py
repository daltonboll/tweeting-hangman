class User:
	"""
	A User has a Twitter handle that identifies them.
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

