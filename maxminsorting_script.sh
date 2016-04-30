#!/bin/bash

#   Perform a pattern match analysis of Stable FC nodes

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./maxmininputfiles$DATETIME
OUTPUTDIR=./maxminoutputfiles$DATETIME

DSGRN=/share/data/bcummins/DSGRN
SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase
NETWORKFILE="$DSGRN/networks/11D_2016_04_18_malaria40hrDuke_90TF_essential.txt"

DATABASENAME="$OUTPUTDIR/11D_2016_04_18_malaria40hrDuke_90TF_essential.db"
RANKEDGENES="datafiles/wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt"
TIMESERIES="datafiles/wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=42 #cut after x time units (NOT after index x)
SCALING_FACTORS="[0.05,0.10,0.15]"   # list of 2 floats between 0 and 1; 0 = most restrictive partial order; 1 = least restrictive

# make time stamped folders
mkdir -p $INPUTDIR/networks $INPUTDIR/patterns $OUTPUTDIR/

# make all the patterns
python ./maxminsorting.py $INPUTDIR $NETWORKFILE $RANKEDGENES $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTORS 

# make database
mpiexec --mca mpi_preconnect_mpi 1 -np 8 -x LD_LIBRARY_PATH $SIGNATURES $NETWORKFILE $DATABASENAME

# search for stable FCs
sqlite3 -separator " " $DATABASENAME 'select ParameterIndex, Vertex from Signatures natural join (select MorseGraphIndex,Vertex from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));' > $OUTPUTDIR/StableFCList.txt

# search for multistability
sqlite3 -separator " " $DATABASENAME 'select count(*) from Signatures natural join (select MorseGraphIndex from (select MorseGraphIndex, count(*) as numMinimal from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where numMinimal > 1);'  > $OUTPUTDIR/MultistabilityList.txt

# get totals
STABLEFCS=`cut -d " " -f 1 $OUTPUTDIR/StableFCList.txt | sort | uniq | wc -w`
MULTISTABLE=`cat $OUTPUTDIR/MultistabilityList.txt  | tr -d "\n"`
NODES=`dsgrn network $NETWORKFILE parameter | sed 's/[^0-9]*\([0-9]*\)[^0-9]*/\1/g'` # note: grep -o "[0-9]*" appears to be buggy on Mac OS X, hence the more complex sed expression instead

for NETWORK in $( ls $INPUTDIR/networks/*); do

	# make results file
	NUM=$(echo `basename $NETWORK` | sed -e s/[^0-9,_,-]//g);
	RESULTSFILE="$OUTPUTDIR/results$NUM.json"
	PATTERNFILE="$INPUTDIR/patterns/pattern$NUM.json"

	qsub maxminsorting_helperscript.sh $PATTERNMATCH $NETWORK $PATTERNFILE $OUTPUTDIR $NUM $STABLEFCS $MULTISTABLE $NODES $RESULTSFILE 
done


