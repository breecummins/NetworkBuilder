#!/bin/bash

# network_builder_pipeline.sh
#   Perform a pattern match analysis of Stable FC nodes

mkdir -p ./inputfiles/networks/ ./inputfiles/POs/ ./databases/ ./outputfiles/
rm ./inputfiles/networks/* ./inputfiles/POs/* ./databases/* ./outputfiles/*

STARTINGFILE="datafiles/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential.txt"
LEMFILE="datafiles/wrair2015_v2_fpkm-p1_s19_50tfs_top25_dljtk_lem_score_table.txt"
RANKEDGENES="datafiles/wrair-fpkm-p1_malaria_s19_DLxJTK_50putativeTFs.txt"
NUMNODES=2 # add nodes of rank 1 to n singly and in pairs
NUMEDGES=2 # add edges of rank 1 to n singly and in pairs
TIMESERIES="datafiles/wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=42 #cut after 42 time units (NOT after index 42)
SCALING_FACTOR=0.01   # between 0 and 1; 0 = most restrictive partial order; 1 = least restrictive

python ./makeFilesForAnalysis.py $STARTINGFILE $LEMFILE $RANKEDGENES $NUMNODES $NUMEDGES $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTOR

# DSGRN=/share/data/bcummins/DSGRN
# SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
# PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

# for i in $( ls inputfiles/networks/*); do
# 	NUM=$(echo $i | sed -e s/[^0-9]//g);
# 	DATABASENAME="./databases/database$NUM.db";
# 	qsub script_for_qsub.sh $SIGNATURES $i $DATABASENAME $PATTERNMATCH "./inputfiles/POs/partialorder$NUM.json"
# done


