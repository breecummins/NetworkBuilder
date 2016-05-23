#!/bin/bash

# analyze random networks

STARTINGFILE=$1 # network spec file: /Users/bcummins/GIT/DSGRN/networks/5D_2016_02_08_cancer_withRP_essential.txt
NUMNETWORKS=$2 # number of networks: 10000
MAXPARAMS=$3 # max number of parameters per network to allow (networks might not finish generating if this is too small)
DSGRN=$4 #/Users/bcummins/GIT/DSGRN
HELPERSCRIPT=$5 #random_network_helperscript.sh

SIGNATURES=$DSGRN/software/Signatures/bin/Signatures

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./random_networks$DATETIME
DATABASEDIR=./random_databases$DATETIME
OUTPUTDIR=./random_outputfiles$DATETIME

mkdir $INPUTDIR/

# mkdir -p $DATABASEDIR/ $OUTPUTDIR/ $INPUTDIR/

python ./random_networkbuilder.py $STARTINGFILE $NUMNETWORKS "$INPUTDIR/network_" $MAXPARAMS

# use xargs below since the number of files can be large
for NETWORK in $( echo $INPUTDIR/* | xargs ls ); do
	NUM=$(echo `basename $NETWORK` | sed -e s/[^0-9]//g);
	DATABASENAME="$DATABASEDIR/database$NUM.db";

	qsub $HELPERSCRIPT $SIGNATURES $NETWORK $DATABASENAME $OUTPUTDIR $NUM $DSGRN

done


