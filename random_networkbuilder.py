import fileparsers
import random,sys

def getRandomInt(n):
    return random.randrange(n)

def addEdge(graph,reg):
    n = len(graph)
    startnode = getRandomInt(n)
    endnode = getRandomInt(n)
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
        # swap regulation if edge already exists
        ind = graph[startnode].index(endnode)
        thisreg = reg[startnode][ind]
        reg[startnode][ind] = 'a'*(thisreg == 'r') + 'r'*(thisreg == 'a')
    else:
        # otherwise add edge with random sign
        graph[startnode].append(endnode)
        regbool = getRandomInt(2)
        reg[startnode].append('a'*regbool + 'r'*(not regbool))
    return graph, reg

def addNode(graph,reg):
    n = len(graph)
    # the new node will have index n
    # pick an incoming edge for n from the existing network (i.e. don't pick node n)
    innode = getRandomInt(n) # NOT getRandomInt(n+1)
    inreg = getRandomInt(2)
    graph[innode].append(n)
    reg[innode].append('a'*inreg + 'r'*(not inreg))
    # pick an outgoing edge for n from the existing network
    outnode = getRandomInt(n)
    outreg = getRandomInt(2)
    graph.append([outnode])
    reg.append(['a'*outreg + 'r'*(not outreg)])
    return graph, reg

def perturbNetwork(graph,reg):
    keepgoing = 1
    while keepgoing:
        edge = getRandomInt(2)
        if edge:
            graph,reg = addEdge(graph,reg)
        else:
            graph,reg = addNode(graph,reg)
        keepgoing = getRandomInt(2)
    return (graph,reg)

def makeNearbyNetworks(starting_network_filename,N,savename = 'network_'):
    random.seed()
    _,starting_graph,starting_regulation,_ = fileparsers.getGraphFromNetworkFile(network_filename=starting_network_filename)
    networks=[]
    while len(networks) < int(N):
        # below: the lists within the starting graph must be explicitly copied or else the starting graph gets reassigned within perturbNetwork
        sg = [list(graph) for graph in starting_graph]  
        sr = [list(reg) for reg in starting_regulation]
        net = perturbNetwork(sg,sr)
        if net not in networks:
            networks.append(net)
    for i,(graph,reg) in enumerate(networks):
        node_list = ['x'+str(k) for k in range(len(graph))]
        essential = [True] * len(graph)
        fname = savename+str(i)+'.txt'
        fileparsers.createNetworkFile(node_list,graph,reg,essential,fname,save2file=True)

if __name__ == '__main__':
    # fname="/Users/bcummins/GIT/DSGRN/networks/5D_2016_02_08_cancer_withRP_essential.txt"
    # N = 200
    # savename = 'networks/randnet_'
    makeNearbyNetworks(*sys.argv[1:])

