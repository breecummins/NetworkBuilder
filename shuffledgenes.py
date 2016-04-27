import fileparsers
import ExtremaPO as EPO
import random,sys
from shutil import copyfile

INPUTDIR = sys.argv[1]
starting_network_file = sys.argv[2]
ranked_genes_file = sys.argv[3] 
numtopgenes = int(sys.argv[4])
numshuffles = int(sys.argv[5])
timeseries_file = sys.argv[6]
ts_type = sys.argv[7]
ts_truncation = float(sys.argv[8])
scalingFactor = float(sys.argv[9])

# get starting data
starting_node_list,starting_graph,starting_regulation,_ = fileparsers.getGraphFromNetworkFile(network_filename=starting_network_file)
numnodes = len(starting_graph)
ranked_genes = fileparsers.parseRankedGenes(fname=ranked_genes_file)[:numtopgenes]

# record initial pattern
pattern_spec = EPO.makeJSONstring(timeseries_file,ts_type,starting_node_list,ts_truncation,n=1,scalingFactor=scalingFactor,step=0.01)
with open(INPUTDIR+'/POs/pattern0.json','w') as pf:
    pf.write(pattern_spec)
copyfile(starting_network_file, INPUTDIR+'/networks/network0.txt')
shuffles = [range(numnodes)]

# now shuffle
random.seed()
essential=[True]*11

while len(shuffles) < numshuffles+1:
    rs = random.sample(range(numtopgenes),numnodes)
    if rs not in shuffles:
        labels = [ranked_genes[r] for r in rs]
        pattern_spec = EPO.makeJSONstring(timeseries_file,ts_type,labels,ts_truncation,n=1,scalingFactor=scalingFactor,step=0.01)
        with open(INPUTDIR+'/POs/pattern{}.json'.format(len(shuffles)),'w') as pf:
            pf.write(pattern_spec)
        fileparsers.createNetworkFile(labels,starting_graph,starting_regulation,essential=essential,fname=INPUTDIR+'/networks/network{}.txt'.format(len(shuffles)),save2file=True)
        shuffles.append(rs)



