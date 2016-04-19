import json,sys,glob

def makestats(fname='results.json'):
    with open(fname,'r') as f:
        listofnetworks = json.load(f)
    for n in listofnetworks:
        pc = n["ParameterCount"]
        fcpc = n["StableFCParameterCount"]
        fcpm = n["StableFCMatchesParameterCount"]
        if fcpc > 0:
            print str(pc) + '/' + str(fcpc) + '/' + str(fcpm) + '/{0:.2f}'.format((float(fcpm)/fcpc) * 100)
        else:
            print str(pc) + '/' + str(fcpc) + '/' + str(fcpm) + '/NaN'


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
    makestats_multiplefile(sys.argv[1]) 
