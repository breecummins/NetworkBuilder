#!/bin/bash

FILENAME=$1

echo "[" >> $FILENAME

for i in $(ls outputfiles/results*.txt); do
	cat $i >> $FILENAME;
	echo ',' >> $FILENAME;
done

echo "]" >> $FILENAME