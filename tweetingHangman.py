from game import Game

# This file is the 'control' of the game, where a new Game instance is initialized and Users are set.

game = Game("computer", "user") # create a new game instance. TODO: create computer/user from User class
game.play(evil_mode=True) # start the game!