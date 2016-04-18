#!/bin/bash

# SAVEFILE=$1 #json
# OUTPUTDIR=$2 #where all the results files are

echo "[" >> $1

for i in $(ls $2/*); do
	cat $i >> $1;
	echo ',' >> $1;
done

echo "]" >> $1

# now delete stuff in OUTPUTDIR