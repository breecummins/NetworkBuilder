import json,sys,glob

def pickOutNetworks(listofjsonnetworks,fname='results.json'):
    with open(fname,'r') as f:
        listofdicts = json.load(f)
    desiredjsondicts = []
    for l in listofdicts:
        if l["Network"] in listofjsonnetworks:
            desiredjsondicts.append(l)
        if len(l) == len(listofjsonnetworks):
            break
    return desiredjsondicts

def findmax(fname='results.json',metric=0,nummax=1):
    # metric 0 => use stable FC over params
    # metric 1 => use matches over params
    # metric 2 => use matches over stable FCs
    with open(fname,'r') as f:
        listofnetworks = json.load(f)
    listofstats=[]
    for n in listofnetworks:
        pc = n["ParameterCount"]
        fcpc = n["StableFCParameterCount"]
        fcpm = n["StableFCMatchesParameterCount"]
        if metric == 0:
            listofstats.append(float(fcpc)/float(pc))
        elif metric == 1:
            listofstats.append(float(fcpm)/float(pc))
        elif fcpc > 0:
            listofstats.append(float(fcpm)/float(fcpc))
        else:
            listofstats.append(float('nan'))
    # get nummax indices
    inds = sorted(range(len(listofstats)), key=lambda i: listofstats[i], reverse=True)[:nummax]
    NW = [listofnetworks[i] for i in inds]
    return NW,inds,listofstats

def findcommon(lolnetworks):
    isall=[]
    inall=[n["Network"] for n in lolnetworks[0]]
    for networklist in lolnetworks:
        ntw = [n["Network"] for n in networklist]
        inall = set(inall).intersection(ntw)
        isall.extend(ntw)
    isall = set(isall)
    return inall, isall


def makestats(fname='results.json',savename='stats.txt'):
    with open(fname,'r') as f:
        listofnetworks = json.load(f)
    with open(savename,'w') as sn:
        for n in listofnetworks:
            pc = n["ParameterCount"]
            fcpc = n["StableFCParameterCount"]
            fcpm = n["StableFCMatchesParameterCount"]
            if fcpc > 0:
                sn.write(str(pc) + '/' + str(fcpc) + '/' + str(fcpm) + '/{0:.2f}'.format((float(fcpm)/fcpc) * 100)+"\n")
            else:
                sn.write(str(pc) + '/' + str(fcpc) + '/' + str(fcpm) + '/NaN'+"\n")

def makestats_multistability(fname='results.json',savename='stats.txt'):
    with open(fname,'r') as f:
        listofnetworks = json.load(f)
    with open(savename,'w') as sn:
        for n in listofnetworks:
            pc = n["ParameterCount"]
            fcpc = n["StableFCParameterCount"]
            mpc = n["MultistableParameterCount"]
            sn.write(str(pc) + '/' + str(fcpc) + '/' + str(mpc)+"\n")

def makestats_multiplefile(DIR='outfiles/'):
    for fname in glob.glob(DIR+'results*.json'):
        with open(fname,'r') as f:
            n = json.load(f)
        pc = n["ParameterCount"]
        fcpc = n["StableFCParameterCount"]
        fcpm = n["StableFCMatchesParameterCount"]
        if fcpc > 0:
            print str(pc) + '/' + str(fcpc) + '/' + str(fcpm) + '/{0:.2f}'.format((float(fcpm)/fcpc) * 100)
        else:
            print str(pc) + '/' + str(fcpc) + '/' + str(fcpm) + '/NaN'

