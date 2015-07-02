"""
Author: Dalton Boll

USAGE: Run 'python3 tweetingHangman.py' from this project's directory. Interact with the GUI to play!

This file is the 'control' of the game, where a new Game instance is initialized and Users are set.
The GUI is also produced in this file.

"""

from game import Game
from user import User
from twitterConnection import TwitterConnection
from tkinter import *


class Application(Frame):

    def __init__(self, master=None):
        """
        Initialize the Application.

        master = the root tkinter interface
        """
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.game = None

    def createWidgets(self):
        """
        Creates the objects to be used in the GUI.
        """
        self.label_test = Label(self, text="Your Twitter username (no '@'):")
        self.label_test.grid(row=0, column=0)

        self.username_field = Entry(self)
        self.username_field.grid(row=0, column=1)

        self.using_twitter = IntVar()
        self.radio1 = Radiobutton(self, text="Play over Twitter", variable=self.using_twitter, value=1)
        self.radio2 = Radiobutton(self, text="Play over the terminal", variable=self.using_twitter, value=0)
        self.radio1.grid(row=1, column=0)
        self.radio1.select()
        self.radio2.grid(row=1, column=1)

        self.evil_mode = IntVar()
        self.radio3 = Radiobutton(self, text="Normal Hangman Mode", variable=self.evil_mode, value=0)
        self.radio4 = Radiobutton(self, text="Evil Hangman Mode", variable=self.evil_mode, value=1)
        self.radio3.grid(row=2, column=0)
        self.radio3.select()
        self.radio4.grid(row=2, column=1)

        self.start_button = Button(self, text="START", command=self.start)
        self.start_button.grid(row=3, column=0, columnspan=1)

        self.quit_button = Button(self, text="QUIT", fg="red", command=self.quit)
        self.quit_button.grid(row=3, column=2, columnspan=1)

        label_text = """
        Step 1: Type in your Twitter username/handle, without the '@' sign.

        Step 2: Select to play over Twitter or through the terminal. Terminal mode
        should be used for debugging purposes only.

        Step 3: Select to play against a generic Hangman computer, or an 'evil' 
        Hangman, who will try its best to outsmart you!

        Step 4: Navigate to https://twitter.com/i/notifications
        This allows you to see dynamic updates when @TweetingHangman tweets you, 
        so you can easily hit the reply button to respond.

        Step 5: Click 'START' to begin the game.

        Step 6: Wait until you get a tweet from @TweetingHangman welcoming you to 
        play. You might have to refresh your Twitter notifications page.

        Step 7: Reply to @TweetingHangman with a single letter at a time, until 
        you guess the mystery word correctly!

        Notes:
        - If you'd like to restart the game, or play with a new user, click 
        the 'STOP' button, and you can then start over again at Step 1.
        - If you'd like to quit playing completely, click the 'QUIT' button, 
        and be on your merry way!
        """

        self.instructions = Label(self, text=label_text)
        self.instructions.grid(row=4, sticky="W", columnspan=6)

    def start(self):
        handle = self.username_field.get()
        print("Playing against @{}".format(handle))
        playing_with_twitter = self.using_twitter.get()
        print("Playing with Twitter? {}".format(bool(playing_with_twitter)))
        playing_evil_mode = self.evil_mode.get()
        print("Playing evil mode? {}".format(bool(playing_evil_mode)))

        player = User(handle)
        twitter_connection = TwitterConnection(player, twitter_mode=playing_with_twitter)

        self.game = Game("computer", player, twitter_connection, twitter_mode=playing_with_twitter) # create a new game instance
        self.game.play(evil_mode=playing_evil_mode) # start the game!
        print("Gathering user input values...")
        username = self.username_field.get()
        print("username: {}; using twitter? {}".format(username, bool(self.using_twitter.get())))

    def quit(self):
        print("User wants to quit.")
        root.destroy()
        if self.game != None:
            self.game.end_game()


root = Tk()
root.title("Tweeting Hangman") #This is the tile at the top of the window

#make my screen dimensions work
w = 800 #The value of the width
h = 700 #The value of the height of the window

# get screen width and height
ws = root.winfo_screenwidth()#This value is the width of the screen
hs = root.winfo_screenheight()#This is the height of the screen

# calculate position x, y
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

#This is responsible for setting the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
app = Application(master=root)
app.mainloop()
