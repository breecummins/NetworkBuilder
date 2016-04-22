#!/bin/bash

SAVEFILE=$1 #json
OUTPUTDIR=$2 #temp results dir
RESULTSSTARTNAME=$3 #beginning of results file name, 'results' for random networks using random_networkbuilder_helperscript.sh as of 04/22/2016


printf "[" > $SAVEFILE #write to file

for i in $(ls $OUTPUTDIR/RESULTSSTARTNAME*); do
	cat $i >> $SAVEFILE; #append to file
	printf ',' >> $SAVEFILE;
done

sed -i '$ s/.$/]/' $SAVEFILE #replace last comma with closing bracket
