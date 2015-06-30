from game import Game
from user import User
from twitterConnection import TwitterConnection

# This file is the 'control' of the game, where a new Game instance is initialized and Users are set.

handle = input("Enter your Twitter username (no '@'): ")
player = User(handle)
twitter_connection = TwitterConnection(player)

game = Game("computer", player, twitter_connection) # create a new game instance. TODO: create computer/user from User class
game.play(evil_mode=True) # start the game!