#!/usr/bin/python3

import xml.etree.cElementTree as ET
import sqlite3
import glob
import re

# Given the rare usage of this script the parameters are hardcoded instead
# of taken from the command line.
CATALOG_FILE = "catalog.rdf"
#CATALOG_FILE = "catalogsample.rdf"
DATABASE_FILE = "catalog.db"
TEXTS_DIR = "/u/nhusted/nobackup/TEXTS-UNIQUE"

def main():

    file_list = glob.glob(TEXTS_DIR + "/*.txt") 
    bookid_to_filename = {}

    # Clean up the file list and create a dictionary that associates
    # ebook id's to their filenames. 
    for i in range(0, len(file_list)):
        t = file_list[i].split("/")
        file_list[i] = t[len(t)-1]

        id = file_list[i]

        for postfix in ["-0.txt", "-8.txt", ".txt"]:
            id = id.replace(postfix, "")

        bookid_to_filename[id] = file_list[i]

    # END for

    #print file_list
    # Get a parsed list of etext files. They should only
    # hae the specific etext number.

    tree = ET.parse(CATALOG_FILE)
    root = tree.getroot()

    # Parse the RDF files keeping in mind the list of etexts
    # to minimize the information in the database
    #parse_single_book_rdf(root, file_list)
    parse_catalog_rdf(root, bookid_to_filename, debug=False)

#END

"""
Created to parse the large catalog.rdf files from project gutenberg. They
contain "etext" and "file" tags for major tags. There are a few others, but
they did not look of interest (e.g. Description). Parsing the RDF
file also adds the final information to the database if debugging is off. 
"""
def parse_catalog_rdf(tree_root, ebook_list, debug=False):

    # Setup the sqlite connection here so the cursor can be passed
    # around to the various parse/insertion functions
    db_conn = sqlite3.connect(DATABASE_FILE)

    for child in tree_root:
        if(child.tag == "{http://www.gutenberg.org/rdfterms/}etext"):

            # We're skipping non-english texts because the eventual corpus targets
            # only english literature for now.
            language = child.find("{http://purl.org/dc/elements/1.1/}language/{http://purl.org/dc/terms/}ISO639-2/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value")

            # Sometimes the language field doesn't exist
            if (language is not None and language.text != "en"):
                print("Not English... skipping...")
                continue
            #END if

            # Information for DB
            etextID = ""
            title = ""
            author = []
            lccsubjects = []
            lcshsubjects = []
            publisher = ""
            downloads = ""
            copyright = ""
            filename = ""
            
            # This is the etext ID
            etextID = child.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}ID")
            # The etext portion needs to be parsed off
            etextID = etextID.replace("etext", "")

            # Find the proper filename based on the etextID. 
            filename = ebook_list.get(etextID, "")

            # If we haven't found the filename by this point, skip the rest of this loop
            # because we don't want to add the information to the database
            if(filename == ""):
                continue

            # Some books are missing the title field. One example had an empty friendly title.
            title_tag = child.find("{http://purl.org/dc/elements/1.1/}title")
            if(title_tag is not None):
                title = title_tag.text
            #END IF

            # Authors can be either single names under creator or multiple names in a list of
            # contributors.
            creator = child.find("{http://purl.org/dc/elements/1.1/}creator")
            contributors = child.findall("{http://purl.org/dc/elements/1.1/}contributor/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Bag/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li")
            for contributor in contributors:
                author.append(contributor.text)

            if (creator != None):
                author.append(creator.text)
            #End if

            publisher_name = child.find("{http://purl.org/dc/elements/1.1/}publisher")
            #publisher =  publisher_name.text.encode("utf-8")
            publisher =  publisher_name.text

            downloads = child.find("{http://www.gutenberg.org/rdfterms/}downloads/{http://www.w3.org/2001/XMLSchema#}nonNegativeInteger/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value").text


            # The full path for the LCSH elements is actually:
            #{http://purl.org/dc/terms/}subject
            #   {http://www.w3.org/1999/02/22-rdf-syntax-ns#}Bag
            #      {http://www.w3.org/1999/02/22-rdf-syntax-ns#}li
            #          {http://purl.org/dc/terms/}LCSH
            for subject in child.findall(".//{http://purl.org/dc/terms/}LCSH/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value"):
                #subjects.append(subject.text.encode("utf-8"))
                lcshsubjects.append(subject.text)
            for subject in child.findall(".//{http://purl.org/dc/terms/}LCC/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}value"):
                #subjects.append(subject.text.encode("utf-8"))
                lccsubjects.append(subject.text)

            # Print out information if we're debugging otherwise we add it to the database
            if(debug == True):
                print(etextID)
                print(filename)
                print(downloads)
                print(title)
                for name in author:
                    print(name)
                print(publisher)
                for subject in lcshsubjects:
                    print(subject)
                for subject in lccsubjects:
                    print(subject)
                print("---------------")
            else:
                # Add all relevant information to the database
                # The order of these three functions is IMPORTANT due to foreign key 
                # requirements. Must always be add_ebook_to_db first.
                add_ebook_to_db(db_conn, etextID, title, publisher, copyright, downloads, filename)
                add_author_to_db(db_conn, etextID, author)
                add_subject_to_db(db_conn, etextID, lccsubjects, lcshsubjects)
            #END IF
        else:
            print(("Unparsed tag: %s" % child.tag))
        #END IF
    #END FOR
    db_conn.commit()
    db_conn.close()

