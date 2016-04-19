#!/bin/bash

# network_builder_pipeline.sh
#   Perform a pattern match analysis of Stable FC nodes

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./inputfiles$DATETIME
DATABASEDIR=./databases$DATETIME
OUTPUTDIR=./outputfiles$DATETIME

mkdir -p $INPUTDIR/networks/ $INPUTDIR/POs/ $DATABASEDIR/ $OUTPUTDIR/

DSGRN=/Users/bcummins/GIT/DSGRN
STARTINGFILE="$DSGRN/networks/7D_2016_04_05_yeastLEMoriginal_essential.txt" #11D_2016_04_18_malaria40hrDuke_90TF_essential.txt"
LEMFILE="datafiles/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt" #wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt"
RANKEDGENES="datafiles/haase-fpkm-p1_yeast_s29_DLxJTK_top25TFs.txt" #wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt"
NUMNODES=10 # add nodes of rank 1 to n singly and in pairs
NUMEDGES=10 # add edges of rank 1 to n singly and in pairs
TIMESERIES="datafiles/haase-fpkm-p1_yeast_s29.txt" #wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=85 #42 #cut after x time units (NOT after index x)
SCALING_FACTOR=0.00   # between 0 and 1; 0 = most restrictive partial order; 1 = least restrictive

python ./makeFilesForAnalysis.py $STARTINGFILE $LEMFILE $RANKEDGENES $NUMNODES $NUMEDGES $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTOR $INPUTDIR

SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

for NETWORK in $( ls $INPUTDIR/networks/*); do
	NUM=$(echo `basename $NETWORK` | sed -e s/[^0-9]//g);
	DATABASENAME="$DATABASEDIR/database$NUM.db";
	RESULTSFILE="$OUTPUTDIR/results$NUM.json"
	PARTIALORDERFILE="$INPUTDIR/POs/partialorder$NUM.json"

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

		# pattern match in stable FCs
		mpiexec -np 3 $PATTERNMATCH $NETWORK $PARTIALORDERFILE $OUTPUTDIR/StableFCList$NUM.txt $OUTPUTDIR/Matches$NUM.txt > /dev/null

		# yank summary results
		MATCHES=`cut -d " " -f 1 $OUTPUTDIR/Matches$NUM.txt | sort | uniq | wc -w`
		STABLEFCS=`cut -d " " -f 1 $OUTPUTDIR/StableFCList$NUM.txt | sort | uniq | wc -w`
		MULTISTABLE=`cut -d " " -f 1 $OUTPUTDIR/MultistabilityList$NUM.txt | sort | uniq | wc -w`
		NODES=`dsgrn network $NETWORK parameter | sed 's/[^0-9]*\([0-9]*\)[^0-9]*/\1/g'`
		# note: grep -o "[0-9]*" appears to be buggy on Mac OS X, hence the more complex sed expression instead

		# dump inputs and results to json
		python summaryJSON.py $NETWORK $PARTIALORDERFILE $MATCHES $STABLEFCS $MULTISTABLE $NODES $RESULTSFILE

		# delete intermediate files
		rm $NETWORK $DATABASENAME $PARTIALORDERFILE "$OUTPUTDIR/StableFCList$NUM.txt" "$OUTPUTDIR/MultistabilityList$NUM.txt" "$OUTPUTDIR/Matches$NUM.txt"
	fi
done