if __name__=='__main__':
    # makestats(sys.argv[1],sys.argv[2]) 
    # makestats_multistability(sys.argv[1],sys.argv[2]) 
    # print json.load(open(sys.argv[1],'r'))[0]["Network"]

    NW1,inds1,listofstats_0_00_m_over_p = findmax(fname='/Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/11D_2016_04_18_malaria40hrDuke_90TF_essential_scalingfactor0-05_shuffledgenes.json',metric=1,nummax=5)
    for nw in NW1:
        print nw["PatternSpecification"]
        print "\n"

    # listofjsonnetworks=[u'PF3D7_0611200 : (PF3D7_1337100) : E\nPF3D7_1139300 : (~PF3D7_0611200) : E\nPF3D7_1146600 : (~PF3D7_1139300)(~PF3D7_1408200) : E\nPF3D7_1222600 : (PF3D7_1146600)(~PF3D7_1317200) : E\nPF3D7_1317200 : (PF3D7_1408200)(~PF3D7_1356900) : E\nPF3D7_1337100 : (PF3D7_1139300 + PF3D7_1317200)(~PF3D7_1146600) : E\nPF3D7_1356900 : (~PF3D7_1222600) : E\nPF3D7_1408200 : (~PF3D7_0611200) : E\n', u'PF3D7_0611200 : (PF3D7_1337100) : E\nPF3D7_1139300 : (~PF3D7_0611200) : E\nPF3D7_1146600 : (~PF3D7_1139300)(~PF3D7_1408200) : E\nPF3D7_1222600 : (PF3D7_1146600)(~PF3D7_1317200) : E\nPF3D7_1317200 : (PF3D7_1408200)(~PF3D7_1146600)(~PF3D7_1356900) : E\nPF3D7_1337100 : (PF3D7_1139300 + PF3D7_1317200) : E\nPF3D7_1356900 : (~PF3D7_1222600) : E\nPF3D7_1408200 : (~PF3D7_0611200) : E\n', u'PF3D7_0611200 : (PF3D7_1337100) : E\nPF3D7_1139300 : (~PF3D7_0611200) : E\nPF3D7_1146600 : (~PF3D7_1139300)(~PF3D7_1408200) : E\nPF3D7_1222600 : (PF3D7_1146600)(~PF3D7_1317200) : E\nPF3D7_1317200 : (PF3D7_1139300 + PF3D7_1408200)(~PF3D7_1356900) : E\nPF3D7_1337100 : (PF3D7_1139300 + PF3D7_1317200) : E\nPF3D7_1356900 : (~PF3D7_1222600) : E\nPF3D7_1408200 : (~PF3D7_0611200) : E\n']

    # fname = '/Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential_scalingfactor0-00_patternmatches.json'

    # for p in pickOutNetworks(listofjsonnetworks,fname):
    #     print p


    # NW1,inds1,listofstats_0_00_m_over_p = findmax(fname='/Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential_scalingfactor0-00_patternmatches.json',metric=1,nummax=5)
    # for n in NW1:
    #     print n["Network"]

    # NW2,inds2,listofstats_0_05_m_over_p = findmax(fname='/Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential_scalingfactor0-05_patternmatches.json',metric=1,nummax=7)
    # NW3,inds3,listofstats_0_00_m_over_f = findmax(fname='/Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential_scalingfactor0-00_patternmatches.json',metric=2,nummax=4)
    # NW4,inds4,listofstats_0_00_f_over_p = findmax(fname='/Users/bcummins/patternmatch_helper_files/patternmatch_archived_results/8D_2016_04_11_malaria40hr_50TF_top25_T0-05_essential_scalingfactor0-00_patternmatches.json',metric=0,nummax=10)

    # inall,isall=findcommon([NW1,NW2])
    # print len(isall)
    # print len(inall)
    # print inall

    # inall,isall=findcommon([NW1,NW2,NW3])
    # print len(isall)
    # print len(inall)

    # inall,isall=findcommon([NW1,NW2,NW4])
    # print len(isall)
    # print len(inall)

    # inall,isall=findcommon([NW3,NW4])
    # print len(isall)
    # print len(inall)

    # print "vals:\n"
    # print [listofstats_0_05_m_over_p[i] for i in inds1]
    # print [listofstats_0_00_f_over_p[i] for i in inds1]


