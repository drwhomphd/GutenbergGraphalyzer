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
from nltk.tokenize import *
import nltk
import re
import networkx as nx
import argparse
import math
import sys

"""
Vertex degree magnitude-based information content algorith.

Implemented based on Bonchev and Buck's "Quantitative measure of network complexity" paper.

I_{vd} = \sum{V}{i=1}{a_i log_2 a_i}


"""
def vector_degree_mag_info(graph):

    information_content = 0.0

    for n in graph.nodes():
        degree = graph.degree(n)

        information_content = information_content + (degree * (math.log(degree,2)))
    #END for


    return information_content

#End vertex_degree_mag_info


"""
The shannon entropy contained in a graph.

Implemented based on Bonchev and Buck's "Quantitative measure of network complexity" paper.
Specifically equation 15.

H(W) = W log_2 W - \sum{V}{i=1}{w_i log_2 w_i}

W is the sum of all edge weights.
w_i is the sum of each node's edge weights.

In the case of these graphs, the "weight" of an edge is he bigram count.

"""
def shannon_graph_entropy(graph):

    information_content = 0.0
    total_edge_weight = 0.0

    # Loop through each node
    for n in graph.nodes():
        
        node_weight = 0.0

        # Add up edge weights for each node
        for n0, n1, edata in graph.edges_iter(n, data=True):

            node_weight = node_weight + edata['weight']
            
            # Continue calculating the total edge weight for H_max
            total_edge_weight = total_edge_weight + edata['weight']
        #END for

        information_content = information_content + (node_weight * math.log(node_weight,2))
        
    #END for

    information_content = (total_edge_weight * math.log(total_edge_weight,2)) - information_content

    return information_content

#End shannon_graph_entropy

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
            action="store_true",
            help="Disable Regexp parsing and enable NLTK parsing.")
    parser.add_argument('-d', '--dir',
            dest="DIR",
            help="Provide a directory of text files to parse instead of an individual file.")            

    args = parser.parse_args()
    INPUT_FILE = args.INPUT_FILE
    GRAPH_FILE = args.GRAPH_FILE
    NLTK = args.NLTK
    DIR = args.DIR

    # The DIR and INPUT_FILE option cannot both be set
    if(DIR and INPUT_FILE):
        print("DIR and INPUT_FILE option are mutually exclusive.")
        sys.exit(-1)

    graph = None

    if(INPUT_FILE):
        if(NLTK):
            graph = nltk_parse(INPUT_FILE)
        else:
            graph = regexp_parse(INPUT_FILE)
        #END if

        print_metrics(graph)

        # Export the graph
        if(GRAPH_FILE):
            nx.write_dot(graph, GRAPH_FILE + ".dot")
        #END if
    #END if

    if(DIR):
        return
    #END IF
#END main
def print_metrics(graph):
        # Print out a few metrics
        
        # Degree assortativity
        print("DA:" + str(nx.degree_assortativity_coefficient(graph)))
        # Average Clustering Coefficient
        print("ACC:" + str(nx.average_clustering(graph)))
        # Information content of vector degree magnitudes
        print("Ivd:" + str(vector_degree_mag_info(graph)))
        # Shannon Graph Information based on edge weights, i.e., bigram counts
        print("SI:" + str(shannon_graph_entropy(graph)))

        # This measure is taking a LONG time to calculate. Leaving out for now.
        #print("Average Shortest Path Length: " + str(nx.average_shortest_path_length(graph)))
#END print_metrics

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

    """
        The \W+$ regexp will match all punctuation only word tokens.
        The \W+ regexp will match word tokens that also include apsotraphe's for shortening.

        A research assumption should be what to do with conjunctions... best to leave them in.
    """
    # Compile the regexp we use to detect punctuation
    punc_regexp = re.compile("\W+$")

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
            
            # Strip out _ characters used for bolding...
            word = word.strip('_')
          
            # Skip tokens that are just punctuation characters.
            if(re.match(punc_regexp, word) != None):
                continue

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
# End regexp_parse


if __name__ == "__main__":
    main();
