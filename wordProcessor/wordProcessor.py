MIN_LENGTH = 6
MAX_LENGTH = 8

print("Opening input file...")
input_file = open("Enwords.txt", "r")

print("Getting output file ready...")
output_file = open("words.txt", "w").close()
output_file = open("words.txt", "a") # clear the contents of the output file for a new session

total_words_found = 0

print("Processing started")
# Copy every word with length greater than MIN_LENGTH over to output file.
# NOTE: last line in file will be a blank '\n'
for word in input_file:
	word_length = len(word)
	if word_length >= MIN_LENGTH and word_length <= MAX_LENGTH:
		print(word, file=output_file, end="")
		total_words_found += 1

print("Removed all words less than {} and greater than {} characters in length.".format(MIN_LENGTH, MAX_LENGTH))
print("Total words found: {}.".format(total_words_found))

input_file.close()
output_file.close()

print("Input and output files closed.")