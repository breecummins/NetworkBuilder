import networkbuilder,fileparsers
import time

def addTopEdges(starting_network_str,source,target,type_reg,ranked_genes,numedges=10):
    networkstr_edges = []
    for rank in range(1,numedges+1):
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_str,source,target,type_reg,ranked_genes,save2file = False, which_edge_to_add=rank,add_new_node=False,network_is_file=True)
        if not networkstr:
            print "Skipped ranked edge {}".format(count)
        else:
            networkstr_edges.append(networkstr)
    return networkstr_edges

def addTopNodes(starstarting_network_str,source,target,type_reg,ranked_genes,numnodes=10,is_new_node_essential=True):
    networkstr_nodes = []
    for rank in range(1,numnodes+1):
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_str,source,target,type_reg,ranked_genes, save2file=False,add_new_node=True,which_node_to_add=rank,is_new_node_essential=is_new_node_essential,network_is_file=True)
        if not networkstr:
            print "Skipped ranked node {}".format(count1)
        else:
            networkstr_nodes.append(networkstr)
    return networkstr_nodes

def addOneAndTwoTopEdges(starting_network_str,source,target,type_reg,ranked_genes,numedges=10):
    networkstr_edges = []
    for rank1 in range(1,numedges+1):
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_str,source,target,type_reg,ranked_genes,save2file = False, which_edge_to_add=rank1,add_new_node=False,network_is_file=True)
        if not networkstr:
            print "Skipped ranked edge {}".format(rank1)
        else:
            networkstr_edges.append(networkstr)
            nstrtemp = []
            for rank2 in range(rank1+1,numedges+1):
                networkstr = networkbuilder.makeNearbyNetwork(networkstr_edges[-1],source,target,type_reg,ranked_genes,save2file=False,which_edge_to_add=rank2,add_new_node=False,network_is_file=False)
                if not networkstr:
                    print "Skipped ranked edges {} and {}".format(rank1, rank2)
                else:
                    nstrtemp.append(networkstr)
            networkstr_edges += nstrtemp
    return networkstr_edges

def addOneAndTwoTopNodes(starting_network_str,source,target,type_reg,ranked_genes,numnodes=10,is_new_node_essential=True):
    networkstr_nodes = []
    for rank1 in range(1,numnodes+1):
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_str, source,target,type_reg,ranked_genes, save2file=False,add_new_node=True,which_node_to_add=rank1,is_new_node_essential=is_new_node_essential,network_is_file=True)
        if not networkstr:
            print "Skipped ranked node {}".format(rank1)
        else:
            networkstr_nodes.append(networkstr)
            nstrtemp = []
            for rank2 in range(rank1+1,numnodes+1):
                networkstr = networkbuilder.makeNearbyNetwork(networkstr_nodes[-1],source,target,type_reg,ranked_genes,save2file=False, add_new_node=True,which_node_to_add=rank2,is_new_node_essential=is_new_node_essential,network_is_file=False)
                if not networkstr:
                    print "Skipped ranked nodes {} and {}".format(rank1, rank2)
                else:
                    nstrtemp.append(networkstr)
            networkstr_nodes += nstrtemp
    return networkstr_nodes

def addTopNodesAndEdges(starting_network_str,source,target,type_reg,ranked_genes,numnodes=10,numedges=10,is_new_node_essential=True):
    networkstr_nodeandedge = []
    for rank1 in range(1,numnodes+1):
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_str,source,target,type_reg,ranked_genes,save2file=False, add_new_node=True,which_node_to_add=rank1,is_new_node_essential=is_new_node_essential,network_is_file=True)
        if not networkstr:
            print "Skipped ranked node {}".format(rank1)
        else:
            startstr = networkstr
            nstrtemp = []
            for rank2 in range(rank1+1,numedges+1):
                networkstr = networkbuilder.makeNearbyNetwork(startstr,source,target,type_reg,ranked_genes,save2file=False, which_edge_to_add=rank2,add_new_node=False,network_is_file=False)
                if not networkstr:
                    print "Skipped ranked node {} and edge {}".format(rank1, rank2)
                else:
                    nstrtemp.append(networkstr)
            networkstr_nodeandedge += nstrtemp
    return networkstr_nodeandedge

def runNetworkBuilder_OneAndTwo(starting_network,LEMfile,ranked_genes_file,numnodes=10,numedges=10,is_new_node_essential=True,network_is_file=True):
    # get starting data and lem data
    if network_is_file:
        with open(starting_network,'r') as sn:
            starting_network_str = sn.read()
    else:
        starting_network_str = starting_network
    source,target,type_reg,lem_score = fileparsers.parseLEMfile(fname=LEMfile)
    ranked_genes = fileparsers.parseRankedGenes(fname=ranked_genes_file)
    # perturb starting network
    networkstr_edges = addOneAndTwoTopEdges(starting_network_str,source,target,type_reg,ranked_genes,numedges=numedges)
    networkstr_nodes = addOneAndTwoTopNodes(starting_network_str,source,target,type_reg,ranked_genes,numnodes=numnodes,is_new_node_essential=is_new_node_essential)
    networkstr_nodeandedge = addTopNodesAndEdges(starting_network_str,source,target,type_reg,ranked_genes,numnodes=numnodes,numedges=numedges,is_new_node_essential=is_new_node_essential)
    return networkstr_edges + networkstr_nodes + networkstr_nodeandedge

def runNetworkBuilder_OneOnly(starting_network_filename,LEMfile,ranked_genes_file,numnodes=10,numedges=10,is_new_node_essential=True,network_is_file=True):
    # get starting data and lem data
    if network_is_file:
        with open(starting_network,'r') as sn:
            starting_network_str = sn.read()
    else:
        starting_network_str = starting_network
    source,target,type_reg,lem_score = fileparsers.parseLEMfile(fname=LEMfile)
    ranked_genes = fileparsers.parseRankedGenes(fname=ranked_genes_file)
    networkstr_edges = addTopEdges(starting_network_str,source,target,type_reg,ranked_genes,numedges=numedges)
    networkstr_nodes = addTopNodes(starting_network_str,source,target,type_reg,ranked_genes,numnodes=numnodes,is_new_node_essential=is_new_node_essential)
    return networkstr_edges + networkstr_nodes

def testrun():
    # starting files
    starting_network_filename = "/Users/bcummins/GIT/DSGRN/networks/11D_2016_04_18_malaria40hrDuke_90TF_essential.txt"
    LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_90tfs_top25_dljtk_lem_score_table.txt'
    ranked_genes_file = "/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt"

    for n in runNetworkBuilder_OneAndTwo(starting_network_filename, LEMfile, ranked_genes_file,numnodes=10,numedges=10):
        print n

if __name__ == '__main__':
    pass