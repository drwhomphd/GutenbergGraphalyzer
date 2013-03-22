#!/usr/bin/python

""" 
*     This file is part of Gutenberg Graphalyzer
*     Gutenberg Graphalyzer is free software: you can redistribute it and/or modify
*     it under the terms of the GNU General Public License as published by
*     the Free Software Foundation, either version 3 of the License, or
*     (at your option) any later version.
*
*     Gutenberg Graphalyzer is distributed in the hope that it will be useful,
*     but WITHOUT ANY WARRANTY; without even the implied warranty of
*     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*     GNU General Public License for more details.
*
*     You should have received a copy of the GNU General Public License
*     along with Gutenberg Graphalyzer.  If not, see <http://www.gnu.org/licenses/>.

This script removes any duplicate etexts from a gutenberg repository. ASCII files delete ISO and UTF8 files. ISO files delete UTF8 files. UTF8 does
nothing. Execute from the directory where the text files are stored.

"""

import sys
import os
import glob

TARGET_DIR = sys.argv[1]

txt_files = glob.glob(TARGET_DIR + "/*.txt")

for file in txt_files:

    # Check or a '-'
    if '-' in file:
        # Split on '-'
        name = file.split('-')
        if name[1][0] is '0':
            # see if a -0 exists
            # If it exists, delete -8
            #print(TARGET_DIR + "/" + name[0] + "-8.txt")
            try:
                os.unlink(TARGET_DIR + "/" + name[0] + "-8.txt")
            except Exception:
                # Do nothing
                print(name[0] + "-8.txt Does not exist.")
        elif name[1][0] is '8':
            # see if a -8 exists
            # If it exists, don't do anything...
            True
        else:
            # This shouldn't exist
            print("Shouldn't Exist.")
            print name
    else:
        # Get rid of -0 and -8 if they exist.

        # Split on '.'
        name = file.split('.')
        try:
            # Delte the -8 and -0 files.

            #print(TARGET_DIR + "/" + name[1] + "-8.txt")
            os.unlink(TARGET_DIR + "/" + name[1] + "-8.txt")
            
            #print(TARGET_DIR + "/" + name[1] + "-0.txt")
            os.unlink(TARGET_DIR + "/" + name[1] + "-0.txt")
        except Exception:
            # Ignore
            True
    #End if
#end for
