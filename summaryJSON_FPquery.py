import json, sys

network_spec_file = sys.argv[1]
pattern_spec_file = sys.argv[2]
MATCHES=sys.argv[3]
STABLEFCS=sys.argv[4]
MULTISTABLE=sys.argv[5]
NODES=sys.argv[6]
STATEP=sys.argv[7]
STATEQ=sys.argv[8]
BISTABLE=sys.argv[9]
outputfilename = sys.argv[10]

with open(network_spec_file,'r') as nf:
    networkstr = nf.read()
if pattern_spec_file != "None":
    with open(pattern_spec_file,'r') as pf:
        postr = json.load(pf)
else:
    postr = "None"

output = {"Network" : networkstr, "PatternSpecification" : postr, "ParameterCount" : int(NODES), "StableFCParameterCount" : int(STABLEFCS), "MultistableParameterCount" : int(MULTISTABLE), "StableFCMatchesParameterCount" : int(MATCHES), "StateP" : int(STATEP), "StateQ" : int(STATEQ), "BistablePQ" : int(BISTABLE)}

json.dump(output,open(outputfilename,'w'))
