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

def addEdges(node_list,graph,reg,source,target,type_reg):
    n = len(graph)
    success = 0
    while success < 2:
        k = getRandomInt(len(source))
        s,t,r = source[k],target[k],type_reg[k]
        sind = node_list.index(s)
        tind = node_list.index(t)
        if s == t and r == 'r': #if negative self-loop, skip
            continue
        elif t in graph[sind] and r == reg[sind][graph[sind].index(tind)]: #if edge exists, skip
            continue
        else:
            graph,reg = altergraph(sind,tind,graph,reg,r)
            success += 1
    return graph,reg

def makeNearbyNetworks(node_list,starting_graph,starting_regulation,essential,numperturbations,source,target,type_reg,savename = 'network_',maxparams=200000):
    # reset random seed for every run
    random.seed()
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
        graph,reg = addEdges(node_list,sg,sr,source,target,type_reg)
        # extract the network spec from the graph and regulation type
        network_spec = fileparsers.createNetworkFile(node_list,graph,reg,essential,save2file=False)
        # check that network spec is all of unique, small enough, and computable, then write to file and save string for comparison
        if (network_spec not in networks) and checkComputability(network_spec,maxparams):
            fname = savename+str(len(networks))+'.txt'
            with open(fname,'w') as f:
                f.write(network_spec)
            networks.append(network_spec)
    return node_list

INPUTDIR = sys.argv[1]
DSGRN = sys.argv[2]

# generate starting graph of labeled out-edges (activation and repression)
network_spec_file = DSGRN + "/networks/11D_2016_04_18_malaria40hrDuke_90TF_essential.txt"
node_list,starting_graph,starting_regulation,essential = fileparsers.getGraphFromNetworkFile(network_filename=network_spec_file)

# make and prune edges
source,target,type_reg,score = fileparsers.parseLEMfile_pickbadnetworks(usepldLap=1,threshold=0,fname='datafiles/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt')
newsource,newtarget,newtype_reg = [],[],[]
for (s,t,r) in zip(source,target,type_reg):
    if s in node_list and t in node_list:
        newsource.append(s)
        newtarget.append(t)
        newtype_reg.append(r)

# perturbation params
numperturbations = 130
maxparams = 200000

# make networks
labels = makeNearbyNetworks(node_list,starting_graph,starting_regulation,essential,numperturbations,newsource,newtarget,newtype_reg,savename = INPUTDIR+'/network_',maxparams=maxparams)

# make pattern
TIMESERIES="datafiles/wrair2015_v2_fpkm-p1_s19.tsv"
TS_TYPE="row"  # or 'col', type of time series file format
TS_TRUNCATION=42 #cut after 42 time units (NOT after index 42)
SCALING_FACTOR=0.05   # between 0 and 1; 0 = most restrictive partial order
pattern = EPO.makeJSONstring(TIMESERIES,TS_TYPE,labels,float(TS_TRUNCATION),n=1,scalingFactor=float(SCALING_FACTOR),step=0.01)
json.dump(pattern,open(INPUTDIR+'/pattern.json','w'))

