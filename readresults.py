import json,sys

def makestats(fname='results.json'):
    with open(fname,'r') as f:
        listofnetworks = json.load(f)
    for n in listofnetworks:
        pc = n["ParameterCount"]
        fcpc = n["StableFCParameterCount"]
        fcpm = n["StableFCMatchesParameterCount"]
        print str(pc) + '/' + str(fcpc) + '/' + str(fcpm) + '/{0:.2g}'.format(float(fcpm)/fcpc * 100)

if __name__=='__main__':
    makestats(sys.argv[1]) 
