import json, re, itertools
import ExtremaPO as EPO

def ParseRowFile(fileName,node_list=None):
    # Parse file with genes in row format
    # node_list can be:
    # None -- get all data
    # integer -- get top node_list number of lines from the file
    # list of strings -- get all data with matching labels
    TSList = []
    TSLabels = []
    value = 0  # indicates if time_points line has been reached
    if isinstance(node_list, (int, long)) and node_list > 0:
        numlines = node_list
        node_list = None
    else:
        numlines = float("inf")
    N = 0
    with open(fileName,'r') as f:
        for line in f:
            wordlist = line.split()
            if wordlist[0] != '#':
                if value == 0:
                    timeStepList = [float(time) for time in wordlist[1:]]
                    value = 1
                else:
                    N +=1
                    name = wordlist[0]
                    if node_list is None or name in node_list:
                        TSLabels.append(name)
                        TSList.append([float(item) for item in wordlist[1:]])
                        if node_list is not None:
                            node_list.remove(name)
            if node_list == [] or N == numlines:
                break
    return TSList,TSLabels, timeStepList

# Truncate timeseries. Keep all data before timeCutOff
def TruncateTS(newTSList,timeStepList,timeCutOff):
    indexOfCutOff = timeStepList.index(timeCutOff)
    truncatedTSList = []
    for ts in newTSList:
        truncatedTSList.append(ts[:(indexOfCutOff+1)])
    # print(truncatedTSList)
    return truncatedTSList

def getMaxMinData(timeseries_file,ts_type,ts_truncation,node_list):
    if ts_type == 'col':
        raise ValueError('Column parsing not implemented.')
    elif ts_type == 'row':
        TSList,TSLabels,timeStepList = ParseRowFile(timeseries_file,node_list)

    if ts_truncation != float(-1):
        TSList = TruncateTS(TSList,timeStepList,ts_truncation)
        timeStepList = timeStepList[:(timeStepList.index(ts_truncation)+1)]

    MaxMinData={}
    for (label,ts) in zip(TSLabels,TSList):
        MaxMinData[label] = (timeStepList[ts.index(max(ts))],timeStepList[ts.index(min(ts))])
    return MaxMinData

def binMaxMinData(MaxMinData,network_node_list):
    bins = []
    data = []
    for key,value in MaxMinData.iteritems():
        if value not in data:
            data.append(value)
            bins.append([key])
        else:
            bins[data.index(value)].append(key) 
    candidates = [ bins[data.index(MaxMinData[n])] for n in network_node_list ]
    return candidates

def makePatterns(networks,TIMESERIES,TS_TYPE,TS_TRUNCATION,scalingFactor,INPUTDIR):
    # get all subsets of genes
    genes = []
    for network in networks:
        eqns = network.split('\n')
        try:
            eqns.remove("")
        except:
            pass
        genes.append(tuple([eqn.split()[0] for eqn in eqns]))
    uniquegenes = list(set(genes))
    # Make patterns. Is slow. Needs to speed up if possible.
    uniquePOs = []
    for labels in uniquegenes:
        uniquePOs.append(EPO.makeJSONstring(TIMESERIES,TS_TYPE,labels,TS_TRUNCATION,1,scalingFactor,step=0.01))
    # return one pattern for each network
    return [uniquePOs[uniquegenes.index(g)] for g in genes]

def makeNetworks(timeseries_file,ts_type,ts_truncation,network_spec,node_list=None,scalingFactors=[0.05,0.10,0.15],INPUTDIR=''):
    network_node_list = []
    for line in network_spec.split("\n"):
        network_node_list.append(line.split()[0])
    MaxMinData = getMaxMinData(timeseries_file,ts_type,ts_truncation,node_list)
    # print MaxMinData
    # print "\n"
    candidates = binMaxMinData(MaxMinData,network_node_list)
    # print candidates
    # print "\n"
    networks = []
    # make all substitutions
    for sub in itertools.product(*candidates):
        if len(set(sub)) < len(sub):
            continue # can't have the same gene twice
        diff = dict((n,m) for (n,m) in zip(network_node_list,sub) if n != m)
        if len(diff) > 0:
            # the following snippet does all replacements at once, so you don't have to care about order of application
            pattern = re.compile("|".join(re.escape(k) for k in diff.keys()))
            new_network_spec = pattern.sub(lambda M: diff[M.group(0)], network_spec)
            networks.append(new_network_spec)
    for sc in scalingFactors:
        sclabel = '{:.2f}'.format(sc).replace('.','-')
        patterns = makePatterns(networks,timeseries_file,ts_type,ts_truncation,sc,INPUTDIR)
        uniqpats = sorted(list(set(patterns)))
        counts = dict((up,patterns.count(up)) for up in uniqpats)

        with open(INPUTDIR+'/counts{}.txt'.format(sclabel),'w') as cf:
            cf.write('Pattern# NetworkCount\n')
            for k,(pat,count) in enumerate(counts.iteritems()):
                cf.write(str(k)+' '+str(count)+'\n')
                with open(INPUTDIR+'/pattern{}_{}.json'.format(k,sclabel),'w') as pf:
                    json.dump(pat,pf)



if __name__ == "__main__":
    timeseries_file = "datafiles/wrair2015_v2_fpkm-p1_s19.tsv"
    ts_type = "row"
    ts_truncation = 42

    # node_list = ['PF3D7_0100100','PF3D7_0100200','PF3D7_0100300','PF3D7_0100400','PF3D7_0100500','PF3D7_0100600','PF3D7_0100700','PF3D7_0100800','PF3D7_0100900','PF3D7_0101000','PF3D7_0101100','PF3D7_0101200','PF3D7_0101300','PF3D7_0101400','PF3D7_0101500','PF3D7_0101600','PF3D7_0101700','PF3D7_0101800','PF3D7_0101900','PF3D7_0102000','PF3D7_0102100','PF3D7_0102200','PF3D7_0102300','PF3D7_0102400','PF3D7_0102500','PF3D7_0102600','PF3D7_0102700','PF3D7_0102800','PF3D7_0102900','PF3D7_0103000','PF3D7_0103100','PF3D7_0103200','PF3D7_0103300','PF3D7_0103400','PF3D7_0103500','PF3D7_0103600','PF3D7_0103700','PF3D7_0103800','PF3D7_0103900','PF3D7_0104000']

    # node_list = 200

    node_list=[]
    with open('datafiles/wrair-fpkm-p1_malaria_s19_DLxJTK_90putativeTFs.txt','r') as rf:
        rf.readline()
        for l in rf:
            node_list.append(l.split()[0])

    with open('/Users/bcummins/GIT/DSGRN/networks/11D_2016_04_18_malaria40hrDuke_90TF_essential.txt','r') as f:
        network_spec = f.read()  
    # network_spec = "PF3D7_0100100 : PF3D7_0100200\nPF3D7_0100200 : (~PF3D7_0100100)"

    scalingFactors = [0.05,0.10,0.15]
    INPUTDIR = 'inputfiles'

    makeNetworks(timeseries_file,ts_type,ts_truncation,network_spec,node_list,scalingFactors,INPUTDIR)








