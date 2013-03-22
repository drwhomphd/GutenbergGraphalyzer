# Gutenberg Graphalyzer

The Gutenberg Graphalyzer project aims to provide a means for measuring the structural complexity of works of literature. It's currently hard-coded to only support texts from the gutenberg project. 

## Tested Corpus
All results provided were based on a corpus created from Project Gutenberg's April 2010 DVD. A processed corpus collection can be found  [here](https://www.cs.Indiana.edu/~nhusted/project_source/pgdvd-en-corpus.tar.bz2)

## Further Documentation

Further documentation is located on my wiki [here](http://cgi.cs.indiana.edu/~nhusted/dokuwiki/doku.php?id=projects:graphalyzer). The documentation contained ont he project page will have some useful queries, issues with parsing, and other miscellaneous matter.

## Script Information

1. graphalyzer.py -- Parses an individual project gutenberg text. Assumes header and footer licensing is present. Run the script with '-h' for further information.

2. make-db-py3.py -- Creates the DB from a directory of project gutenberg text files and an RDF catalog file. Has three global "constants" that must be set for proper usage.

3. run-experiment.sh -- Runs the graphalyzer script after finding all text files from the corpus. Uses xargs to run the script in parallel. Thanks to the use of SQLite there are no race conditions as far as I have seen.

4. remove-duplicates.py -- Takes one command ine argument: the directory containing all the text files. Removes duplicate file types. Prefers ASCII over ISO and ISO over UTF-8.

5. result-analysis.r -- Generates a set of graphs from SQL queries to the results. Can be used as a guideline for future data exploration with R. Can easily be run from the command line with 'R CMD BATCH result-analysis.r'


## License Material
All research results, presentations, and documentation are Creative Commons 3.0 Attribution-NonCommercial. All source code is GPL V3.0

<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc/3.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">GutenbergGraphalyzer</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Nathaniel Husted</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/deed.en_US">Creative Commons Attribution-NonCommercial 3.0 Unported License</a>.
