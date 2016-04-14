import networkbuilder

def addTopEdges(starting_network_filename,LEMfile,ranked_genes_file,new_network_name,save2file=True,numedges=10,draw_network=False,essential=True):
    count1 = 1
    while count1 < numedges+1:
        new_network_filename = new_network_name + "_" + str(count1).zfill(2) + "edge" + "_essential"*essential + ".txt"
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, save2file = save2file, which_edge_to_add=count1,add_new_node=False,draw_network=draw_network)
        if not networkstr:
            print "Skipped ranked edge {}".format(count1)
        else:
            count2 = count1+1
            while count2 < numedges+1:
                if essential:
                    new_network_filename2 = new_network_filename[:-14] + "_" + str(count2).zfill(2) + "edge_essential.txt"
                else:
                    new_network_filename2 = new_network_filename[:-4] + "_" + str(count2).zfill(2) + "edge.txt"
                networkstr = makenetwork(new_network_filename,LEMfile,ranked_genes_file,new_network_filename2, save2file=save2file,which_edge_to_add=count2,add_new_node=False,draw_network=draw_network)
                if not networkstr:
                    print "Skipped ranked edges {} and {}".format(count1, count2)
                count2 += 1
        count1 += 1

def addTopNodes(starting_network_filename,LEMfile,ranked_genes_file,new_network_name,save2file=True,numnodes=10,draw_network=False,is_new_node_essential=True,essential=True):
    wordlist = new_network_name.rsplit('/',1)
    path = wordlist[0] + '/'
    fname = wordlist[1].split('D',1)
    dim = int(fname[0])
    # network_middle = 'D' + fname[1].replace("_essential","") + "_"
    network_middle = 'D' + fname[1] + "_"
    count1 = 1
    while count1 < numnodes+1:
        node2add = network_middle + str(count1).zfill(2) + "node"
        new_network_filename = path + str(dim+1) + node2add + "_essential"*essential + ".txt"
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, save2file=save2file,add_new_node=True,draw_network=draw_network,which_node_to_add=count1,is_new_node_essential=is_new_node_essential)
        if not networkstr:
            print "Skipped ranked node {}".format(count1)
        else:
            count2 = count1+1
            while count2 < numnodes+1:
                new_network_filename2 = path + str(dim+2) + node2add + "_" + str(count2).zfill(2) + "node" + "_essential"*essential + ".txt"
                networkstr = networkbuilder.makeNearbyNetwork(new_network_filename,LEMfile,ranked_genes_file,new_network_filename2,save2file=save2file, add_new_node=True,draw_network=draw_network,which_node_to_add=count2,is_new_node_essential=is_new_node_essential)
                if not networkstr:
                    print "Skipped ranked nodes {} and {}".format(count1, count2)
                count2 += 1
        count1 += 1

def addTopNodesAndEdges(starting_network_filename,LEMfile,ranked_genes_file,new_network_name,save2file=save2file,numnodes=10,numedges=10,draw_network=False,is_new_node_essential=True,essential=True):
    wordlist = new_network_name.rsplit('/',1)
    path = wordlist[0] + '/'
    fname = wordlist[1].split('D',1)
    dim = int(fname[0])
    new_network_name = path + str(dim+1) + 'D' + fname[1]
    count1 = 1
    while count1 < numnodes+1:
        new_network_filename = new_network_name + "_" + str(count1).zfill(2) + "node" + "_essential"*essential + ".txt"
        networkstr = networkbuilder.makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename,save2file=save2file, add_new_node=True,draw_network=draw_network,which_node_to_add=count1,is_new_node_essential=is_new_node_essential)
        if not networkstr:
            print "Skipped ranked node {}".format(count1)
        else:
            count2 = 1
            while count2 < numedges+1:
                if essential:
                    new_network_filename2 = new_network_filename[:-14] + "_" + str(count2).zfill(2) + "edge_essential.txt"
                else:
                    new_network_filename2 = new_network_filename[:-4] + "_" + str(count2).zfill(2) + "edge.txt"
                networkstr = networkbuilder.makeNearbyNetwork(new_network_filename,LEMfile,ranked_genes_file,new_network_filename2,save2file=save2file, which_edge_to_add=count2,add_new_node=False,draw_network=draw_network)
                if not networkstr:
                    print "Skipped ranked node {} and edge {}".format(count1, count2)
                count2 += 1
        count1 += 1

def runNetworkBuilder(starting_network_filename,LEMfile,ranked_genes_file,save2file=True,numnodes=10,numedges=10):
    essential = bool(starting_network_filename.find("essential"))
    new_network_name = starting_network_filename.replace("_essential","").split(".")[0]
    addTopEdges(starting_network_filename,LEMfile,ranked_genes_file,new_network_name,save2file,numedges=numedges,essential=essential)
    addTopNodes(starting_network_filename,LEMfile,ranked_genes_file,new_network_name,save2file,numnodes=numnodes,essential=essential)
    addTopNodesAndEdges(starting_network_filename,LEMfile,ranked_genes_file,new_network_name,save2file,numnodes=numnodes,numedges=numedges,essential=essential)

if __name__ == '__main__':
    # starting files
    starting_network_filename = "networks/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential.txt"
    LEMfile='/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair2015_v2_fpkm-p1_s19_50tfs_top25_dljtk_lem_score_table.txt'
    ranked_genes_file = "/Users/bcummins/ProjectData/malaria/wrair2015_v2_fpkm-p1_s19_40hr_highest_ranked_genes/wrair-fpkm-p1_malaria_s19_DLxJTK_50putativeTFs.txt"

    runNetworkBuilder(starting_network_filename, LEMfile, ranked_genes_file,whichbuilder = "networkbuilder_malaria_40hr",numnodes=10,numedges=10)
