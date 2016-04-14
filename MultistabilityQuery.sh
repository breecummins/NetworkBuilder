#!/bin/bash
# MultistabilityQuery input_database output_file
#   "input_database" is the name of a DSGRN database
#   "output_file" is the name of the output file to be produced
#      It will hold a list of parameter index / Morse set index pairs
#      separated by newlines corresponding to Morse graphs with 
#      multiple minimal Morse sets.

sqlite3 -separator " " $1 'select count(*) from Signatures natural join (select MorseGraphIndex from (select MorseGraphIndex, count(*) as numMinimal from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where numMinimal > 1);' > $2
