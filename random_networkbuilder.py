import fileparsers
import random

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
        reg[startnode][ind] = thisreg
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
    # pick an incoming edge for n
    innode = getRandomInt(n)
    inreg = getRandomInt(2)
    graph[innode].append(n)
    reg[innode].append('a'*regbool + 'r'*(not regbool))
    # pick an outgoing edge for n 
    outnode = getRandomInt(n)
    outreg = getRandomInt(2)
    graph.append([outnode])
    reg.append(['a'*regbool + 'r'*(not regbool)])
    return graph, reg

def getRandomInt(n):
    return random.randrange(n)

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
    _,starting_graph,starting_regulation,_ = fileparsers.getGraphFromNetworkFile(network_filename=starting_network_filename)
    networks = [None] * N
    for i in range(N):
        networks[i] = perturbNetwork(starting_graph,starting_regulation)
    uniq_ntw = list(set(networks))
    for i,(graph,reg) in enumerate(uniq_ntw):
        node_list = ['x'+str(k) for k in range(len(graph))]
        essential = [True] * len(graph)
        fname = savename+str(i)+'.txt'
        fileparsers.createNetworkFile(node_list,graph,reg,ess,fname,save2file=True)

