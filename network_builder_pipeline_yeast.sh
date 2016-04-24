#!/bin/bash

# network_builder_pipeline.sh
#   Perform a pattern match analysis of Stable FC nodes

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./inputfiles$DATETIME
DATABASEDIR=./databases$DATETIME
OUTPUTDIR=./outputfiles$DATETIME

mkdir -p $INPUTDIR/networks/ $INPUTDIR/POs/ $DATABASEDIR/ $OUTPUTDIR/

DSGRN=/share/data/bcummins/DSGRN
STARTINGFILE="$DSGRN/networks/5D_2016_04_23_wavepool_essential.txt" 
LEMFILE="datafiles/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt" 
RANKEDGENES="datafiles/haase-fpkm-p1_yeast_s29_DLxJTK_top25TFs.txt" 
NUMNODES=10 # add nodes of rank 1 to n singly and in pairs
NUMEDGES=10 # add edges of rank 1 to n singly and in pairs
MAXPARAMS=200000 # maximum parameters allowed per network
TIMESERIES="datafiles/haase-fpkm-p1_yeast_s29.txt"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=85 #cut after 42 time units (NOT after index 42)
SCALING_FACTOR=0.05   # between 0 and 1; 0 = most restrictive partial order; 1 = least restrictive

python ./makeFilesForAnalysis.py $STARTINGFILE $LEMFILE $RANKEDGENES $NUMNODES $NUMEDGES $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTOR $INPUTDIR $MAXPARAMS

SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

for i in $( ls $INPUTDIR/networks/*); do
	NUM=$(echo `basename $i` | sed -e s/[^0-9]//g);
	DATABASENAME="$DATABASEDIR/database$NUM.db";
	RESULTSFILE="$OUTPUTDIR/results$NUM.json"
	qsub script_for_qsub.sh $SIGNATURES $i $DATABASENAME $PATTERNMATCH "$INPUTDIR/POs/partialorder$NUM.json" $OUTPUTDIR $RESULTSFILE $NUM
done


