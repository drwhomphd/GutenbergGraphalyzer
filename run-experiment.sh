#!/bin/bash

DB_FILE="catalog.db"
TEXT_FILES=~/nobackup/TEXTS-UNIQUE/
#TEXT_FILES=./*.txt
PATH_TO_GRAPHALYZER="./"
#total=$(ls -l $TEXT_FILES | wc -l)
THREAD_COUNT=32

counter=0

find $TEXT_FILES/ -name '*.txt' -print | xargs -I CMD --max-procs=$THREAD_COUNT python $PATH_TO_GRAPHALYZER/graphalyzer.py -i CMD -o $DB_FILE

#for file in $TEXT_FILES
#do
#  let counter+=1
#  echo "$counter / $total"
#  python $PATH_TO_GRAPHALYZER/graphalyzer.py -i $file -o $DB_FILE > OUT.TXT
#done
