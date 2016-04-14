import fileparsers

def rankGenes(genes,LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_lem.allscores.tsv',outputfile='malaria20hr43rankedgenes.txt'):
    source,target,_,_=fileparsers.parseLEMFile(threshold=0,fname=LEMfile) # do not rank 0-scored edges; source,target are sorted by decreasing lem score
    num_edges = len(source)
    scores = [0]*len(genes)
    for k,(src,tar) in enumerate(zip(source,target)):
        scores[genes.index(src)] += (num_edges-k) # give highest score to top edges
        scores[genes.index(tar)] += (num_edges-k)
    ranks = fileparsers.sort_by_list(scores,[genes],reverse=True)
    descending_scores, ranked_genes = ranks[0], ranks[1]
    with open(outputfile,'w') as f:
        for (r,s) in zip(ranked_genes,descending_scores):
            f.write("{}    {}\n".format(r,s))

if __name__=='__main__':
    #specifically for malaria 20 hr, since we don't have periodicity ranks
    genes_20hr=['PF3D7_1115500','PF3D7_1006100','PF3D7_0504700','PF3D7_0604600','PF3D7_1408400','PF3D7_1027000','PF3D7_1103800','PF3D7_0614800','PF3D7_1435700','PF3D7_1405100','PF3D7_0403500','PF3D7_1301500','PF3D7_1428800','PF3D7_0506700','PF3D7_1350900','PF3D7_0925700','PF3D7_0518400','PF3D7_0529500','PF3D7_0809900','PF3D7_1008000','PF3D7_1009400','PF3D7_1225200','PF3D7_1337400','PF3D7_1437000','PF3D7_0313000','PF3D7_0627300','PF3D7_0629800','PF3D7_0704600','PF3D7_0729000','PF3D7_0812600','PF3D7_0818700','PF3D7_0915100','PF3D7_0919000','PF3D7_0926100','PF3D7_1119400','PF3D7_1138800','PF3D7_1225800','PF3D7_1227400','PF3D7_1233600','PF3D7_1237800','PF3D7_1302500','PF3D7_1406100','PF3D7_1412900']
    rankGenes(genes_20hr)

