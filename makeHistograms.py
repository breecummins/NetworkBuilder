import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.size'] = 24
import sys

def histogramData(fname="stats.txt"):
    with open(fname,'r') as stats:
        numparams=[]
        numFC=[]
        nummatches=[]
        for line in stats:
            nums = line.split('/')
            numparams.append(float(nums[0]))
            numFC.append(float(nums[1]))
            nummatches.append(float(nums[2]))
    FCoverParams=[FC/p for FC,p in zip(numFC,numparams)]
    MatchesOverParams=[matches/p for matches,p in zip(nummatches,numparams)]
    MatchesOverFCs=[matches/FC  if FC > 0 else float('nan') for matches,FC in zip(nummatches,numFC)]
    return FCoverParams, MatchesOverParams, MatchesOverFCs

def makeHistogram(fname="stats.txt",histtitle='8D LEM network, 154 perturbations',scaling_factor='0.00',startingvals=[float('nan')]*3,otherpoint=[float('nan')]*3):
    FCoverParams, MatchesOverParams,MatchesOverFCs = histogramData(fname)

    def plotHist(data,xlabel,title,sv,op):
        n, bins, patches = plt.hist([d*100 for d in data], 20, normed=0, facecolor='green', alpha=0.75)
        plt.hold('on')
        plt.plot(sv,25,marker='*',color='r',markersize=24)
        plt.plot(op,25,marker='*',color='k',markersize=24)
        plt.xlabel(xlabel)
        plt.ylabel('# networks')
        plt.title(title)
        plt.axis([0,100,0,30])
        plt.grid(True)
        plt.show()

    plotHist(FCoverParams,'% stable FCs',histtitle,float(startingvals[0]),float(otherpoint[0]))
    plotHist(MatchesOverParams,'% matches over total parameters',histtitle+', scaling factor '+scaling_factor,float(startingvals[1]),float(otherpoint[1]))
    # plotHist(MatchesOverFCs,'% matches over stable FCs',histtitle+', scaling factor '+scaling_factor,float(startingvals[2]))

def makeScatterPlot(fname1="stats_0-00.txt",fname2="stats_0-05.txt",startingvals=[(float('nan'),float('nan'))]*3,title='8D LEM network',scaling_factor1='0.00',scaling_factor2='0.05',otherpoint=[(float('nan'),float('nan'))]*3):
    # SCATTER PLOT DEPENDS ON HAVING THE SAME NETWORKS IN THE SAME ORDER. IF THIS DOESN'T HAPPEN, DATA WILL HAVE TO BE SORTED
    FCoverParams1, MatchesOverParams1,MatchesOverFCs1 = histogramData(fname1)
    FCoverParams2, MatchesOverParams2,MatchesOverFCs2 = histogramData(fname2)

    def plotScatter(data1,data2,fulltitle,xlabel,ylabel,sv,op):
        plt.scatter([d*100 for d in data1],[d*100 for d in data2],s=75,alpha=0.75)
        plt.hold('on')
        plt.plot(sv[0],sv[1],marker='*',color='r',markersize=24)
        plt.plot(op[0],op[1],marker='*',color='k',markersize=24)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(fulltitle)
        plt.axis([0,100,0,100])
        plt.grid(True)
        plt.show()

    # plotScatter(MatchesOverParams1,MatchesOverParams2,title+', % matches over total parameters','scaling factor '+scaling_factor1,'scaling factor '+scaling_factor2,startingvals[0])
    # plotScatter(MatchesOverFCs1,MatchesOverFCs2,title+', % matches over stable FCs','scaling factor '+scaling_factor1,'scaling factor '+scaling_factor2,startingvals[1])
    plotScatter(MatchesOverParams2,FCoverParams2,title+', resolution '+scaling_factor2,'% matches over total parameters','% stable FCs',startingvals[2],otherpoint[2])

def makeHistogram_multistable(fname="stats.txt"):
    with open(fname,'r') as stats:
        numparams=[]
        numFC=[]
        nummulti=[]
        for line in stats:
            nums = line.split('/')
            numparams.append(float(nums[0]))
            numFC.append(float(nums[1]))
            nummulti.append(float(nums[2]))
    
    MultioverParams=[m/p for m,p in zip(nummulti,numparams)]

    def plotHist(data,xlabel,title,sv):
        n, bins, patches = plt.hist([d*100 for d in data], 50, normed=0, facecolor='green', alpha=0.75)
        plt.hold('on')
        plt.plot(sv,100,marker='*',color='r',markersize=24)
        plt.xlabel(xlabel)
        plt.ylabel('# networks')
        plt.title(title)
        plt.axis([0,100,0,250])
        plt.grid(True)
        plt.show()

    plotHist(MultioverParams,'% multistability','{} random perturbations'.format(len(MultioverParams)-1),100)

if __name__ == "__main__":
    # EXAMPLE INPUTS FOR HISTOGRAM: 
    # /Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential_scalingfactor0-00_patternmatches_summarystats.txt
    # '8D LEM network, 154 perturbations'
    # 0.00
    # [11.3,20.1,5.0]

    # makeHistogram(fname=sys.argv[1],histtitle=sys.argv[2],scaling_factor=sys.argv[3],startingvals=eval(sys.argv[4]))#,otherpoint=eval(sys.argv[5]))
    makeScatterPlot(*sys.argv[1:3],startingvals=eval(sys.argv[3]),title=sys.argv[4])#,otherpoint=eval(sys.argv[5]))

    # makeHistogram_multistable(sys.argv[1])
