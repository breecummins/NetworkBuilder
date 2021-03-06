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
StableFCList=$10

# pattern match in stable FCs pattern 1
mpiexec --mca mpi_preconnect_mpi 1 -np $NSLOTS -x LD_LIBRARY_PATH $PATTERNMATCH $NETWORKFILE $PATTERNFILE $StableFCList $OUTPUTDIR/Matches$NUM.txt > /dev/null

# yank summary results
MATCHES=`cut -d " " -f 1 $OUTPUTDIR/Matches$NUM.txt | sort | uniq | wc -w`

# dump inputs and results to json
python summaryJSON.py $NETWORKFILE $PATTERNFILE $MATCHES $STABLEFCS $MULTISTABLE $NODES $RESULTSFILE

# delete intermediate files
rm $PATTERNFILE "$OUTPUTDIR/Matches$NUM.txt" 
# rm $PATTERNFILE $NETWORKFILE "$OUTPUTDIR/Matches$NUM.txt" #need network file for subsequent pattern files
