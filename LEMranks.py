import fileparsers
import sys,statistics,json
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.size']=24

def reformat(node_list,graph,regulation):
    net_source=[]
    net_target=[]
    net_reg = []

    for k,(outedges,reg) in enumerate(zip(graph,regulation)):
        for (oe,r) in zip(outedges,reg):
            net_source.append(node_list[k])
            net_target.append(node_list[oe])
            net_reg.append(r)
    return net_source,net_target,net_reg

def getLEMranks(network_spec_str,totaledges,source,target,type_reg):
    node_list,graph,regulation,essential = fileparsers.getGraphFromNetworkFile(networkstr=network_spec_str)
    net_source,net_target,net_reg = reformat(node_list,graph,regulation)

    LEMranks = []
    for (ns,nt,nr) in zip(net_source,net_target,net_reg):
        for k,(s,t,r) in enumerate(zip(source,target,type_reg)):
            if s == ns and t==nt and r==nr:
                LEMranks.append(k / totaledges)
                break

    return LEMranks

def printLEMranks(results_file,LEM_file,fname="LEMranks.txt",use_pldLap=False,plotresults=False,title="11D malaria 40 hr 90 TF, scaling factor 0.05"):
    # use_pldLap = False or 0 means use sqrt loss / root
    if use_pldLap:
        source,target,type_reg,lem_score = fileparsers.parseLEMfile(-1,LEM_file)
    else:
        source,target,type_reg,sqrtlossdroot_score = fileparsers.parseLEMfile_sqrtlossdroot(2,LEM_file)
    totaledges = float(len(source))

    results = json.load(open(results_file,'r'))

    try:
        network_spec_str = results["Network"]
        LEMranks = getLEMranks(network_spec_str,totaledges,source,target,type_reg)
        print "Mean: {}".format(statistics.mean(LEMranks))
        print "Median: {}".format(statistics.median(LEMranks))
        print "% stable FCs: {}".format(float(results["StableFCParameterCount"])/float(results["ParameterCount"]))
        print "% pattern matches: {}".format(float(results["StableFCMatchesParameterCount"])/float(results["ParameterCount"]))
    except:
        stats=[]
        for R in results:
            network_spec_str = R["Network"]
            LEMranks = getLEMranks(network_spec_str,totaledges,source,target,type_reg)
            stats.append( (statistics.mean(LEMranks),statistics.median(LEMranks),float(R["StableFCMatchesParameterCount"])/float(R["ParameterCount"])) )
        with open(fname,'w') as sf:
            for s in stats:
                sf.write('/'.join([str(t) for t in s])+"\n")
        if plotresults:
            plotLEMranks(stats,title,use_pldLap)


def plotLEMranks(stats,title,use_pldLap):
    means,meds,percents=zip(*stats)
    plt.scatter(means[1:],percents[1:],s=75,alpha=0.75)
    plt.hold('on')
    plt.plot(means[0],percents[0],marker='*',color='r',markersize=24)
    plt.title(title)
    if use_pldLap:
        plt.xlabel('Average normalized edge rank from pld.Lap')
    else:
        plt.xlabel('Average normalized edge rank from sqrt loss / root')
    plt.ylabel('% pattern matches')
    plt.show()
    # plt.scatter(meds,percents,s=75,alpha=0.75)
    # plt.title = title+', median rank'
    # plt.show()

def plotSampleHistogram(LEMRank_file,title="11D malaria 40 hr 90 TF permutations",use_pldLap=False):
    means=[]
    with open(LEMRank_file,'r') as sf:
        means = [float(l.split('/')[0]) for l in sf]
    n, bins, patches = plt.hist(means[1:], 100, normed=0, facecolor='black', alpha=0.4)
    plt.hold('on')
    plt.plot(means[0],5,marker='*',color='r',markersize=24)
    if use_pldLap:
        plt.xlabel('Average normalized edge rank from pld.Lap')
    else:
        plt.xlabel('Average normalized edge rank from sqrt loss / root')
    plt.ylabel('# networks')
    plt.title(title)
    plt.axis([0,1,0,80])
    plt.grid(True)
    plt.show()

            



if __name__=="__main__":
    LEMRank_file = "/Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/11D_2016_04_18_malaria40hrDuke_90TF_essential_shuffledgenes_scalingfactor_0-05_2500shuffles_LEMranks_sqrtdloss.txt"
    plotSampleHistogram(LEMRank_file)


    # results_file = sys.argv[1]
    # LEM_file = sys.argv[2]
    # save_file = sys.argv[3]
    # use_pldLap = eval(sys.argv[4]) 
    # plotresults = True

    # printLEMranks(results_file,LEM_file,save_file,use_pldLap,plotresults)

    # with open("/Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/11D_2016_04_18_malaria40hrDuke_90TF_essential_shuffledgenes_scalingfactor_0-05_2500shuffles_LEMranks_sqrtdloss.txt","r") as rf:
    #     nonzeros = []
    #     for l in rf:
    #         wordlist = l.split('/')
    #         if float(wordlist[-1]) > 0:
    #             nonzeros.append(float(wordlist[-1]))
    # for s in sorted(nonzeros):
    #     print s
    # print len(nonzeros)
