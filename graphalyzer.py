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
import math


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
w_i is the sum of 

"""
def shannon_graph_entropy(graph):

    information_content = 0.0
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
            default="test",
            help="Filename to save the GraphViz Graph to. Automatically appends .dot")
    args = parser.parse_args()
    INPUT_FILE = args.INPUT_FILE
    GRAPH_FILE = args.GRAPH_FILE



    # Open lit file...
    input = open(INPUT_FILE, 'r')

    # Collected count of each word
    word_dictionary = {}

    # Word count of the text
    total_words = 0

    graph = nx.Graph()

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

            graph.add_node(word)

            if (previous_word != ""):
                # Add an edge between our current word and our
                # previous word
                graph.add_edge(previous_word, word)
    
                # Get current bigram count
                # Default value returned is 0 if it does not exist
                curr_count = graph[previous_word][word].get('weight', 0) 

                # Increment Count
                curr_count = curr_count + 1

                # Reset bigram count
                graph[previous_word][word]['weight'] = curr_count
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

    # Print out a few metrics
    print("Degree Assortativity: " + str(nx.degree_assortativity_coefficient(graph)))
    print("Average Clustering Coefficient: " + str(nx.average_clustering(graph)))
    print(vector_degree_mag_info(graph))
    # This measure is taking a LONG time to calculate. Leaving out for now.
    #print("Average Shortest Path Length: " + str(nx.average_shortest_path_length(graph)))



    # Export the graph
    nx.write_dot(graph, GRAPH_FILE + ".dot")
#END main


if __name__ == "__main__":
    main();
