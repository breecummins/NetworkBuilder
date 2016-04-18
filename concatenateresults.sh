#!/bin/bash

SAVEFILE=$1
OUTPUTDIR=$2

echo "[" >> $SAVEFILE

for i in $(ls $OUTPUTDIR/*); do
	cat $i >> $SAVEFILE;
	echo ',' >> $SAVEFILE;
done

echo "]" >> $SAVEFILE

# now delete stuff in OUTPUTDIR