#END FUNCTION

"""
Parses the single book RDF files. They contain far more information than the
catalog equivalents. In this case detailed information about authors, file
types, and the etexts themselves.
"""
#def parse_single_book_rdf(tree_root, ebook_list):
#    #for ebook in root.findall("{http://www.gutenberg.org/2009/pgterms/}ebook"):
#    for child in tree_root:
#
##        print child.tag
##        print child.attrib
#
#        # We iterate through the children and switch over an ebook or agent
#        # because this means we only loop over all entries once instead of
#        # with the findall which potentially means we scan the document twice.
#        # Only used with single book rdf texts
#        if(child.tag == "{http://www.gutenberg.org/2009/pgterms/}ebook"):
#            # Get the ebook number
##            print child.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
#
#            # Get specific ebook information
#            for title in child.findall("{http://purl.org/dc/terms/}title"):
##                print title.text
#
#            # Get Copyright information
#            for marc260 in child.findall("{http://www.gutenberg.org/2009/pgterms/}marc260"):
##                print marc260.text
#
#
##            print "###"
#        elif(child.tag == "{http://www.gutenberg.org/2009/pgterms/}agent"):
#
#            for author_name in child.findall("{http://www.gutenberg.org/2009/pgterms/}name"):
##                print author_name.text
#
#        else: # Any other tags we don't care about
#            continue
# END
def add_ebook_to_db(dbc, ebookID, title, publisher, copyright, downloads, filename):

        dbc.execute("INSERT INTO ebooks VALUES (?,?,?,?,?)", (ebookID, title, copyright, downloads, filename))

#END FUNCTION
"""
The name field from the catalogue will have the author's birth and death
date. To safe space both the author is added to author details, if the
author doesn't currently exist, and then added to bookauthors.
"""
def add_author_to_db(dbc, ebookID, author_list):

    for author in author_list:
        # Place holder in case the author's aren't provided    
        first = ""
        last = ""
        birth = ""
        death = ""
       
        # We need to clean up the extra informationin the field
        pattern = re.compile("\[\w*\]")
        author = author.strip()
        author = pattern.sub("", author)

        # This splits it in to last name, firstname, and birth/death
        parts = author.split(",")

        if (len(parts) == 0):
            first = "Unknown"
            last = "Unknown"
        #END IF

        for i in range(0,len(parts)):
            # It's possible for there not to be a '-' and that an author's birth/death is just
            # given as a century. If that's the case, we set it as empty
            if("-" in parts[i]):
                life = parts[i].split('-')
                birth = life[0].strip()
                death = life[1].strip()
            else:
                # If it's the 0th element, it's a last name
                if (i == 0):
                    last = parts[i].strip()
                elif (i == 1): # If it's the 1st element, its a first name
                    first = parts[i].strip()
                else: # any other element is a title and we'll ignore it for now
                    continue
            #END IF
        #END FOR


        # Add the author to the author's database if they're not already there
        r = dbc.execute("SELECT authorID FROM authordetails WHERE first=? AND last=?", (first, last,))
        id = r.fetchone()

        # Add the author to the list of ebook ids and authors
        if (id is None):
            dbc.execute("INSERT INTO authordetails(first, last, birth, death) VALUES(?, ?, ?, ?)", (first, last, birth, death,))
            r = dbc.execute("SELECT authorID FROM authordetails WHERE first=? AND last=?", (first, last,))
            id = r.fetchone()
        #END IF

        dbc.execute("INSERT INTO bookauthors VALUES(?,?)", (ebookID, id[0],))
    #END FOR

    return

"""
The subject is added to subjectdetails, if it does not already exist,
and booksubjects at the same time to conserve space. 
"""
def add_subject_to_db(dbc, ebookID, lccsubject_list, lcshsubject_list):

    for subject in lccsubject_list:

        # Need to obtain the subject ID if it exists.
        r = dbc.execute("SELECT subjectID FROM lccsubjects WHERE subject=?", (subject,))
        id = r.fetchone()
        
        if (id is None):
            # If it doesn't exist we need to Insert the subject, get its id, then add it to the booksubjects
            dbc.execute("INSERT INTO lccsubjects(subject) VALUES (?)", (subject,))
            r = dbc.execute("SELECT subjectID FROM lccsubjects WHERE subject=?", (subject,))
            id = r.fetchone()
        # END IF
        
        dbc.execute("INSERT INTO lccmap VALUES(?,?)", (ebookID, id[0],))
    #END FOR
    
    for subject in lcshsubject_list:

        # Need to obtain the subject ID if it exists.
        r = dbc.execute("SELECT subjectID FROM lcshsubjects WHERE subject=?", (subject,))
        id = r.fetchone()
        
        if (id is None):
            # If it doesn't exist we need to Insert the subject, get its id, then add it to the booksubjects
            dbc.execute("INSERT INTO lcshsubjects(subject) VALUES (?)", (subject,))
            r = dbc.execute("SELECT subjectID FROM lcshsubjects WHERE subject=?", (subject,))
            id = r.fetchone()
        # END IF
        
        dbc.execute("INSERT INTO lcshmap VALUES(?,?)", (ebookID, id[0],))
    #END FOR

#END FUNCTION

if __name__ == "__main__":
    main()
