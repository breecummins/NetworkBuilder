import fileparsers, graphoutput
import numpy as np
from scipy.sparse.csgraph import connected_components
import time

def chooseGenes(topscores,source,target):
    # This is currently deprecated because we are only picking a threshold instead of the top number of highest scoring edges to get a smaller number of genes.
    return list(set(source[:topscores]).intersection(target[:topscores]))

def makeOutedges(genes,source,target,type_reg,lem_score):
    outedges=[[] for _ in range(len(genes))]
    regulation=[[] for _ in range(len(genes))]
    lem_scores=[[] for _ in range(len(genes))]
    for s,t,tr,l in zip(source,target,type_reg,lem_score):
        if s in genes and t in genes:
            outedges[genes.index(s)].append(genes.index(t))
            regulation[genes.index(s)].append(tr)
            lem_scores[genes.index(s)].append(l)
    return [tuple(oe) for oe in outedges],[tuple(r) for r in regulation],[tuple(l) for l in lem_scores]

def strongConnect(outedges):
    adjacencymatrix=np.zeros((len(outedges),len(outedges)))
    for i,o in enumerate(outedges):
        for j in o:
            adjacencymatrix[i,j]=1
    N,components=connected_components(adjacencymatrix,directed=True,connection="strong")
    return list(components)

def strongConnectIndices(outedges):
    components=strongConnect(outedges)
    grouped_components=[[k for k,c in enumerate(components) if c == d] for d in range(max(components)+1) if components.count(d)>1]
    return grouped_components

def pruneOutedges(geneinds, outedges, regulation, LEM_scores):
    new_outedges,new_regulation,new_LEM_scores=[],[],[]
    for k in geneinds:
        otup,rtup,ltup=[],[],[]
        for o,r,l in zip(outedges[k],regulation[k],LEM_scores[k]):
            if o in geneinds:
                otup.append(geneinds.index(o)), rtup.append(r), ltup.append(l)
        new_outedges.append(tuple(otup))
        new_regulation.append(tuple(rtup))
        new_LEM_scores.append(tuple(ltup)) 
    return new_outedges,new_regulation,new_LEM_scores   

def generateLEMNetworks(threshold=0,frontname='yeast25',makegraph=1,saveme=1,onlylargestnetwork=0,LEMfile='/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'):
    print 'Parsing file...'
    source,target,type_reg,lem_score=fileparsers.parseLEMFile(threshold,LEMfile)
    genes = sorted(set(source).intersection(target))
    # print genes
    print 'Making outedges...'
    outedges,regulation,LEM_scores=makeOutedges(genes,source,target,type_reg,lem_score)
    # print outedges
    print 'Extracting strongly connected components...'
    grouped_scc_gene_inds=strongConnectIndices(outedges)
    scc_genenames=[[genes[g]  for g in G] for G in grouped_scc_gene_inds ]
    # print scc_genes
    if onlylargestnetwork:
        L = [len(g) for g in grouped_scc_gene_inds]
        ind=L.index(max(L))
        grouped_scc_gene_inds = grouped_scc_gene_inds[ind]
        flat_scc_gene_inds = grouped_scc_gene_inds[:]
        scc_genenames = scc_genenames[ind]
        flat_scc_genenames = scc_genenames[:]
    else:    
        flat_scc_gene_inds= [g for G in grouped_scc_gene_inds for g in G]
        flat_scc_genenames = [s for S in scc_genenames for s in S]
    outedges,regulation,LEM_scores=pruneOutedges(flat_scc_gene_inds,outedges,regulation,LEM_scores)
    if makegraph:
        print 'Making graph for {} nodes and {} edges....'.format(len(flat_scc_gene_inds),len([o for oe in outedges for o in oe]))
        graphoutput.makeGraph(flat_scc_genenames,outedges,regulation,name='{}_graph_thresh{}.pdf'.format(frontname,str(threshold).replace('.','-')))
    if saveme:
        _ = fileparsers.createNetworkFile(flat_scc_genenames,outedges,regulation,[essential]*len(flat_scc_genenames),new_network_path+'{}D_'.format(len(flat_scc_genenames))+time.strftime("%Y_%m_%d")+'_{}_T{}'.format(frontname,str(threshold).replace('.','-')) + '_essential'*essential +'.txt',save2file=True)
    else:
        return fileparsers.createNetworkFile(flat_scc_genenames,outedges,regulation,[essential]*len(flat_scc_genenames),save2file=False)

if __name__ == "__main__":
    # for t in [0.5,0.4,0.1,0.05]:
    #     generateResult(threshold=t,saveme=0)

    # for t in [0.4,0.3,0.2,0.1]:
    #     generateResult(threshold=t,saveme=0,frontname='yeast40',LEMfile='/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top40dljtk_lem_score_table.txt')

    for t in [0.6,0.5,0.4,0.3,0.2,0.1]:
        generateLEMNetworks(threshold=t,saveme=0,frontname='mouseliver40',LEMfile='/Users/bcummins/ProjectData/mouseliver/hogenesch-10st2013_livr_top40dljtk_lem_score_table.txt')