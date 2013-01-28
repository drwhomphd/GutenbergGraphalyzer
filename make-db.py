#!/usr/bin/python

import xml.etree.cElementTree as ET

tree = ET.parse("sample_entry.rdf")

root = tree.getroot()

#for ebook in root.findall("{http://www.gutenberg.org/2009/pgterms/}ebook"):
for child in root:

    print child.tag
    print child.attrib

    # We iterate through the children and switch over an ebook or agent
    # because this means we only loop over all entries once instead of
    # with the findall which potentially means we scan the document twice.
    if(child.tag == "{http://www.gutenberg.org/2009/pgterms/}ebook"):
        # Get the ebook number
        print child.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']

        # Get specific ebook information
        for title in child.findall("{http://purl.org/dc/terms/}title"):
            print title.text

        # Get Copyright information
        for marc260 in child.findall("{http://www.gutenberg.org/2009/pgterms/}marc260"):
            print marc260.text


        print "###"
    elif(child.tag == "{http://www.gutenberg.org/2009/pgterms/}agent"):

        for author_name in child.findall("{http://www.gutenberg.org/2009/pgterms/}name"):
            print author_name.text

    else: # Any other tags we don't care about
        continue
    

