import networkbuilder
import time

def addTopEdges(starting_network_filename,LEMfile,ranked_genes_file,numedges=10):
    count1 = 1
    networkstr_edges = []
    while count1 < numedges+1:
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,save2file = False, which_edge_to_add=count1,add_new_node=False,draw_network=False,network_is_file=True)
        if not networkstr:
            print "Skipped ranked edge {}".format(count1)
        else:
            networkstr_edges.append(networkstr)
            nstrtemp = []
            count2 = count1+1
            while count2 < numedges+1:
                networkstr = networkbuilder.makeNearbyNetwork(networkstr_edges[-1],LEMfile,ranked_genes_file,save2file=False,which_edge_to_add=count2,add_new_node=False,draw_network=False,network_is_file=False)
                if not networkstr:
                    print "Skipped ranked edges {} and {}".format(count1, count2)
                else:
                    nstrtemp.append(networkstr)
                count2 += 1
            networkstr_edges += nstrtemp
        count1 += 1
    return networkstr_edges

def addTopNodes(starting_network_filename,LEMfile,ranked_genes_file,numnodes=10,is_new_node_essential=True):
    count1 = 1
    networkstr_nodes = []
    while count1 < numnodes+1:
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file, save2file=False,add_new_node=True,draw_network=False,which_node_to_add=count1,is_new_node_essential=is_new_node_essential,network_is_file=True)
        if not networkstr:
            print "Skipped ranked node {}".format(count1)
        else:
            networkstr_nodes.append(networkstr)
            nstrtemp = []
            count2 = count1+1
            while count2 < numnodes+1:
                networkstr = networkbuilder.makeNearbyNetwork(networkstr_nodes[-1],LEMfile,ranked_genes_file,save2file=False, add_new_node=True,draw_network=False,which_node_to_add=count2,is_new_node_essential=is_new_node_essential,network_is_file=False)
                if not networkstr:
                    print "Skipped ranked nodes {} and {}".format(count1, count2)
                else:
                    nstrtemp.append(networkstr)
                count2 += 1
            networkstr_nodes += nstrtemp
        count1 += 1
    return networkstr_nodes

def addTopNodesAndEdges(starting_network_filename,LEMfile,ranked_genes_file,numnodes=10,numedges=10,is_new_node_essential=True):
    count1 = 1
    networkstr_nodeandedge = []
    while count1 < numnodes+1:
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,save2file=False, add_new_node=True,draw_network=False,which_node_to_add=count1,is_new_node_essential=is_new_node_essential,network_is_file=True)
        if not networkstr:
            print "Skipped ranked node {}".format(count1)
        else:
            networkstr_nodeandedge.append(networkstr)
            nstrtemp = []
            count2 = 1
            while count2 < numedges+1:
                networkstr = networkbuilder.makeNearbyNetwork(networkstr_nodeandedge[-1],LEMfile,ranked_genes_file,save2file=False, which_edge_to_add=count2,add_new_node=False,draw_network=False,network_is_file=False)
                if not networkstr:
                    print "Skipped ranked node {} and edge {}".format(count1, count2)
                else:
                    nstrtemp.append(networkstr)
                count2 += 1
            networkstr_nodeandedge += nstrtemp
        count1 += 1
    return networkstr_nodeandedge

def runNetworkBuilder(starting_network_filename,LEMfile,ranked_genes_file,numnodes=10,numedges=10,is_new_node_essential=True):
    networkstr_edges = addTopEdges(starting_network_filename,LEMfile,ranked_genes_file,numedges=numedges)
    networkstr_nodes = addTopNodes(starting_network_filename,LEMfile,ranked_genes_file,numnodes=numnodes,is_new_node_essential=is_new_node_essential)
    networkstr_nodeandedge = addTopNodesAndEdges(starting_network_filename,LEMfile,ranked_genes_file,numnodes=numnodes,numedges=numedges,is_new_node_essential=is_new_node_essential)
    return networkstr_edges + networkstr_nodes + networkstr_nodeandedge

if __name__ == '__main__':
    # starting files
    starting_network_filename = "networks/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential.txt"
    LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_50tfs_top25_dljtk_lem_score_table.txt'
    ranked_genes_file = "/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair-fpkm-p1_malaria_s19_DLxJTK_50putativeTFs.txt"

    for n in runNetworkBuilder(starting_network_filename, LEMfile, ranked_genes_file,numnodes=2,numedges=2):
        print n
