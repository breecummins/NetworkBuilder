#!/bin/bash

# Perform a pattern match analysis of Stable FC nodes

DSGRN=$1 #/share/data/bcummins/DSGRN
NETWORKS=$2 #$DSGRN/networks/6D*Francis*
TIMESERIES=$3 #"datafiles/wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE=$4 #"row" or "col", type of time series file format
TS_TRUNCATION=$5 #42 #cut after 42 time units (NOT after index 42); -1 does not cut
SCALING_FACTOR=$6 #0.05   # between 0 and 1; 0 = most restrictive partial order; 1 = least restrictive


SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./inputfiles$DATETIME
DATABASEDIR=./databases$DATETIME
OUTPUTDIR=./outputfiles$DATETIME

mkdir -p $INPUTDIR/networks $INPUTDIR/patterns $DATABASEDIR/ $OUTPUTDIR/

for n in $( ls $NETWORKS ); do
	cp $n $INPUTDIR/networks/
	NETWORKFILE="$INPUTDIR/networks/$(basename $n)"
	BNAME=$(basename $n)
	NAME="${BNAME%.*}"
	PATTERNFILE="$INPUTDIR/patterns/$NAME_pattern.json"
	python makepattern.py $n $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTOR $PATTERNFILE # could add additional for loop for multiple scaling factors
	DATABASENAME="$DATABASEDIR/$NAME.db";
	RESULTSFILE="$OUTPUTDIR/results_$NAME.json"
	qsub script_for_qsub.sh $SIGNATURES $NETWORKFILE $DATABASENAME $PATTERNMATCH $PATTERNFILE $OUTPUTDIR $RESULTSFILE $NAME
done

