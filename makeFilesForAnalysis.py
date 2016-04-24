import ExtremaPO as EPO
import deterministicperturbations as dp
import sys,json,subprocess

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
MAXPARAMS = sys.argv[11]

with open(STARTINGFILE,'r') as sf:
    startingnetwork = sf.read()
candidates = dp.runNetworkBuilder_OneAndTwo(startingnetwork,LEMFILE,RANKEDGENES,int(NUMNODES),int(NUMEDGES),is_new_node_essential=True,network_is_file=False)
candidates = [startingnetwork] + candidates

networks=[]
for k,network_spec in enumerate(candidates):
    sentence = subprocess.check_output(['dsgrn','network', network_spec,'parameter'],shell=False)
    numparams = [int(s) for s in sentence.split() if s.isdigit()][0]
    if numparams <= MAXPARAMS:
        networks.append(network_spec)

print "Number of networks is {}.".format(len(networks))

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
    uniquePOs.append(EPO.makeJSONstring(TIMESERIES,TS_TYPE,labels,float(TS_TRUNCATION),n=1,scalingFactor=float(SCALING_FACTOR),step=0.01))
# for po in uniquePOs:
#     print json.loads(po)["poset"]

matchingPOs = [uniquePOs[uniquegenes.index(g)] for g in genes]

for k,(net,po) in enumerate(zip(networks,matchingPOs)):
    with open(INPUTDIR+'/networks/network{}.txt'.format(k),'w') as nf:
        nf.write(net)
    with open(INPUTDIR+'/POs/partialorder{}.json'.format(k),'w') as pf:
        pf.write(po)

