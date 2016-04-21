#!/bin/bash
#Active comments for SGE
#$ -V
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -pe orte 8

# arg1 = path to Signatures
# arg2 = network file
# arg3 = database file
# arg4 = output directory
# arg5 = results number

# get unique identifier
NUM=$5

# make database
mpiexec --mca mpi_preconnect_mpi 1 -np $NSLOTS -x LD_LIBRARY_PATH $1 $2 $3

# if making the database fails, then quit
if [ ! -f $3 ]; then echo "Database $NUM did not compute\n"; cat $2; exit 1; fi 

# otherwise, analyze
# search for stable FCs
sqlite3 -separator " " $3 'select ParameterIndex, Vertex from Signatures natural join (select MorseGraphIndex,Vertex from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));' > $4/StableFCList$NUM.txt

# search for multistability
sqlite3 -separator " " $3 'select count(*) from Signatures natural join (select MorseGraphIndex from (select MorseGraphIndex, count(*) as numMinimal from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where numMinimal > 1);'  > $4/MultistabilityList$NUM.txt

# yank summary results
MATCHES="not searched"
STABLEFCS=`cut -d " " -f 1 $4/StableFCList$NUM.txt | sort | uniq | wc -w`
MULTISTABLE=`cut -d " " -f 1 $4/MultistabilityList$NUM.txt | sort | uniq | wc -w`
NODES=`dsgrn network $2 parameter | sed 's/[^0-9]*\([0-9]*\)[^0-9]*/\1/g'`
# note: grep -o "[0-9]*" appears to be buggy on Mac OS X, hence the more complex sed expression instead

# dump inputs and results to json
python summaryJSON.py $2 "None" $MATCHES $STABLEFCS $MULTISTABLE $NODES "$4/results$NUM.json"

# delete intermediate files
rm $2 $3 "$4/StableFCList$NUM.txt" "$4/MultistabilityList$NUM.txt"