Project Name: TweetingHangman
Author: Dalton Boll
GitHub: https://github.com/daltonboll/tweeting-hangman

------------------------------------------------------------------------------------------------------------------
SHORT DESCRIPTION:

TweetingHangman is a game with classic 'Hangman' rules. The user plays against 
a computer over Twitter, and can optionally play in 'evil' mode - a true test 
of one's word guessing abilities.

------------------------------------------------------------------------------------------------------------------
LONG DESCRIPTION:

TweetingHangman is just like the popular 'Hangman' game, but with a twist. 
A human player gets to play against a computer over Twitter, tweeting guesses and 
actions back and forth. The computer can also be put into 'evil' mode, which 
makes it nearly impossible for the human player to win.

The goal of this project is to take a classic game and spice it up a little bit 
with modern technology. These days, tons of people have Twitter accounts. Why not 
leverage this use of people's time by making games over Twitter? 

The original idea for TweetingHangman was to allow anyone with a Twitter account to 
tweet a special set of characters at the TweetingHangman account (@TweetingHangman), 
which would initialize a game. However, this would require a script to be running that would 
constantly check to see if @TweetingHangman received any new game requests. This game 
would also be susceptible to spamming new game requests, which could overload the server that 
the backend code for the game would be running on.

So instead of an automated TweetingHangman game, this game seeks out to engage the user through 
a user interface, in which they can select the kind of game they'd like to play (regular or evil), 
enter in their Twitter handle, and start playing immediately over Twitter. @TweetingHangman will 
initiate the contact to the user-given Twitter handle (call it @user), asking @user to start 
playing the game with a guess. If @user tweets back, then @TweetingHangman will begin the game. 

@TweetingHangman will tweet @user with a mystery word of the form '_ _ _ _ _...', and ask @user 
to guess a letter. @user tweets back one letter at a time, receiving acknowledgements via tweets 
from @TweetingHangman about whether or not the letter was found in the mystery word, or if @user 
ran out of guesses, etc. 

@TweetingHangman will recognize if a user has stopped playing by frequently polling the Twitter
API. @TweetingHangman will also send an extra tweet trying to garner a response from @user, and, 
if no response is received yet again, the game will end.

EVIL MODE
The 'evil' mode of TweetingHangman is a mode in which the computer player (@TweetingHangman) is 
extremely smart (or rather sneaky). @TweetingHangman will secretly switch the mystery word upon 
@user's guesses, making it almost impossible for @user to win the game. There's nothing like a 
little public Twitter humiliation for @user to get better at 'evil' TweetingHangman!

TERMINAL MODE
The game can also be played through the terminal. This option gives the user the more classic version
of the Hangman game, and excludes Twitter completely from the game. 

------------------------------------------------------------------------------------------------------------------
USAGE:

	- 0.1 Make sure you have a valid set of Twitter developer API access keys located in the file 'keys'. This 
	    game will work with any account that has developer access, not just @TweetingHangman. For security 
	    reasons, @TweetingHangman's developer keys are not publicly included on GitHub. Your keys should be 
	    kept in the file 'keys' in the following format:

	    consumer_key = [INSERT YOUR CONSUMER KEY WITHOUT BRACKETS]
	    consumer_secret = [INSERT YOUR CONSUMER SECRET WITHOUT BRACKETS]
	    access_token = [INSERT YOUR ACCESS TOKEN WITHOUT BRACKETS]
	    access_token_secret = [INSERT YOUR ACCESS TOKEN SECRET WITHOUT BRACKETS]

	- 0.2 Make sure you have created a Twitter account if you'd like to play this game over Twitter (playing 
	    over the terminal without a Twitter account is also an option). 

	- 1. Start the game in the terminal by running 'python3 tweetingHangman.py' from the root project directory.

	- 2. A user interface will pop up. Enter in your Twitter username (without the '@') if you want to play over 
	   Twitter. If you want to play over the terminal, you can leave the username field blank. 

	- 3. Decide if you want to play over Twitter (3.1) or via the terminal (3.2).

		- 3.1. Select 'Play over Twitter' to play Hangman over Twitter.
			- 3.1.1. Select 'Normal Hangman Mode' to play the classic version of Hangman, or 'Evil Hangman Mode' 
			         to play the 'evil' version of Hangman.
			- 3.1.2. Navigate to https://twitter.com/i/notifications [log into your Twitter account if you aren't
			         already logged in]
	        - 3.1.3. Press the 'START' button to begin playing the game.
	        - 3.1.4. Go back to https://twitter.com/i/notifications and refresh the page until you see a tweet from 
	                 @TweetingHangman. Refreshing is necessary because the Twitter interface is sometimes slow at 
	                 dynamically updating automatically.
	        - 3.1.5. Click the reply button next to @TweetingHangman's tweet to start guessing! Please only use 
	                 single alphabetical characters, and don't hit the enter key on your keyboard. Just hit the 
	                 "Tweet" button once you've typed in your letter.
	        - 3.1.6. Continue refreshing the notifications page and replying to @TweetingHangman's tweets until 
	                 the game is over. Please don't spend too much time in between replies - the game must 
	                 continuously poll the Twitter API to see if you have sent a reply yet, and too much polling 
	                 will lock the game out of Twitter for 15 minutes.
	        - 3.1.7. Reply to @TweetingHangman with 'quit' (without quotes) at any time to quit the game. Note 
	                 that when playing over Twitter, clicking on the 'QUIT' button in the program interface 
	                 will cause the interface to freeze. This happens because of the way the Tkinter - which 
	                 powers the user interface - reacts to polling Twitter with time.sleep(). It's best to 
	                 tweet to quit or right click on the program and close it that way.

	    - 3.2. Select 'Play over the terminal' to play Hangman over the terminal.
			- 3.2.1. Select 'Normal Hangman Mode' to play the classic version of Hangman, or 'Evil Hangman Mode' 
			         to play the 'evil' version of Hangman.
	        - 3.2.2. Press the 'START' button to begin playing the game.
	        - 3.2.3. Switch from the program interface back to your terminal.
	        - 3.2.4. Type your response to the game through the terminal and hit enter on your keyboard to start 
	                 guessing! Please only use single alphabetical characters.
	        - 3.2.5. Continue responding to the game via the terminal until the game is over.
	        - 3.2.6. Type 'quit' (without quotes) into the terminal and hit enter at any time to quit the game. 
	                 You can also hit the 'QUIT' button in the program interface to quit the game since you 
	                 aren't playing over Twitter.

