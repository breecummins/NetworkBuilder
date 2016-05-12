import ExtremaPO as EPO
import os,json,sys

NETWORK_FILE = sys.argv[1] 
TIMESERIES_FILE  = sys.argv[2]  
TS_TYPE = sys.argv[3]  
TS_TRUNCATION  = float(sys.argv[4]) 
SCALING_FACTOR = float(sys.argv[5])
PATTERN_FILE = sys.argv[6]

with open(NETWORK_FILE,'r') as f:
    network = f.read()

eqns = network.split('\n')
try:
    eqns.remove("")
except:
    pass
genes=tuple([eqn.split()[0] for eqn in eqns])
pattern = EPO.makeJSONstring(TIMESERIES_FILE,TS_TYPE,genes,TS_TRUNCATION,n=1,scalingFactor=SCALING_FACTOR,step=0.01)

with open(PATTERN_FILE,'w') as pf:
    json.dump(pattern,pf)





