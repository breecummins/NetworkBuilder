import ExtremaPO as EPO
import deterministicperturbations as dp
from databasecomputability import checkComputability
import sys,json

STARTINGFILE = sys.argv[1] 
LEMFILE = sys.argv[2] 
RANKEDGENES  = sys.argv[3] 
NUMNODES  = sys.argv[4] 
NUMEDGES = sys.argv[5] 
TIMESERIES  = sys.argv[6]  
TS_TYPE = sys.argv[7]  
TS_TRUNCATION  = sys.argv[8] 
SCALING_FACTORS = eval(sys.argv[9])
INPUTDIR = sys.argv[10]
MAXPARAMS = sys.argv[11]

with open(STARTINGFILE,'r') as sf:
    startingnetwork = sf.read()
networks = dp.runNetworkBuilder_OneAndTwo(startingnetwork,LEMFILE,RANKEDGENES,int(NUMNODES),int(NUMEDGES),is_new_node_essential=True,network_is_file=False)
networks = [startingnetwork] + networks
sizelimitednetworks = []
for network_spec in networks:
    if checkComputability(network_spec,MAXPARAMS):
        sizelimitednetworks.append(network_spec)
networks = sizelimitednetworks
genes = []
for network in networks:
    eqns = network.split('\n')
    try:
        eqns.remove("")
    except:
        pass
    genes.append(tuple([eqn.split()[0] for eqn in eqns]))
uniquegenes = list(set(genes))

# The following function call is slow. Needs to speed up if possible.
uniquePOs = []
for labels in uniquegenes:
    pos = []
    for sf in SCALING_FACTORS:
        pos.append(EPO.makeJSONstring(TIMESERIES,TS_TYPE,labels,float(TS_TRUNCATION),n=1,scalingFactor=float(sf),step=0.01))
    uniquePOs.append(pos)
# for po in uniquePOs:
#     print json.loads(po)["poset"]

matchingPOs = [uniquePOs[uniquegenes.index(g)] for g in genes]

for k,(net,po) in enumerate(zip(networks,matchingPOs)):
    with open(INPUTDIR+'/networks/network{}.txt'.format(k),'w') as nf:
        nf.write(net)
    with open(INPUTDIR+'/POs1/pattern{}.json'.format(k),'w') as pf:
        pf.write(po[0])
    with open(INPUTDIR+'/POs2/pattern{}.json'.format(k),'w') as pf:
        pf.write(po[1])

