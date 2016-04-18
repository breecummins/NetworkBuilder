#!/bin/bash

SAVEFILE=$1 #json
OUTPUTDIR=$2 #where all the results files are

printf "[" > $SAVEFILE #write to file

for i in $(ls $OUTPUTDIR/*); do
	cat $i >> $SAVEFILE; #append to file
	printf ',' >> $SAVEFILE;
done

printf '%s\n' '$' 's/.$/]/' wq | ex $SAVEFILE #replace last comma with closing bracket

# now delete stuff in OUTPUTDIR