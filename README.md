github: https://github.com/daltonboll/tweeting-hangman

Project Name: TweetingHangman
Author: Dalton Boll

--------------------------------------------------------------------------------------------------------
Short description:
TweetingHangman is a game with classic 'Hangman' rules. The user plays against 
a computer over Twitter, and can optionally play in 'evil' mode - a true test 
of one's word guessing abilities.

--------------------------------------------------------------------------------------------------------
Long description:
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
initiate the contact to the user-given Twitter handle (call it @user), asking @user to confirm 
their wish to play the game. If @user tweets back, then @TweetingHangman will begin the game. 
@TweetingHangman will tweet @user with a mystery word of the form '_ _ _ _ _...', and ask @user 
to guess a letter. @user tweets back one letter at a time, receiving acknowledgements via tweets 
from @TweetingHangman about whether or not the letter was found in the mystery word, or if @user 
ran out of guesses, etc. 

@user can request status updates from @TweetingHangman to see how many guesses @user has left, 
or to see which letters @user has already guessed. @user can also choose to end the game at 
any time by tweeting "end game" to @TweetingHangman. @TweetingHangman should also be able to
recognize if @user has stopped playing, and ping @user to see if they intend to keep on playing 
or not. If no response is received, then @TweetingHangman will end the game.

The 'evil' mode of TweetingHangman is a mode in which the computer player (@TweetingHangman) is 
extremely smart (or rather sneaky). @TweetingHangman will secretly switch the mystery word upon 
@user's guesses, making it almost impossible for @user to win the game. There's nothing like a 
little public Twitter humiliation for @user to get better at 'evil' TweetingHangman!

Currently, the game runs completely fine through the terminal with no tweeting implementation 
(it's just a regular game of Hangman right now). The next step is to develop the 'evil' mode, 
and finally to integrate tweeting through the Twitter API.

Start the game in the terminal by running 'python3 tweetingHangman.py'.

