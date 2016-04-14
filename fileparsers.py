def sort_by_list(X,Y,reverse=False):
    # X is a list of length n, Y is a list of lists of length n
    # sort every list in Y by either ascending order (reverse = False) or descending order (reverse=True) of X 
    newlists = [[] for _ in range(len(Y)+1)]
    for ztup in sorted(zip(X,*Y),reverse=reverse):
        for k,z in enumerate(ztup):
            newlists[k].append(z)
    return newlists

def parseLEMfile(threshold=0,fname='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt'):
    # returns the source, target, and type of regulation sorted by decreasing LEM score (also returned)
    # file format must be:
    # 1) some number of comment lines denoted by #
    # 2) following lines begin with TARGET_GENE = TYPE_REG(SOURCE_GENE)
    # 3) pld.lap score is the first numerical score on each line 
    source=[]
    type_reg=[]
    target=[]
    lem_score=[]
    with open(fname,'r') as f:
        for l in f.readlines():
            while l[0] == '#':
                continue
            wordlist=l.split()
            k=0
            while not wordlist[k][0].isdigit():
                continue
            lem = float(wordlist[k])
            if lem>threshold:
                target.append(wordlist[0]) 
                lem_score.append(lem)
                two_words=wordlist[2].split('(')
                type_reg.append(two_words[0])
                source.append(two_words[1][:-1])
    [lem_score,source,target,type_reg] = sort_by_list(lem_score,[source,target,type_reg],reverse=True) # reverse=True because we want descending lem scores
    return source,target,type_reg,lem_score

def parseRankedGenes(fname="/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_DLxJTK_257TFs.txt"):
    # file format: comment lines denoted by hash followed by lines beginning with GENE_NAME RANK
    genes = []
    ranks = []
    with open(fname,'r') as f:
        for l in f.readlines():
            while l[0] == '#':
                continue
            wordlist=l.split()
            genes.append(wordlist[0])
            ranks.append(wordlist[1])
    ranked_genes = sort_by_list(ranks,[genes],reverse=False)[1] # reverse=False because we want ascending ranks
    return ranked_genes

def createNetworkFile(node_list,graph,regulation,essential=None,fname="network.txt",save2file=True):
    # take a graph and return a network spec file
    # which edges are essential
    if essential is None:
        essential = [False]*len(node_list)
    # calculate inedges and get regulation type
    dual=[[(j,reg[outedges.index(node)]) for j,(outedges,reg) in enumerate(zip(graph,regulation)) if node in outedges] for node in range(len(node_list))]
    # auto-generate network file for database
    networkstr = ""  
    with open(fname,'w') as f:
        for (name,inedgereg,ess) in zip(node_list,dual,essential):
            act = " + ".join([node_list[i] for (i,r) in inedgereg if r == 'a'])
            if act:
                act = "(" + act  + ")"
            rep = "".join(["(~"+node_list[i]+")" for (i,r) in inedgereg if r == 'r'])
            nodestr = name + " : " + act + rep 
            if ess:
                nodestr + " : E"
            nodestr += "\n"
            if save2file:
                f.write(nodestr)
            networkstr += nodestr
    return networkstr

def getGraphFromNetworkFile(network_filename):
    # take a network spec file and return a graph
    node_list = []
    inedges = []
    essential = [] #essentialness is inherited
    with open(network_filename,'r') as nf:
        for l in nf.readlines():
            words = l.replace('(',' ').replace(')',' ').replace('+',' ').split()
            if words[-2:] == [':', 'E']:
                essential.append(True)
                words = words[:-2]
            else:
                essential.append(False)
            node_list.append(words[0])
            inedges.append(words[2:]) # get rid of ':' at index 1
    graph = [[] for _ in range(len(node_list))]
    regulation = [[] for _ in range(len(node_list))]
    for target,edgelist in enumerate(inedges):
        for ie in edgelist:
            if ie[0] == '~':
                ind = node_list.index(ie[1:])
                regulation[ind].append('r') 
            else:
                ind = node_list.index(ie)
                regulation[ind].append('a') 
            graph[ind].append(target)  # change inedges to outedges
    return node_list,graph,regulation,essential

def generateMasterList(fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_462TF_forLEM/cuffNorm_subTFs_stdNames.txt'):
    # This is for all 462 TFs in the original malaria data set. May be deprecated.
    f=open(fname,'r')
    wordlist = f.readline().split()[22::]
    f.close()
    genelist = wordlist[::22]
    timeseries=[]
    for k in range(len(genelist)):
        timeseries.append([float(w) for w in wordlist[22*k+1:22*(k+1)]])
    return genelist, timeseries

