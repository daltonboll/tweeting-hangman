"""
Author: Dalton Boll
GitHub: https://github.com/daltonboll/tweeting-hangman

USAGE: Run 'python3 tweetingHangman.py' from this project's directory. Interact with the GUI to play!

This file is the 'control' of the game, where a new Game instance is initialized and Users are set.
The GUI is also produced in this file.
"""

from game import Game # for playing the Twitter Hangman game
from user import User # for giving the game a user
from twitterConnection import TwitterConnection # for communicating with Twitter
from tkinter import * # for GUI creation
import tkinter.messagebox # for popup message box creation


class Application(Frame):
    """
    The Application class is used to paint the Tkinter GUI, and control 
    the stopping and starting of the game. Inherits from the Tkinter 
    Frame object.
    """

    debug = False

    def __init__(self, master=None):
        """
        Initialize the Application.

        master = the root tkinter interface
        """
        Frame.__init__(self, master) # initialize the frame
        self.pack() # pack the frame with an interface
        self.paintObjects() # paint the various objects onto the GUI (e.g. buttons and labels)
        self.game = None # initialize the game to None - we don't create a Game instance until user input is gathered

    def paintObjects(self):
        """
        Creates the objects to be used in the GUI (e.g. buttons, lables, and text input).
        """
        self.username_label = Label(self, text="Your Twitter username (no '@'):") # initialize the Tkinter username Label
        self.username_label.grid(row=0, column=0) # paint the label onto the Frame in a grid format, specifying row and column

        self.username_field = Entry(self) # initialize the Tkinter username Entry field to collect the user's username
        self.username_field.grid(row=0, column=1) # paint the label onto the Frame in grid format

        self.using_twitter = IntVar() # used to tell if the twitter radio buttons are highlighted
        # initialize Tkinter radio buttons used for selecting terminal or twitter play, they connect to the self.using_twitter variable
        self.play_twitter_radio = Radiobutton(self, text="Play over Twitter", variable=self.using_twitter, value=1) # self.using_twitter = 1 when highlighted
        self.play_terminal_radio = Radiobutton(self, text="Play over the terminal", variable=self.using_twitter, value=0) # self.using_twitter = 0 when highlighted
        self.play_twitter_radio.grid(row=1, column=0) # paint the radio button onto the Frame in grid format
        self.play_twitter_radio.select() # automatically highlight the 'play over twitter' radio button
        self.play_terminal_radio.grid(row=1, column=1) # paint the radiob utton onto the Frame in grid format

        self.evil_mode = IntVar() # used to tell if the evil hangman radio buttons are highlighted
        # initialize Tkinter radio buttons used for selecting normal or evil hangman play, they connect to the self.evil_mode variable
        self.normal_hangman_radio = Radiobutton(self, text="Normal Hangman Mode", variable=self.evil_mode, value=0) # self.evil_mode = 0 when highlighted
        self.evil_hangman_radio = Radiobutton(self, text="Evil Hangman Mode", variable=self.evil_mode, value=1) # self.evil_mode = 1 when highlighted
        self.normal_hangman_radio.grid(row=2, column=0) # paint the radio button onto the Frame in grid format
        self.normal_hangman_radio.select() # automatically highlight the 'normal hangman mode' radio button
        self.evil_hangman_radio.grid(row=2, column=1) # paint the radio button onto the Frame in grid format

        self.start_button = Button(self, text="START", command=self.start) # initialize the Tkinter start button, linked to function self.start
        self.start_button.grid(row=3, column=0, columnspan=1) # paint the button onto the Frame in grid format, spanning 1 column

        self.quit_button = Button(self, text="QUIT", fg="red", command=self.quit) # initialize the Tkinter quit button, linked to the function self.quit 
        self.quit_button.grid(row=3, column=2, columnspan=1) # paint the button onto the Frame in grid format, spanning 1 column

        # Instructions to be painted onto the GUI for the user
        label_text = """
        Step 1: Type in your Twitter username/handle, without the '@' sign.

        Step 2: Select to play over Twitter or through the terminal.

        Step 3: Select to play against a generic Hangman computer, or an 'evil' 
        Hangman, who will try its best to outsmart you!

        Step 4: Navigate to https://twitter.com/i/notifications
        This allows you to see dynamic updates when @TweetingHangman tweets you, 
        so you can easily hit the reply button to respond.

        Step 5: Click 'START' to begin the game.

        Step 6: Wait until you get a tweet from @TweetingHangman welcoming you to 
        play. You should keep refreshing your Twitter notifications page until 
        you get a tweet, because the Twitter interface can be slow at dynamically 
        updating automatically.

        Step 7: Reply to @TweetingHangman with a single letter at a time, until 
        you guess the mystery word correctly!

        Notes:
        - To quit playing over Twitter mode: simply reply to @TweetingHangman with 
        the word 'quit' (no quotes), or right click on the GUI logo in your 
        application dock and close it there. Due to continuous polling of the Twitter 
        API, pressing the 'QUIT' button can cause the interface to freeze when in 
        Twitter mode. 
        - To quit playing over Terminal mode: type 'quit' (no quotes) in the terminal 
        or click the 'QUIT' button in the GUI.
        - Twitter limits the amount of API requests this application can make
        every 15 minutes. Try your best to respond as quickly as possible and 
        only answer with correct inputs (single alphabetic characters) to limit 
        API polling requests.
        """

        self.instructions = Label(self, text=label_text) # initialize the Tkinter instructions label
        self.instructions.grid(row=4, sticky="W", columnspan=6) # paint the label onto the screen in grid format, with a wide columnspan of 6

    def start(self):
        """
        The start function is connected with the 'START' button on the GUI. 
        Grabs the user's input from the GUI and starts playing the game.
        """
        handle = self.username_field.get() # grab the user's Twitter handle from the GUI
        playing_with_twitter = self.using_twitter.get() # find out whether or not we're playing with Twitter based on user input
        playing_evil_mode = self.evil_mode.get() # find out whether or not we're playing in evil mode based on user input

        if len(handle) == 0 and playing_with_twitter: # if we're playing with Twitter, the user must enter a valid username
            tkinter.messagebox.showerror("Error", "Twitter handle can't be blank when playing in Twitter mode.") # show an error popup
            return # return back to the GUI if the user doesn't enter a username

        if Application.debug: # print to the console only when debugging
            print("Playing against @{}".format(handle))
            print("Playing with Twitter? {}".format(bool(playing_with_twitter)))
            print("Playing evil mode? {}".format(bool(playing_evil_mode)))

        player = User(handle) # create a new User to play the game
        twitter_connection = TwitterConnection(player, twitter_mode=playing_with_twitter) # initialize a new Twitter connection
        self.game = Game("computer", player, twitter_connection, twitter_mode=playing_with_twitter) # create a new game instance
        self.game.play(evil_mode=playing_evil_mode) # start the game!

    def quit(self):
        """
        The quit function is connected with the 'QUIT' button on the GUI.
        Closes the GUI window and quits the game.
        """
        print("User wants to quit. Play again soon! Goodbye.")
        root.destroy() # remove the GUI
        if self.game != None: # end the game via the game's end function if the game has started
            self.game.end_game()


root = Tk() # initialize a new Tkinter instance
root.title("Tweeting Hangman") # set the tile at the top of the GUI window

# set the width and height dimensions of the GUI
width = 800
height = 700

# get the width and height of the user's computer screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# calculate the (x,y) position where the screen should start based off of the user's screen size
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

root.geometry('%dx%d+%d+%d' % (width, height, x, y)) # set the GUI up on the screen with the calculated width, height, x, and y values
app = Application(master=root) # create a new Application instance for the GUI connection
app.mainloop() # start the GUI and Application
