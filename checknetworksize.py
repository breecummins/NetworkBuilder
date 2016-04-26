import subprocess
import deterministicperturbations as dp

STARTINGFILE="/Users/bcummins/GIT/DSGRN/networks/5D_2016_04_23_wavepool_essential.txt" 
LEMFILE="datafiles/haase-fpkm-p1_yeast_s29_top25dljtk_lem_score_table.txt" 
RANKEDGENES="datafiles/haase-fpkm-p1_yeast_s29_DLxJTK_top25TFs.txt" 
NUMNODES=10 # add nodes of rank 1 to n singly and in pairs
NUMEDGES=10 # add edges of rank 1 to n singly and in pairs

with open(STARTINGFILE,'r') as sf:
    startingnetwork = sf.read()
print startingnetwork
networks = dp.runNetworkBuilder_OneAndTwo(startingnetwork,LEMFILE,RANKEDGENES,int(NUMNODES),int(NUMEDGES),is_new_node_essential=True,network_is_file=False)
networks = [startingnetwork] + networks
goodones=[]
for k,network_spec in enumerate(networks):
    sentence = subprocess.check_output(['dsgrn','network', network_spec,'parameter'],shell=False)
    numparams = [int(s) for s in sentence.split() if s.isdigit()][0]
    if numparams <= 25000:
        goodones.append(network_spec)
print len(goodones)
