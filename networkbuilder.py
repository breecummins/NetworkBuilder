import fileparsers

def addNode(node_list,ranked_genes,source,target,type_reg,which_node_to_add = 1):
    count = 0
    new_node = None
    for g in ranked_genes:
        if g not in node_list:
            count += 1
            if count == which_node_to_add:
                new_node=g
                break
    if new_node is None:
        return None, None, None
    best_outedge = None
    best_inedge = None
    N = len(node_list)
    for (s,t,r) in zip(source,target,type_reg):
        if s == new_node and t in node_list and best_outedge is None:
            best_outedge = (N,node_list.index(t),r)
        elif s in node_list and t == new_node and best_inedge is None:
            best_inedge = (node_list.index(s),N,r)
        elif best_outedge is not None and best_inedge is not None:
            break
    return new_node, best_inedge, best_outedge

def addEdge(which_edge_to_add,node_list,graph,regulation,source,target,type_reg):
    count = 0
    new_edge = None
    for (s,t,r) in zip(source,target,type_reg):
        if s in node_list and t in node_list:
            s_ind = node_list.index(s)
            t_ind = node_list.index(t)
            outedges = graph[s_ind]
            if t_ind not in outedges or r != regulation[s_ind][outedges.index(t_ind)]:
                count += 1
                if count == which_edge_to_add:
                    new_edge = (s_ind,t_ind,r)
                    break
    return new_edge

def checkEdgeAdmissible(outedges,regulation):
    # THIS CODE CAN EASILY BECOME OBSOLETE!!!!
    # The following is based on the files in /data/CHomP/Projects/DSGRN/DB/data/logic/ as of 04/12/16,
    # and on the choice that activations are ALWAYS summed and repressions are ALWAYS multiplied.
    inedges = []
    inreg = []
    for node in range(len(outedges)):
        ie = []
        ir = []
        for j,(o,r) in enumerate(zip(outedges,regulation)):
            try:
                ind = o.index(node)
            except:
                ind = None
            if ind is not None:
                ie.append(j)
                ir.append(r[ind])
        inedges.append(ie)
        inreg.append(ir)
    for (ie, oe, ir) in zip(inedges,outedges,inreg):
        if len(ie) > 4:
            return False
        elif len(oe) > 5:
            return False
        elif len(ie) == 4: 
            if len(oe) == 3 and ir.count('a') == 3: # three a's are added, three r's are multiplied
                return False
            elif len(oe) == 4 and ir.count('a') > 1:
                return False
            elif len(oe) == 5:
                return False
    return True

def makeNearbyNetwork(starting_network_str,source,target,type_reg,ranked_genes,new_network_filename="network.txt",save2file=False,which_edge_to_add=1,add_new_node=True,which_node_to_add=1,is_new_node_essential=False,network_is_file=True):
    # starting_network_str is the string that comes from reading the network file 
    # source, target, and type_reg are outputs of fileparsers.parseLEMfile
    # ranked_genes is the output of fileparsers.parseRankedGenes

    # if adding a node, two new edges will be added connecting the new node to the graph and which_edge_to_add is ignored
    # if not adding a node, which_node_to_add is ignored and which_edge_to_add is used with existing nodes

    # construct the graph for the starting network
    starting_node_list,starting_graph,starting_regulation,essential = fileparsers.getGraphFromNetworkFile(networkstr = starting_network_str)

    # add a new node or edge
    if add_new_node:
        new_node, best_inedge, best_outedge = addNode(starting_node_list,ranked_genes,source,target,type_reg,which_node_to_add)
        if new_node is None:
            raise ValueError("No new node to add.")
        # best_*edge = (source, target, regulation)
        node_list = starting_node_list + [new_node]
        graph = starting_graph + [[]]
        regulation = starting_regulation + [[]]
        graph[best_inedge[0]].append(best_inedge[1])
        regulation[best_inedge[0]].append(best_inedge[2])
        graph[best_outedge[0]].append(best_outedge[1])
        regulation[best_outedge[0]].append(best_outedge[2])
        essential.append(is_new_node_essential)
    else:
        new_edge = addEdge(which_edge_to_add,starting_node_list,starting_graph,starting_regulation,source,target,type_reg)        
        if new_edge is None:
            raise ValueError("No new edge to add.")
        else:
            (s,t,r) = new_edge # new_edge = (source,target,regulation)
        node_list = starting_node_list
        graph = starting_graph
        regulation = starting_regulation
        outedges = graph[s]
        if t in outedges:
            regulation[s][outedges.index[t]] = r
        else:
            graph[s].append(t)
            regulation[s].append(r)
    # # make output
    # if draw_network:
    #     graphoutput.makeGraph(node_list,graph,regulation,new_network_filename.replace(".txt",".pdf"))
    admissible = checkEdgeAdmissible(graph,regulation)
    if admissible:
        networkstr = fileparsers.createNetworkFile(node_list,graph,regulation,essential,new_network_filename,save2file= save2file)
    else:
        networkstr = ""
    return networkstr
    
if __name__ == "__main__":
    # starting files
    starting_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_05_yeastLEMoriginal_essential.txt"
    LEMfile = '/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt'
    ranked_genes_file = "/Users/bcummins/ProjectData/yeast/haase-fpkm-p1_yeast_s29_DLxJTK_257TFs.txt"

    # # add nodes to starting network
    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_1stnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=1,is_new_node_essential=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_2ndnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=2,is_new_node_essential=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_3rdnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=3,is_new_node_essential=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_4thnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=4,is_new_node_essential=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/8D_2016_04_07_yeastLEM_5thnode_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, add_new_node=True,draw_network=True,which_node_to_add=5,is_new_node_essential=True)

    # # add edges to starting network
    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_1stedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=1,add_new_node=False,draw_network=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_2ndedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=2,add_new_node=False,draw_network=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_3rdedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=3,add_new_node=False,draw_network=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_4thedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=4,add_new_node=False,draw_network=True)

    # new_network_filename = "/Users/bcummins/GIT/DSGRN/networks/7D_2016_04_07_yeastLEM_5thedge_essential.txt"
    # makeNearbyNetwork(starting_network_filename,LEMfile,ranked_genes_file,new_network_filename, which_edge_to_add=5,add_new_node=False,draw_network=True)

    for t in extractSubset(['FKH1','SPT21','PLM2','SWI4','WTM2','NDD1','HCM1'],threshold=0,fname=LEMfile):
        print t

    # for g in makeGraphFromNetworkFile(network_filename+'.txt'):
    #     print g
