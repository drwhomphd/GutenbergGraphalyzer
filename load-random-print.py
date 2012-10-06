#!/usr/bin/python

import re

input = open('test.txt', 'r')

word_dictionary = {}
total_words = 0

line = input.readline()
while (line != ""):

    # Split the line in to individual words
    word_list = re.split('\W+', line)

    # Loop through each word
    for word in word_list:

        # Skip the empties. 
        if  (word == ''):
            continue

        # Convert to lowercase
        word = word.lower()

        # Remove underline marks '_'
        word = word.strip('_')


        # Is word in dictionary yet?
            # Yes? Increment Count
            # No? Set Count to 1
    # END FOR

    line = input.readline()
#END WHILE
