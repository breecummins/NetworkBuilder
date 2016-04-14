#!/bin/bash

cd /share/data/bcummins/DSGRN/software/Signatures/

for i in $( ls networks/ ); do
	qsub database_script2.sh ${i%.*};
done