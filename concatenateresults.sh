#!/bin/bash

SAVEFILE=$1 #json
OUTPUTDIR=$2 #where all the results files are

echo "[" >> $SAVEFILE

for i in $(ls $OUTPUTDIR/*); do
	cat $i >> $SAVEFILE;
	echo ',' >> $SAVEFILE;
done

echo "]" >> $SAVEFILE

# now delete stuff in OUTPUTDIR