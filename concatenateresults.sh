#!/bin/bash

SAVEFILE=$1 #json
OUTPUTDIR=$2 #where all the results files are

printf "[" >> $SAVEFILE

for i in $(ls $OUTPUTDIR/*); do
	cat $i >> $SAVEFILE;
	printf ',' >> $SAVEFILE;
done

printf '%s\n' '$' 's/.$/]/' wq | ex $SAVEFILE

# now delete stuff in OUTPUTDIR