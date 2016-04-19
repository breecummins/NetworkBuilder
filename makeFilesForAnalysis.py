import ExtremaPO as EPO
import deterministicperturbations as dp
import sys,json

STARTINGFILE = sys.argv[1] 
LEMFILE = sys.argv[2] 
RANKEDGENES  = sys.argv[3] 
NUMNODES  = sys.argv[4] 
NUMEDGES = sys.argv[5] 
TIMESERIES  = sys.argv[6]  
TS_TYPE = sys.argv[7]  
TS_TRUNCATION  = sys.argv[8] 
SCALING_FACTOR = sys.argv[9]
INPUTDIR = sys.argv[10]

with open(STARTINGFILE,'r') as sf:
    startingnetwork = sf.read()
networks = dp.runNetworkBuilder_OneAndTwo(STARTINGFILE,LEMFILE,RANKEDGENES,int(NUMNODES),int(NUMEDGES),is_new_node_essential=True)
networks = [startingnetwork] + networks
genes = []
for network in networks:
    eqns = network.split('\n')
    try:
        eqns.remove("")
    except:
        pass
    genes.append(tuple([eqn.split()[0] for eqn in eqns]))
uniquegenes = list(set(genes))
uniquePOs = []
for labels in uniquegenes:
    uniquePOs.append(EPO.makeJSONstring(TIMESERIES,TS_TYPE,labels,float(TS_TRUNCATION),n=1,scalingFactor=float(SCALING_FACTOR),step=0.01))
# for po in uniquePOs:
#     print json.loads(po)["poset"]
matchingPOs = [uniquePOs[uniquegenes.index(g)] for g in genes]

for k,(net,po) in enumerate(zip(networks,matchingPOs)):
    with open(INPUTDIR+'/networks/network{}.txt'.format(k),'w') as nf:
        nf.write(net)
    with open(INPUTDIR+'/POs/partialorder{}.json'.format(k),'w') as pf:
        pf.write(po)

