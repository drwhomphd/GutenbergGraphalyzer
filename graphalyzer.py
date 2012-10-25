#!/usr/bin/python
"""
     This file is part of Gutenberg Graphalyzer
     Gutenberg Graphalyzer is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     Gutenberg Graphalyzer is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with Gutenberg Graphalyzer.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
import networkx as nx
import argparse
from nltk.tokenize import *
import nltk

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
            dest="INPUT_FILE",
            default="test.txt")
    parser.add_argument('-g', '--graph',
            dest="GRAPH_FILE",
            default=False,
            help="Filename to save the GraphViz Graph to. Automatically appends .dot")
    parser.add_argument('-n', '--nltk',
            dest="NLTK",
            default=False,
            action="store_true")
    args = parser.parse_args()
    INPUT_FILE = args.INPUT_FILE
    GRAPH_FILE = args.GRAPH_FILE
    NLTK = args.NLTK

    graph = None

    if(NLTK):
        graph = nltk_parse(INPUT_FILE)
    else:
        graph = regexp_parse(INPUT_FILE)
    #END if

    # Print out a few metrics
    print("Degree Assortativity: " + str(nx.degree_assortativity_coefficient(graph)))
    print("Average Clustering Coefficient: " + str(nx.average_clustering(graph)))
    # This measure is taking a LONG time to calculate. Leaving out for now.
    #print("Average Shortest Path Length: " + str(nx.average_shortest_path_length(graph)))

    # Export the graph
    if(GRAPH_FILE):
        nx.write_dot(graph, GRAPH_FILE + ".dot")
#END main

def is_ascii(word):
    check_val = True
    try:
        word.decode('ascii')
    except UnicodeDecodeError:
        check_val = False
    
    return check_val
# END is_ascii

def nltk_parse(input_file):
    # Open lit file...
    input = open(input_file, 'r')
    word_graph = nx.Graph()
   
    # Make sure the nltk related files are downloaded
    nltk.download("punkt")
    
    # Collected count of each word
    word_dictionary = {}

    total_words = 0
    
    # Always holds the previous word seene
    previous_word = ""
   
    lines = input.read()

    # Tokenizing Sentences
    sentences = sent_tokenize(lines)
    for sentence in sentences:

        # Split the line in to individual words
        word_list = word_tokenize(sentence) 

        # Loop through each word
        for word in word_list:

            # Convert to lowercase
            word = word.lower()
            
            if is_ascii(word):
                word_graph.add_node(word)

                if (previous_word != ""):
                    # Add an edge between our current word and our
                    # previous word
                    word_graph.add_edge(previous_word, word)
        
                    # Get current bigram count
                    # Default value returned is 0 if it does not exist
                    curr_count = word_graph[previous_word][word].get('weight', 0) 

                    # Increment Count
                    curr_count = curr_count + 1

                    # Reset bigram count
                    word_graph[previous_word][word]['weight'] = curr_count
                # End if

                # Now that we no longer need the previous_word
                # set the current word to the previous word
                previous_word = word

                total_words = total_words + 1
            #END if

            # Dictionary output will be done later
            # Is word in dictionary yet?
                # Yes? Increment Count
                # No? Set Count to 1
        # END FOR

    #END FOR


    input.close()
    return word_graph

def regexp_parse(input_file):
    # Open lit file...
    input = open(input_file, 'r')
    word_graph = nx.Graph()

    # Collected count of each word
    word_dictionary = {}

    # Word count of the text
    total_words = 0

    # Always holds the previous word seen
    previous_word = ""

    line = input.readline()
    while (line != ""):

        # Split the line in to individual words
        word_list = re.split('\W+', line)

        # Loop through each word
        for word in word_list:


            # Skip the empties. 
            if  (word == ""):
                continue

            # Convert to lowercase
            word = word.lower()

            # Remove underline marks '_'
            word = word.strip('_')

            word_graph.add_node(word)

            if (previous_word != ""):
                # Add an edge between our current word and our
                # previous word
                word_graph.add_edge(previous_word, word)
    
                # Get current bigram count
                # Default value returned is 0 if it does not exist
                curr_count = word_graph[previous_word][word].get('weight', 0) 

                # Increment Count
                curr_count = curr_count + 1

                # Reset bigram count
                word_graph[previous_word][word]['weight'] = curr_count
            # End if

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

    input.close()

    return word_graph

if __name__ == "__main__":
    main();
