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
# arg6 = dsgrn path

# get unique identifier
NUM=$5

# print file name in case the job has to be aborted
echo "Starting $2."

# make database
mpiexec --mca mpi_preconnect_mpi 1 -np $NSLOTS -x LD_LIBRARY_PATH $1 $2 $3

# if making the database fails, then quit
if [ ! -f $3 ]; then echo "Database $NUM did not compute\n"; cat $2; exit 1; fi 	

# otherwise, analyze
FPQUERY=$6/software/FPQuery/FPQuery

$FPQUERY $3 E2F 3 3 Rb 0 0 > "$4/stateP$NUM.txt"
$FPQUERY $3 E2F 0 0 Rb 1 1 > "$4/stateQ$NUM.txt"
$FPQUERY $3 E2F 0 0 Rb 1 1 E2F 3 3 Rb 0 0 > "$4/bistability$NUM.txt"

# yank summary results
MATCHES=-1
STABLEFCS=-1
MULTISTABLE=-1
STATEP=`cut -d " " -f 1 $4/stateP$NUM.txt | sort | uniq | wc -w`
STATEQ=`cut -d " " -f 1 $4/stateQ$NUM.txt | sort | uniq | wc -w`
BISTABILITY=`cut -d " " -f 1 $4/bistability$NUM.txt | sort | uniq | wc -w`
NODES=`dsgrn network $2 parameter | sed 's/[^0-9]*\([0-9]*\)[^0-9]*/\1/g'`
# note: grep -o "[0-9]*" appears to be buggy on Mac OS X, hence the more complex sed expression instead

# dump inputs and results to json
python summaryJSON_FPquery.py $2 "None" $MATCHES $STABLEFCS $MULTISTABLE $NODES $STATEP $STATEQ $BISTABILITY "$4/results$NUM.json"

# delete intermediate files
rm $2 $3 "$4/stateP$NUM.txt" "$4/stateQ$NUM.txt" "$4/bistability$NUM.txt"