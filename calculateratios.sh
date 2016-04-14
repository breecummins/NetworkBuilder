#!/bin/bash
# 1st argument is db name
# 2nd argument is network spec file

. /share/data/bcummins/BooleanNetworks/BooleanNetworks/LEMScores/StableFCQuery.sh $1 ./StableFCList.txt 
STABLEFCS=`cut -d " " -f 1 StableFCList.txt | sort | uniq | wc -w`
NODES=`dsgrn network $2 parameter | sed 's/[^0-9]*\([0-9]*\)[^0-9]*/\1/g'`
echo $1 / $STABLEFCS / $NODES / `bc <<< "scale=2; $STABLEFCS/$NODES"`
