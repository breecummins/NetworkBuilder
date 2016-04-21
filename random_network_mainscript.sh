#!/bin/bash

# analyze random networks

STARTINGFILE=$1 # network spec file: /Users/bcummins/GIT/DSGRN/networks/5D_2016_02_08_cancer_withRP_essential.txt
NUMNETWORKS=$2 # number of networks: 10000
MAXNODES=$3 # max number of nodes to allow (it is possible to choose too few nodes so that networks can never finish generating)
DSGRN=$4 #/Users/bcummins/GIT/DSGRN

SIGNATURES=$DSGRN/software/Signatures/bin/Signatures

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./random_networks$DATETIME
DATABASEDIR=./random_databases$DATETIME
OUTPUTDIR=./random_outputfiles$DATETIME

mkdir -p $DATABASEDIR/ $OUTPUTDIR/

python ./random_networkbuilder.py $STARTINGFILE $NUMNETWORKS "$INPUTDIR/network_"

# use xargs below since the number of files can be large
for NETWORK in $( echo $INPUTDIR/* | xargs ls ); do
	NUM=$(echo `basename $NETWORK` | sed -e s/[^0-9]//g);
	DATABASENAME="$DATABASEDIR/database$NUM.db";

	qsub random_network_helperscript.sh $SIGNATURES $i $DATABASENAME $OUTPUTDIR $NUM

done

