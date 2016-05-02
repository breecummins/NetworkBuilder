#!/bin/bash
#Active comments for SGE
#$ -V
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -pe orte 32

PATTERNMATCH=$1
NETWORKFILE=$2
PATTERNFILE=$3
OUTPUTDIR=$4
NUM=$5
STABLEFCS=$6
MULTISTABLE=$7
NODES=$8
RESULTSFILE=$9


# pattern match in stable FCs
mpiexec --mca mpi_preconnect_mpi 1 -np $NSLOTS -x LD_LIBRARY_PATH $PATTERNMATCH $NETWORKFILE $PATTERNFILE $OUTPUTDIR/StableFCList.txt $OUTPUTDIR/Matches_$NUM.txt > /dev/null

# yank summary results
MATCHES=`cut -d " " -f 1 $OUTPUTDIR/Matches_$NUM.txt | sort | uniq | wc -w`

# dump inputs and results to json
python summaryJSON.py $NETWORKFILE $PATTERNFILE $MATCHES $STABLEFCS $MULTISTABLE $NODES $RESULTSFILE

# delete intermediate files
 # rm $PATTERNFILE $NETWORKFILE "$OUTPUTDIR/Matches_$NUM.txt" 
