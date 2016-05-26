import ExtremaPO as EPO
import deterministicperturbations as dp
import sys,json,subprocess,os,re

NETWORKDIR=os.path.expanduser(sys.argv[1])
MAPPINGDIR=os.path.expanduser(sys.argv[2])
INPUTDIR=os.path.expanduser(sys.argv[3])
PATTERNDIR=os.path.expanduser(sys.argv[4])
TIMESERIES=os.path.expanduser(sys.argv[5])
TS_TYPE=sys.argv[6] 
TS_TRUNCATION=float(sys.argv[7]) 
SCALING_FACTORS=eval(sys.argv[8]) 

def getidentifier(fname):
    # it is assumed that the concatenation of all numbers in a file's base name is unique
    basename = (fname.split(os.sep)[-1].split(os.extsep))[0]
    identifier = ''.join(c for c in basename if c.isdigit())
    return identifier

def formatidentifier(identifier,numdigits):
    return str(identifier).zfill(numdigits)

networkfiles = [os.path.join(NETWORKDIR,nf) for nf in os.listdir(NETWORKDIR)]
formatnumnet = len(str(len(networkfiles)))
mappingfiles = [os.path.join(MAPPINGDIR,nf) for nf in os.listdir(MAPPINGDIR)]
mappingidentifiers = [getidentifier(mf) for mf in mappingfiles]

genelist = []
uniqueid = []
# make all networks
for netfile in networkfiles:
    network_str = open(netfile,'r').read()
    genericnames = ([nl.split()[0] for nl in network_str.split('\n') if nl])
    ident = getidentifier(netfile)
    net_identifier = formatidentifier(ident,formatnumnet)
    mapfile = mappingfiles[mappingidentifiers.index(ident)]
    with open(mapfile,'r') as mf:
        lines=[]
        for l in mf:
            if l.rstrip():
                lines.append(l)
    formatnummap = len(str(len(lines)))
    for k,line in enumerate(lines):
        genes = line.split()
        if len(genes) != len(genericnames):
            print "Dimension of network and gene mapping do not match: Skipping " + network_str + " with mapping " + line + ".\n"
        else:
            genelist.append(tuple(genes))
            substitutions = dict(zip(genericnames,genes))
            re_pattern = re.compile('|'.join(substitutions.keys()))
            new_network = re_pattern.sub(lambda x: substitutions[x.group()], network_str)
            map_identifier = formatidentifier(k,formatnummap)
            uid = net_identifier+'_'+map_identifier
            subprocess.call("mkdir "+os.path.join(PATTERNDIR,uid),shell=True)
            uniqueid.append(uid)
            savename = 'network'+uid+'.txt'
            with open(os.path.join(INPUTDIR,savename),'w') as newnf:
                newnf.write(new_network)

# make all patterns from unique genelist and save with matching file names
uniquegenes = list(set(genelist))
uniquepatterns = []
for labels in uniquegenes:
    patlist=[]
    for scalingFactor in SCALING_FACTORS:
        patlist.append(EPO.makeJSONstring(TIMESERIES,TS_TYPE,labels,float(TS_TRUNCATION),n=1,scalingFactor=float(scalingFactor),step=0.01))
    uniquepatterns.append(patlist)

for uid,g in zip(uniqueid,genelist):
    i = uniquegenes.index(g)
    for scalingFactor,pattern in zip(SCALING_FACTORS,uniquepatterns[i]):
        sf = '_{:.2f}'.format(scalingFactor).replace('.','_')
        patternfile = os.path.join(PATTERNDIR,os.path.join(uid,'pattern{}.json'.format(sf)))
        with open(patternfile,'w') as pf:
            json.dump(pattern,pf)


