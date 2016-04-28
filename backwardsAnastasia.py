import fileparsers,sys,random,json
from databasecomputability import checkComputability
import ExtremaPO as EPO

def getRandomInt(n):
    return random.randrange(n)

def altergraph(startnode,endnode,graph,reg,newreg):
    n = len(graph)
    if endnode == startnode:
        # self-loops are a special case
        if endnode in graph[startnode]:
            # if the self-loop exists, delete it
            outedges = graph[startnode]
            ind = outedges.index(endnode)
            graph[startnode] = outedges[:ind]+outedges[ind+1:]
            tempreg = reg[startnode]
            reg[startnode] = tempreg[:ind]+tempreg[ind+1:]
        else:
            # otherwise add self-activation only (no self-repression allowed)
            graph[startnode].append(endnode)
            reg[startnode].append('a')
    elif endnode in graph[startnode]:
        # swap regulation if edge already exists (given sign)
        ind = graph[startnode].index(endnode)
        reg[startnode][ind] = newreg
    else:
        # otherwise add edge with given sign
        graph[startnode].append(endnode)
        reg[startnode].append(newreg)
    return graph, reg

def addEdge(node_list,graph,reg,source,target,type_reg):
    n = len(graph)
    startnode = getRandomInt(n)
    endnode = getRandomInt(n)
    for (s,t,r) in zip(source,target,type_reg):
        if s == node_list[startnode] and t == node_list[endnode]:
            if startnode == endnode and r == 'r': #if negative self-loop, skip
                continue
            elif endnode in graph[startnode] and r == reg[startnode][graph[startnode].index(endnode)]: #if edge exists, skip (the edge with opposite regulation may still be in the list)
                continue
            else:
                return altergraph(startnode,endnode,graph,reg,r)
    return None,None


def makeNearbyNetworks(starting_network_filename,numperturbations,source,target,type_reg,savename = 'network_',maxnodes=8,maxparams=200000):
    # reset random seed for every run
    random.seed()
    # generate starting graph of labeled out-edges (activation and repression)
    node_list,starting_graph,starting_regulation,essential = fileparsers.getGraphFromNetworkFile(network_filename=starting_network_filename)
    # begin analysis with starting network spec -- save to file and initialize networks with [networkstr]
    fname = savename+str(0)+'.txt'  
    networks = [fileparsers.createNetworkFile(node_list,starting_graph,starting_regulation,essential,fname=fname,save2file=True)]
    # now make perturbations
    # note that the while loop below can be an infinite loop if numperturbations is too large for maxnodes and maxparams
    while len(networks) < int(numperturbations)+1: 
        # below: the lists within the starting graph must be explicitly copied or else the starting graph gets reassigned within perturbNetwork
        sg = [list(outedges) for outedges in starting_graph]  
        sr = [list(reg) for reg in starting_regulation]
        # add two edges (or swap regulation of edges) to the starting network
        success = 0
        while success < 2:
            graph,reg = addEdge(node_list,sg,sr,source,target,type_reg)
            if graph is not None:
                success += 1
        # extract the network spec from the graph and regulation type
        network_spec = fileparsers.createNetworkFile(node_list,graph,reg,essential,save2file=False)
        # check that network spec is all of unique, small enough, and computable, then write to file and save string for comparison
        if (len(graph) <= int(maxnodes)) and (network_spec not in networks) and checkComputability(network_spec,maxparams):
            fname = savename+str(len(networks))+'.txt'
            with open(fname,'w') as f:
                f.write(network_spec)
            networks.append(network_spec)
    return node_list

INPUTDIR = sys.argv[1]
DSGRN = sys.argv[2]

source,target,type_reg,score = fileparsers.parseLEMfile_pickbadnetworks(usepldLap=1,threshold=0,fname='datafiles/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt')

network_spec = DSGRN + "/networks/11D_2016_04_18_malaria40hrDuke_90TF_BACKWARDS_essential.txt"
numperturbations = 100
maxnodes = 11
maxparams = 200000

labels = makeNearbyNetworks(network_spec,numperturbations,source,target,type_reg,savename = INPUTDIR+'/network_',maxnodes=maxnodes,maxparams=200000)

TIMESERIES="datafiles/wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=42 #cut after 42 time units (NOT after index 42)
SCALING_FACTOR=0.05   # between 0 and 1; 0 = most restrictive partial order

pattern = EPO.makeJSONstring(TIMESERIES,TS_TYPE,labels,float(TS_TRUNCATION),n=1,scalingFactor=float(SCALING_FACTOR),step=0.01)
json.dump(pattern,open(INPUTDIR+'/pattern.json','w'))

