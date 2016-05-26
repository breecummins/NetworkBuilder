#!/bin/bash

# analyze Francis networks

NETWORKDIR=$1 # location of network isomorphisms
MAPPINGDIR=$2 # location of gene mappings associated to each isomorphism
DSGRN=$3 #/Users/bcummins/GIT/DSGRN
HELPERSCRIPT=$4 #shuffledgenes_helperscript.sh
NETWORKBUILDER=$5 #Francis_networkbuilder.py
TIMESERIES=$6 #datafiles/wrair2015_v2_fpkm-p1_s19.tsv  
TS_TYPE=$7 #'row' 
TS_TRUNCATION=$8 #42 
SCALING_FACTORS=$9 #[0.0,0.05,0.1,0.15]

SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./Francis$DATETIME/networks
PATTERNDIR=./Francis$DATETIME/patterns
DATABASEDIR=./Francis$DATETIME/databases
OUTPUTDIR=./Francis$DATETIME/results

mkdir -p $INPUTDIR/ $PATTERNDIR/ $DATABASEDIR/ $OUTPUTDIR/

python $NETWORKBUILDER $NETWORKDIR $MAPPINGDIR $INPUTDIR $PATTERNDIR $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTORS

# use xargs since the number of files can be large
RUNIDPREV=""
for NETWORKFILE in $( echo $INPUTDIR/* | xargs ls ); do
	BNAME=`basename $NETWORKFILE`
	RUNID=${BNAME%%_*}

	if [[ "$RUNID" != "$RUNIDPREV" ]]; then
		# only run database if it hasn't been done for this network isomorphism
		DATABASENAME="$DATABASEDIR/database$RUNID.db";

		# make database
		mpiexec --mca mpi_preconnect_mpi 1 -np 8 -x LD_LIBRARY_PATH $SIGNATURES $NETWORKFILE $DATABASENAME

		# search for stable FCs
		sqlite3 -separator " " $DATABASENAME 'select ParameterIndex, Vertex from Signatures natural join (select MorseGraphIndex,Vertex from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));' > $OUTPUTDIR/StableFCList$RUNID.txt

		# search for multistability
		sqlite3 -separator " " $DATABASENAME 'select count(*) from Signatures natural join (select MorseGraphIndex from (select MorseGraphIndex, count(*) as numMinimal from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where numMinimal > 1);'  > $OUTPUTDIR/MultistabilityList$RUNID.txt

		# get totals
		STABLEFCS=`cut -d " " -f 1 $OUTPUTDIR/StableFCList$RUNID.txt | sort | uniq | wc -w`
		MULTISTABLE=`cat $OUTPUTDIR/MultistabilityList$RUNID.txt  | tr -d "\n"`
		NODES=`dsgrn network $NETWORKFILE parameter | sed 's/[^0-9]*\([0-9]*\)[^0-9]*/\1/g'` # note: grep -o "[0-9]*" appears to be buggy on Mac OS X, hence the more complex sed expression instead

		# remove intermediate files
		rm "$OUTPUTDIR/StableFCList$RUNID.txt" "$OUTPUTDIR/MultistabilityList$RUNID.txt" "$DATABASEDIR/database$RUNID.db"

		RUNIDPREV=$RUNID
	fi

	NETID=${BNAME%%.*}
	NETID=${NETID##network}
	echo $NETID

	for PATTERNFILE in $( echo $PATTERNDIR/$NETID/* | xargs ls ); do
		NUM="$NETID_${PATTERNFILE##pattern}"
		NUM=${NUM%%.*}
		RESULTSFILE="$OUTPUTDIR/results$NUM.json"
		qsub $HELPERSCRIPT $PATTERNMATCH $NETWORKFILE $PATTERNFILE $OUTPUTDIR $NUM $STABLEFCS $MULTISTABLE $NODES $RESULTSFILE
	done

done