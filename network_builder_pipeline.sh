#!/bin/bash

# network_builder_pipeline.sh
#   Perform a pattern match analysis of Stable FC nodes

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./inputfiles$DATETIME
DATABASEDIR=./databases$DATETIME
OUTPUTDIR=./outputfiles$DATETIME

mkdir -p $INPUTDIR/networks/ $INPUTDIR/POs/ $DATABASEDIR/ $OUTPUTDIR/

DSGRN=/share/data/bcummins/DSGRN
STARTINGFILE="$DSGRN/networks/11D_2016_04_18_malaria40hrDuke_90TF_essential.txt"
LEMFILE="datafiles/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt" #wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt"
RANKEDGENES="datafiles/wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt" #wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt"
NUMNODES=10 # add nodes of rank 1 to n singly and in pairs
NUMEDGES=10 # add edges of rank 1 to n singly and in pairs
TIMESERIES="datafiles/wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=42 #cut after 42 time units (NOT after index 42)
SCALING_FACTOR=0.00   # between 0 and 1; 0 = most restrictive partial order; 1 = least restrictive

python ./makeFilesForAnalysis.py $STARTINGFILE $LEMFILE $RANKEDGENES $NUMNODES $NUMEDGES $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTOR $INPUTDIR

SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

for i in $( ls $INPUTDIR/networks/*); do
	NUM=$(echo `basename $i` | sed -e s/[^0-9]//g);
	DATABASENAME="$DATABASEDIR/database$NUM.db";
	RESULTSFILE="$OUTPUTDIR/results$NUM.json"
	qsub script_for_qsub.sh $SIGNATURES $i $DATABASENAME $PATTERNMATCH "$INPUTDIR/POs/partialorder$NUM.json" $OUTPUTDIR $RESULTSFILE $NUM
done


