#!/bin/bash

cd /share/data/bcummins/DSGRN/software/Signatures/

for i in $( ls ./databases/ ); do
	cp ./databases/$i /share/data/CHoMP/Projects/DSGRN/DB/data/;
done

DATE=`date +%Y_%m_%d_H%H_M%M_S%S`

mkdir $DATE
mv ./databases/ $DATE
mv ./networks/ $DATE

tar -cvzf $DATE.tar.gz $DATE

