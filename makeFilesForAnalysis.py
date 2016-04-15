import ExtremaPO as EPO
import deterministicperturbations as dp
import sys

STARTINGFILE = sys.argv[1] 
LEMFILE = sys.argv[2] 
RANKEDGENES  = sys.argv[3] 
NUMNODES  = sys.argv[4] 
NUMEDGES = sys.argv[5] 
TIMESERIES  = sys.argv[6]  
TS_TYPE = sys.argv[7]  
TS_TRUNCATION  = sys.argv[8] 

networks = dp.runNetworkBuilder_OneAndTwo(STARTINGFILE,LEMFILE,RANKEDGENES,int(NUMNODES),int(NUMEDGES),is_new_node_essential=True)
genes = []
for network in networks:
    if network:
        genes.append(tuple([eqn.split()[0] for eqn in network]))
uniquegenes = list(set(genes))
uniquePOs = []
for labels in uniquegenes:
    uniquePOs.append(EPO.makeJSONstring(TIMESERIES,TS_TYPE,labels,TS_TRUNCATION,n=1,scalingFactor=1,step=0.01))
matchingPOs = [uniquePOs[uniquegenes.index(g)] for g in genes]

for k,(net,po) in enumerate(zip(networks,matchingPOs)):
    with open('inputfiles/networks/network{}.txt'.format(k),'w') as nf:
        nf.write(net)
    with open('inputfiles/POs/partialorder{}.json'.format(k),'w') as pf:
        pf.write(po)

