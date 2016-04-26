#!/bin/bash

# network_builder_pipeline_local.sh
#   Perform a pattern match analysis of Stable FC nodes

DATETIME=`date +%Y_%m_%d_%H_%M_%S`
INPUTDIR=./shuffledinputfiles$DATETIME
OUTPUTDIR=./shuffledoutputfiles$DATETIME
NETWORKFILE="/Users/bcummins/GIT/DSGRN/networks/11D_2016_04_18_malaria40hrDuke_90TF_essential.txt"
DATABASENAME="$OUTPUTDIR/11D_2016_04_18_malaria40hrDuke_90TF_essential.db"
RANKEDGENES="datafiles/wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt"
NUMTOPGENES=25
NUMSHUFFLES=150
TIMESERIES="datafiles/wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=42 #cut after x time units (NOT after index x)
SCALING_FACTORS=0.05   # list of 2 floats between 0 and 1; 0 = most restrictive partial order; 1 = least restrictive
DSGRN=/Users/bcummins/GIT/DSGRN
SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase

# make time stamped folders
mkdir -p $INPUTDIR/ $OUTPUTDIR/

# make all the patterns
python ./shuffledgenes.py $INPUTDIR $NETWORKFILE $RANKEDGENES $NUMTOPGENES $NUMSHUFFLES $TIMESERIES $TS_TYPE $TS_TRUNCATION $SCALING_FACTORS 

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

for PATTERNFILE in $( ls $INPUTDIR/*); do

	# make results file
	NUM=$(echo `basename $PATTERNFILE` | sed -e s/[^0-9]//g);
	RESULTSFILE="$OUTPUTDIR/results_$NUM.json"

	qsub shuffledgenes_helperscript.sh $PATTERNMATCH $NETWORKFILE $PATTERNFILE $OUTPUTDIR $NUM $STABLEFCS $MULTISTABLE $NODES $RESULTSFILE 
done


