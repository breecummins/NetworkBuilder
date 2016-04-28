#!/bin/bash

# analyze random networks

DSGRN=$1 #/Users/bcummins/GIT/DSGRN

SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./backward_inputfiles$DATETIME
DATABASEDIR=./backward_databases$DATETIME
OUTPUTDIR=./backward_outputfiles$DATETIME

mkdir $INPUTDIR/ $DATABASEDIR/ $OUTPUTDIR/

python ./backwardsAnastasia.py $INPUTDIR $DSGRN

for NETWORK in $( ls $INPUTDIR/network*); do
	NUM=$(echo `basename $NETWORK` | sed -e s/[^0-9]//g);
	DATABASENAME="$DATABASEDIR/database$NUM.db";
	RESULTSFILE="$OUTPUTDIR/results$NUM.json"
	qsub backwardsAnastasia_helperscript.sh $SIGNATURES $NETWORK $DATABASENAME $PATTERNMATCH "$INPUTDIR/pattern.json" $OUTPUTDIR $RESULTSFILE $NUM
done


