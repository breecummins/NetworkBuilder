import subprocess

def checkEdgeAdmissible(outedges,regulation):
    # THIS CODE CAN EASILY BECOME OBSOLETE!!!!
    # The following is based on the files in /share/data/bcummins/work/share/DSGRN/logic/ as of 04/22/16,
    # and on the choice that activations are ALWAYS summed and repressions are ALWAYS multiplied.
    # In particular, the files 4_x_2_2.dat will never be used.
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
        if len(ie) > 5:
            return False
        elif len(oe) > 7:
            return False
        elif len(ie) == 3 and len(oe)>5:
            return False
        elif len(ie) == 4: 
            if ir.count('a') != 4 and ir.count('r') != 4:
                return False
            elif len(oe) == 3: 
                return False
            elif len(oe) == 4 and ir.count('r') != 4:
                return False
            elif len(oe) >= 5:
                return False
        elif len(ie) == 5:
            if len(oe) > 1:
                return False
            elif ir.count('r') != 5 and ir.count('a') != 5:
                return False
    return True

def checkComputability(network_spec,maxparams):
    try:
        sentence = subprocess.check_output(['dsgrn','network', network_spec,'parameter'],shell=False)
        numparams = [int(s) for s in sentence.split() if s.isdigit()][0]
        return (numparams <= int(maxparams))
    except:
        return False
