#!/bin/bash

SAVEFILE=$1 #json
OUTPUTDIR=$2 #temp results files
INPUTDIR=$3 #temp network files and partial orders
DATABASEDIR=$4 #temp databases


printf "[" > $SAVEFILE #write to file

for i in $(ls $OUTPUTDIR/*); do
	cat $i >> $SAVEFILE; #append to file
	printf ',' >> $SAVEFILE;
done

printf '%s\n' '$' 's/.$/]/' wq | ex $SAVEFILE #replace last comma with closing bracket

rm -r $OUTPUTDIR $INPUTDIR $DATABASEDIR