import json, sys

networkfile = sys.argv[1]
partialorderfile = sys.argv[2]
MATCHES=sys.argv[3]
STABLEFCS=sys.argv[4]
MULTISTABLE=sys.argv[5]
NODES=sys.argv[6]
outputfilename = sys.argv[7]

with open(networkfile,'r') as nf:
    networkstr = nf.read()
if partialorderfile != "None":
    with open(partialorderfile,'r') as pf:
        postr = pf.read()
else:
    postr = "None"

output = {"Network" : networkstr, "PartialOrder" : postr, "ParameterCount" : int(NODES), "StableFCParameterCount" : int(STABLEFCS), "MultistableParameterCount" : int(MULTISTABLE), "StableFCMatchesParameterCount" : int(MATCHES)}

json.dump(output,open(outputfilename,'w'))
