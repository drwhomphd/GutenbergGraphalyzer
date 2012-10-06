#!/usr/bin/python

import re
import networkx as nx

input = open('test.txt', 'r')

# Collected count of each word
word_dictionary = {}

# Word count of the text
total_words = 0

graph = nx.Graph()

# Always holds the previous word seen
previous_word = ''

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

        graph.add_node(word)

        # Add an edge between our current word and our
        # previous word
        graph.add_edge(previous_word, word)

        # Get current bigram count
        # Default value returned is 0 if it does not exist
        curr_count = graph[previous_word][word].get('count', 0) 
        
        # Increment Count
        curr_count = curr_count + 1

        # Reset bigram count
        graph[previous_word][word]['count'] = curr_count

        # Now that we no longer need the previous_word
        # set the current word to the previous word
        previous_word = word

        total_words = total_words + 1
        
        # Dictionary output will be done later
        # Is word in dictionary yet?
            # Yes? Increment Count
            # No? Set Count to 1
    # END FOR

    line = input.readline()
#END WHILE

print total_words
print len(graph.nodes())
print len(graph.edges())
