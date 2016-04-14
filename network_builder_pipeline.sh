# network_builder_pipeline.sh
#   Perform a pattern match analysis of Stable FC nodes

DSGRN=../../../../
SIGNATURES=$DSGRN/software/Signatures/bin/Signatures
STABLEFC=$DSGRN/software/PatternMatch/bin/StableFCQuery.sh

# add multistable query -- or maybe have a different script for this + stable FC query

PATTERNMATCH=$DSGRN/software/PatternMatch/bin/PatternMatchDatabase
mpiexec -np 9 $SIGNATURES ./network_spec.txt ./database.db > /dev/null

# catch if database not computed

$STABLEFC ./database.db ./StableFCList.txt > /dev/null

# add multistable query

mpiexec -np 9 $PATTERNMATCH ./network_spec.txt ./pattern_spec.json ./StableFCList.txt ./Matches.txt > /dev/null
MATCHES=`cut -d " " -f 1 Matches.txt | sort | uniq | wc -w`
STABLEFCS=`cut -d " " -f 1 StableFCList.txt | sort | uniq | wc -w`
NODES=`dsgrn network ./network_spec.txt parameter | sed 's/[^0-9]*\([0-9]*\)[^0-9]*/\1/g'`
# note: grep -o "[0-9]*" appears to be buggy on Mac OS X, hence the more complex sed expression instead

# write to json file
echo $MATCHES / $STABLEFCS / $NODES

