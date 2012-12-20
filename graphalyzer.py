#!/usr/bin/python
from __future__ import division
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
Average Edge Complexity
< a_i > = \frac{A}{V} = \frac{E_g}{V} = E_a

Redefines A = E = E_g = # of edges. This is different than traditional values of A in undirected graphs as
A is usually normalized to 2E (as undirected graph edges are shorthand for 1 input edge and 1 output edge).

Implemented based on Bonchev and Buck's "Quantitative measure of network complexity" paper.
"""
def average_edge_complexity(graph):

    return graph.number_of_edges() / graph.number_of_nodes()

#END average_edge_complexity

"""
Normalized Edge Complexity

Conn = \frac{A}{V^2} = \frac{E_g}{V^2} = E_n

Redefines A = E = E_g = # of edges. This is different than traditional values of A in undirected graphs as
A is usually normalized to 2E (as undirected graph edges are shorthand for 1 input edge and 1 output edge).

Implemented based on Bonchev and Buck's "Quantitative measure of network complexity" paper.
"""
def normalized_edge_complexity(graph):

    if(graph.number_of_selfloops() > 0):
        return graph.number_of_edges() / (graph.number_of_nodes() * graph.number_of_nodes())

    else:
        return graph.number_of_edges() / (graph.number_of_nodes() * (graph.number_of_nodes() - 1.0))
    #END if

#End normalized_edge_complexity


"""
Vertex degree magnitude-based information content algorith.

Implemented based on Bonchev and Buck's "Quantitative measure of network complexity" paper.

I_{vd} = \sum{V}{i=1}{a_i log_2 a_i}


"""
def vector_degree_mag_info(graph):

    information_content = 0.0

    for n in graph.nodes():
        degree = graph.out_degree(n)
        if degree > 0:
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
        for n0, n1, edata in graph.out_edges_iter(n, data=True):

            node_weight = node_weight + edata['weight']
            
            # Continue calculating the total edge weight for H_max
            total_edge_weight = total_edge_weight + edata['weight']
        #END for
        if node_weight > 0:
            information_content = information_content + (node_weight * math.log(node_weight,2))
        
    #END for

    information_content = (total_edge_weight * math.log(total_edge_weight,2)) - information_content

    return information_content

#End shannon_graph_entropy


"""
Calcualtes the Average number of out_edges for the graph.

\sum{i=1}{V}{a_i} / V
"""
def average_adjacency(graph):
    adj = 0.0

    for n in graph.nodes_iter():
        adj = adj + graph.out_degree(n)
    #END For

    return adj / graph.number_of_nodes()
#END average_adjacency

"""
Calculates the distance degree of a specific node. The Distance degree is the 
sum of the node's shortest paths to all other nodes in the graph.
"""
def distance_degree(graph, node):
    
    dist_degree = 0.0

    for n in graph.nodes_iter():
        dist_degree = dist_degree + nx.shortest_path_length(graph, source=node, target=n)
    #END for

    return dist_degree
#END distance_degree

"""
Complexity Index B

B = \sum{i=1}{V}{a_i / d_i}

Implemented based on Bonchev and Buck's "Quantitative measure of network complexity" paper.
"""
def complexity_index_B(graph):

    B = 0.0

    for n in graph.nodes_iter():
        B = B + (graph.out_degree(n) / distance_degree(graph, n))
    #END for

    return B

#End complexity_index_B

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
            default=True,
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

        # Pre-Computed Values Saved for Other Metrics
        ivd = vector_degree_mag_info(graph)
        si = shannon_graph_entropy(graph)
        
        # Takes too long
        #average_distance = nx.average_shortest_path_length(graph)
       
        # Print out metrics
        # Degree assortativity
        print("DA:" + str(nx.degree_assortativity_coefficient(graph)))
        # Information content of vector degree magnitudes
        print("Ivd:" + str(ivd))
        # Normalized Ivd over the number of nodes in the graph
        print("Ivdnorm:" + str((ivd/graph.number_of_nodes())))
        # Shannon Graph Information based on edge weights, i.e., bigram counts
        print("SI:" + str(si))
        print("SInorm:" + str(si / graph.number_of_nodes()))
        # Normalized Edge Complexity
        print("NEC:" + str(normalized_edge_complexity(graph)))
        # Average Edge Complexity
        print("AEC:" + str(average_edge_complexity(graph)))
        
        # Takes too long
        # Average Shortest Path
        # print("ASP:" + str(average_distance))
        # Takes too long
        # <A_i> / <D_i> = A / D
        # print("AD:" + str(average_adjacency(graph) / average_distance))
        # Takes too long
        # Complexity Index B
        # print("B:" + str(complexity_index_B(graph)))
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
    word_graph = nx.DiGraph()
   
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

        # Don't save previous words between sentences
        previous_word = ""

    #END FOR


    input.close()
    return word_graph
"""
Regular expression parsing provides a very rudimentary set of parsing for the text file.
It reads the file line by line and then splits each line based on one or more non-word 
characters. The problem with splitting on one or more non-word characters is, partially,
contractions will not be recorded, though the individual letters after them will become
nodes in the graph. This is not quite as specific as the NLTK parsing. The other major
difference is the regexp parsing has no recording of sentences, thus, stopping BiGrams
from being recorded across sentence boundries is not possible.
"""
def regexp_parse(input_file):
    # Open lit file...
    input = open(input_file, 'r')
    word_graph = nx.DiGraph()

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
