#!/usr/bin/python

import xml.etree.cElementTree as ET

def main():
    tree = ET.parse("catalog.rdf")
    #tree = ET.parse("catalogsample.rdf")

    root = tree.getroot()

    #parse_single_book_rdf(root)
    parse_catalog_rdf(root)

#END

"""
Created to parse the large catalog.rdf files from project gutenberg. They
contain "etext" and "file" tags for major tags. There are a few others, but
they did not look of interest (e.g. Description)
"""
def parse_catalog_rdf(tree_root):
    for child in tree_root:
        if(child.tag == "{http://www.gutenberg.org/rdfterms/}etext"):

            # We're skipping non-english texts because the eventual corpus targets
            # only english literature for now.
            language = child.find("{http://purl.org/dc/elements/1.1/}language/{http://purl.org/dc/terms/}ISO639-2/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value")

            # Sometimes the language field doesn't exist
            if (language is not None and language.text != "en"):
                print "Not English... skipping..."
                continue
            #END if
            
            # This is the etext ID
            print child.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}ID")

            title = ""
            title_tag = child.find("{http://purl.org/dc/elements/1.1/}title")

            # Some books are missing the title field. One example had an empty friendly title.
            if(title_tag is None):
                title = ""
            else:
                title = title_tag.text.encode("utf-8")

            # Authors can be either single names under creator or multiple names in a list of
            # contributors.
            creator = child.find("{http://purl.org/dc/elements/1.1/}creator")
            author = [];
            if (creator == None):
               contributors = child.findall("{http://purl.org/dc/elements/1.1/}contributor/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Bag/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li")
               for contributor in contributors:
                   author.append(contributor.text.encode("utf-8"))
            else:
                author.append(creator.text.encode("utf-8"))
            #End if

            publisher = child.find("{http://purl.org/dc/elements/1.1/}publisher")

            print publisher.text.encode("utf-8")
            for name in author:
                print name

            # The full path for the LCSH elements is actually:
            #{http://purl.org/dc/terms/}subject
            #   {http://www.w3.org/1999/02/22-rdf-syntax-ns#}Bag
            #      {http://www.w3.org/1999/02/22-rdf-syntax-ns#}li
            #          {http://purl.org/dc/terms/}LCSH
            for subject in child.findall(".//{http://purl.org/dc/terms/}LCSH/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value"):
                print subject.text.encode("utf-8")
            for subject in child.findall(".//{http://purl.org/dc/terms/}LCC/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value"):
                print subject.text.encode("utf-8")

            print "---------------"
        else:
            print("Unparsed tag: %s" % child.tag)
        #END IF
    #END FOR


"""
Parses the single book RDF files. They contain far more information than the
catalog equivalents. In this case detailed information about authors, file types,
and the etexts themselves.
"""
def parse_single_book_rdf(tree_root):
    #for ebook in root.findall("{http://www.gutenberg.org/2009/pgterms/}ebook"):
    for child in tree_root:

        print child.tag
        print child.attrib

        # We iterate through the children and switch over an ebook or agent
        # because this means we only loop over all entries once instead of
        # with the findall which potentially means we scan the document twice.
        
        # Only used with single book rdf texts
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
# END

if __name__ == "__main__":
    main()
