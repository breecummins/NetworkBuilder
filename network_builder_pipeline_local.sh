#!/bin/bash

# network_builder_pipeline_local.sh
#   Perform a pattern match analysis of Stable FC nodes

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./inputfiles$DATETIME
DATABASEDIR=./databases$DATETIME
OUTPUTDIR=./outputfiles$DATETIME

mkdir -p $INPUTDIR/networks/ $INPUTDIR/POs1/ $INPUTDIR/POs2/ $DATABASEDIR/ $OUTPUTDIR/

DSGRN=/Users/bcummins/GIT/DSGRN
STARTINGFILE="$DSGRN/networks/5D_2016_04_23_wavepool_essential.txt" 
#STARTINGFILE="$DSGRN/networks/7D_2016_04_05_yeastLEMoriginal_essential.txt" #11D_2016_04_18_malaria40hrDuke_90TF_essential.txt"
LEMFILE="datafiles/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt" #wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt"
RANKEDGENES="datafiles/haase-fpkm-p1_yeast_s29_DLxJTK_top25TFs.txt" #wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt"
NUMNODES=10 # add nodes of rank 1 to n singly and in pairs
NUMEDGES=10 # add edges of rank 1 to n singly and in pairs
TIMESERIES="datafiles/haase-fpkm-p1_yeast_s29.txt" #wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=85 #42 #cut after x time units (NOT after index x)
SCALING_FACTORS='[0.00,0.05]'   # list of 2 floats between 0 and 1; 0 = most restrictive partial order; 1 = least restrictive
MAXPARAMS=25000

python ./makeFilesForAnalysis_sizelimited_multiplePO.py $STARTINGFILE $LEMFILE $RANKEDGENES $NUMNODES $NUMEDGES $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTORS $INPUTDIR $MAXPARAMS

SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

for NETWORK in $( ls $INPUTDIR/networks/*); do
	NUM=$(echo `basename $NETWORK` | sed -e s/[^0-9]//g);
	DATABASENAME="$DATABASEDIR/database$NUM.db";
	RESULTSFILE1="$OUTPUTDIR/results1_$NUM.json"
	RESULTSFILE2="$OUTPUTDIR/results2_$NUM.json"
	PATTERNFILE1="$INPUTDIR/POs1/pattern$NUM.json"
	PATTERNFILE2="$INPUTDIR/POs2/pattern$NUM.json"

	# make database
	mpiexec -np 3 $SIGNATURES $NETWORK $DATABASENAME

	# if making the database fails, then quit
	if [ ! -f $DATABASENAME ]; then 
		echo "Database $NUM did not compute\n"
		rm $NETWORK
	else
		# otherwise, analyze
		# search for stable FCs
		sqlite3 -separator " " $DATABASENAME 'select ParameterIndex, Vertex from Signatures natural join (select MorseGraphIndex,Vertex from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));' > $OUTPUTDIR/StableFCList$NUM.txt

		# search for multistability
		sqlite3 -separator " " $DATABASENAME 'select count(*) from Signatures natural join (select MorseGraphIndex from (select MorseGraphIndex, count(*) as numMinimal from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where numMinimal > 1);'  > $OUTPUTDIR/MultistabilityList$NUM.txt

		# pattern match in stable FCs pattern 1
		mpiexec -np 3 $PATTERNMATCH $NETWORK $PATTERNFILE1 $OUTPUTDIR/StableFCList$NUM.txt $OUTPUTDIR/Matches1_$NUM.txt > /dev/null

		# yank summary results
		MATCHES1=`cut -d " " -f 1 $OUTPUTDIR/Matches1_$NUM.txt | sort | uniq | wc -w`
		STABLEFCS=`cut -d " " -f 1 $OUTPUTDIR/StableFCList$NUM.txt | sort | uniq | wc -w`
		MULTISTABLE=`cat $OUTPUTDIR/MultistabilityList$NUM.txt  | tr -d "\n"`
		NODES=`dsgrn network $NETWORK parameter | sed 's/[^0-9]*\([0-9]*\)[^0-9]*/\1/g'`
		# note: grep -o "[0-9]*" appears to be buggy on Mac OS X, hence the more complex sed expression instead

		# dump inputs and results to json
		python summaryJSON.py $NETWORK $PATTERNFILE1 $MATCHES1 $STABLEFCS $MULTISTABLE $NODES $RESULTSFILE1

		# pattern match in stable FCs pattern 2
		mpiexec -np 3 $PATTERNMATCH $NETWORK $PATTERNFILE2 $OUTPUTDIR/StableFCList$NUM.txt $OUTPUTDIR/Matches2_$NUM.txt > /dev/null

		# yank summary results
		MATCHES2=`cut -d " " -f 1 $OUTPUTDIR/Matches2_$NUM.txt | sort | uniq | wc -w`

		# dump inputs and results to json
		python summaryJSON.py $NETWORK $PATTERNFILE2 $MATCHES2 $STABLEFCS $MULTISTABLE $NODES $RESULTSFILE2

		# delete intermediate files
		rm $NETWORK $DATABASENAME $PATTERNFILE1 $PATTERNFILE2 "$OUTPUTDIR/StableFCList$NUM.txt" "$OUTPUTDIR/MultistabilityList$NUM.txt" "$OUTPUTDIR/Matches1_$NUM.txt" "$OUTPUTDIR/Matches2_$NUM.txt"
	fi
done