------------------------------------------------------------------------------------------------------------------
PROGRAM STRUCTURE:

This game consists of a few important files:

	- tweetingHangman.py: The 'brain' of the program. The game starts here as an Application class. The 
	  Application class also handles GUI painting from the Tkinter Python library. The Application class 
	  will create new Game, User, and TwitterConnection instances to run the game.

	- game.py: Home to the Game class. The Game handles all user input, output, and communication with the 
	  TwitterConnection class. General looping, calculations, and the loading of the game's dictionary 
	  happens here.

    - twitterConnection.py: This is where the communication with Twitter happens. Tweeting Hangman uses 
      the tweepy library to communicate with the Twitter API. Tweeting replies to the user and collecting 
      replies from the User happen here.

    - user.py: Contains the User class. A User instance serves as a simple function: a container for the 
      user's Twitter username/handle, without the '@'.

    - keys: This is where the Twitter developer API keys are kept (this file is absent on GitHub). See 
      section 0.1 of the 'USAGE' section above for more info.

Other miscellaneous files:

	- todo.txt: A place for me to keep my thoughts about future improvements I can make to the game.

	- wordProcessor [folder]
		- wordProcessor.py: This is a simple script that takes in a list of words (currently all words 
		  in the English dictionary, kept in Enwords.txt), and filters through them given certain 
		  parameters. The words that pass through the filter are placed into the file words.txt for 
		  use in the game. Currently, wordProcessor only filters by minimum and maximum word length.

		- Enwords.txt: A list of every word in the English language, with each word on a new line.

		- words.txt: A list of words that pass through the filtering process of the wordProcessor.

------------------------------------------------------------------------------------------------------------------
CURRENT PROBLEMS FACED:

	- Connecting to Twitter often reports errors, I generally have hardcoded the game to respond by shutting down 
	  (most of the time). This is because asking the user to handle the errors is usually infeasible. The most common reasons for these errors include:

	  	- The game has polled the API too many times in a 15 minute time period. This usually happens because 
	  	  it is necessary to frequently check and see if @user has responded to @TweetingHangman yet. The only 
	  	  way around this (that I've found so far) is to space out the time between polling, and therefore 
	  	  reducing the frequency of API calls. However, this creates some extra lag between when @user responds 
	  	  with a tweet and when @TweetingHangman responds back. In long games, where @user keeps making errors 
	  	  in their response (e.g. not tweeting single alphabetical characters), the polling limit will be 
	  	  reached faster. It's important to be precise and fast when playing over Twitter to avoid any lockouts
	  	  that prevent the game from running (the lockouts end after 15 minutes).

  	    - There is no connection to the Twitter server.

  	    - @user doesn't exist.

  	    - The Twitter server has an error.

  	    - There is a slow internet connection, which leads to too much polling between replies.

    - When playing in Twitter mode, frequent polling of the Twitter API takes place. This causes the GUI built 
      with the Tkinter library to freeze up, rendering it useless (especially concerning if the user wants to 
      use the 'QUIT' button). I believe there is a way around this by using special methods within the Tkinter
      library instead of time.sleep(), but more research needs to be done on this. Currently, the user has to 
      quit the game by more forceful means.

    - Distribution of the game can be an issue. This is because I can't publicly give out @TweetingHangman's 
      developer keys, so anyone who wants to play has to have their own developer keys, and manually place 
      them in the keys file.

  	- Because of the nature of the game, very similar (almost exact duplicate) tweets are sent by @TweetingHangman 
  	  to @user. Twitter blocks account access for (24?) hours if too many of a users tweets become duplicates, 
  	  however, their exact algorithm for this hasn't been revealed. In an effort to prevent this, I append a 
  	  randomized 3-character hash to the beginning of every tweet from @TweetingHangman. So far, it seems to 
  	  work well in combating the duplicate filter. However, it makes the user experience somewhat worse, because 
  	  random characters are displayed in every tweet.

------------------------------------------------------------------------------------------------------------------