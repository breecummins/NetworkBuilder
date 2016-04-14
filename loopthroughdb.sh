#!/bin/bash

cd /share/data/bcummins/DSGRN/software/Signatures/

for i in $( ls ./databases/ ); do
	NAME=${i%.*};
	. /share/data/bcummins/BooleanNetworks/BooleanNetworks/LEMScores/calculateratios.sh ./databases/$i ./networks/$NAME.txt;
done