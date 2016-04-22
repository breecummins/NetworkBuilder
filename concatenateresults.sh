#!/bin/bash

SAVEFILE=$1 #json
OUTPUTDIR=$2 #temp results dir
INPUTDIR=$3 #temp network and partial order dir
DATABASEDIR=$4 #temp database dir
RESULTSSTARTNAME=$5 #beginning of results file name, 'results' for random networks using random_networkbuilder_helperscript.sh as of 04/22/2016


printf "[" > $SAVEFILE #write to file

for i in $(ls $OUTPUTDIR/RESULTSSTARTNAME*); do
	cat $i >> $SAVEFILE; #append to file
	printf ',' >> $SAVEFILE;
done

sed -i '$ s/.$/]/' $SAVEFILE #replace last comma with closing bracket

# check if SAVEFILE has the character '}', which indicates the presence of dictionaries
# if it does, delete
# but wait, this is an issue if you only want to concatenate partial results, should make deleting an input arg
if [ $( fgrep -o } $SAVEFILE | wc -l ) ]; then
	rm -r $OUTPUTDIR $INPUTDIR $DATABASEDIR
else
	echo "Concatenation failed."
fi

