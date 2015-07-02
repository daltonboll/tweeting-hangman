"""
Author: Dalton Boll
GitHub: https://github.com/daltonboll/tweeting-hangman

wordProcessor is used to filter through a list of words. It prunes out words less than 
	a certain length and greater than a certain length. This is helpful for getting a 
	solid dictionary for the tweetingHangman program.

USAGE:
	- In 'Enwords.txt', separate each word you'd like to process by a new line, e.g:
		word1
		word2
		word3
		...
	- Set MIN_LENGTH to the minimum length of the words you want to filter through
	- Set MAX_LENGTH to the maximum length of the words you want to filter through
	- Run 'python3 wordProcessor.py' from this project's 'wordProcessor' directory
"""

MIN_LENGTH = 6 # the minimum length of the words you want
MAX_LENGTH = 8 # the maximum length of the words you want

print("Opening input file...")
input_file = open("Enwords.txt", "r") # open the file where the words are contained

print("Getting output file ready...")
output_file = open("words.txt", "w").close() # clear the contents of the output file for a new session
output_file = open("words.txt", "a") # open the output file for appending filtered words

total_words_found = 0 # the number of words we've found that match our filtering settings

print("Processing started")
# Copy every word with length greater than MIN_LENGTH and less than MAX_LENGTH over to output file
# NOTE: last line in file will be a blank '\n'
for word in input_file: # for each word in the file:
	word_length = len(word) # get the length of the word
	if word_length >= MIN_LENGTH and word_length <= MAX_LENGTH: # if the word length satisfies our parameters:
		print(word, file=output_file, end="") # add it to our output file
		total_words_found += 1 # increment the number of words found that satisfied our parameters

print("Removed all words less than {} and greater than {} characters in length.".format(MIN_LENGTH, MAX_LENGTH))
print("Total words found: {}.".format(total_words_found))

input_file.close() # close the input file
output_file.close() # close the output file

print("Input and output files closed.")