#!/bin/bash

DB_FILE="catalog.db"
TEXT_FILES=~/nobackup/TEXTS-UNIQUE/*.txt
PATH_TO_GRAPHALYZER="./"

for file in $TEXT_FILES
do
  $("python $PATH_TO_GRAPHALYZER/graphalyzer.py -i $file -o $DB_FILE")
done
