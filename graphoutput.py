import pydot

def makeGraph(genes,outedges,regulation,name='graph_lastedge500.pdf'):
    graph = pydot.Dot(graph_type='digraph')
    for g in genes:
        graph.add_node(pydot.Node(g))
    for i,(oe,reg) in enumerate(zip(outedges,regulation)):
        for o,r in zip(oe,reg):
            if r=='r':
                graph.add_edge(pydot.Edge((genes[i],genes[o]),arrowhead='tee'))
            else:
                graph.add_edge(pydot.Edge(genes[i],genes[o]))
    graph.write_pdf(name)

def plottimeseries(period20,fname='period20_timeseries.png'):
    # OBSOLETE. Needs to be updated.
    genelist,timeseries = LEM.generateMasterList()
    period20_timeseries = []
    masterinds = []
    for p in period20:
        ind = genelist.index(p)
        masterinds.append(ind)
        period20_timeseries.append(timeseries[ind])
    fig=plt.figure()
    rcParams.update({'font.size': 22})
    plt.hold('on')
    times=range(0,61,3)
    leg=[]
    for p,ts in zip(period20,period20_timeseries):
        plt.plot(times,[t/max(ts) for t in ts],linewidth=2)
        leg.append(str(genelist.index(p))+' '+p)
    plt.xlabel('Hours')
    plt.ylabel('Abundance')
    leghandle=plt.legend(leg,loc='center left', bbox_to_anchor=(1, 1))
    plt.savefig(fname, bbox_extra_artists=(leghandle,), bbox_inches='tight')


def timeSeriesParserPlotter(genes,masterlist,fname='/Users/bcummins/ProjectData/malaria/wrair2015_pfalcip_harmonicGenes_forNewLEM/wrair2015_pfalc_43tf_20hrPer_lem.tsv',savename='timeseries_malaria_8node_43_20hr.pdf'):
    # OBSOLETE. Needs to be updated.
    f=open(fname,'r')
    for _ in range(5):
        f.readline()
    genelist=f.readline().split()[1:]
    times=[[float(w) for w in l.split()[1:]] for l in f.readlines()]
    timeseries=np.array(times).transpose()
    plt.clf()
    fig=plt.figure()
    NUM_COLORS = len(genes)
    cm = plt.get_cmap('spectral')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    plt.hold('on')
    times=range(0,61,3)
    leg=[]
    for g in genes:
        ind=genelist.index(g)
        M=max(timeseries[ind])
        plt.plot(times,[t/M for t in timeseries[ind]],linewidth=2)
        leg.append(str(masterlist.index(g)) + ' ' + g)
    leghandle=plt.legend(leg,loc='center left', bbox_to_anchor=(1, 1))
    # plt.show()
    plt.savefig(savename, bbox_extra_artists=(leghandle,), bbox_inches='tight')
    plt.close('all')
    
def plotTimeSeries():
    # OBSOLETE. Needs to be updated.
    masterlist=generateMasterList()
    # genes=['PF3D7_0504700','PF3D7_0506700', 'PF3D7_0818700','PF3D7_0925700','PF3D7_0403500','PF3D7_1115500','PF3D7_1350900','PF3D7_0919000','PF3D7_1406100','PF3D7_0614800','PF3D7_1237800','PF3D7_0809900']
    for g in masterlist:
        timeSeriesParserPlotter([g],masterlist,savename='timeseries_malaria_43_20hr_gene{:02d}.pdf'.format(masterlist.index(g)))
