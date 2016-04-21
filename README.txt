Instructions for running random network perturbations.

Shell scripts: random_network_mainscript.sh
		 	   random_network_helperscript.sh
			   concatenateresults.sh

Local python module dependencies: random_networkbuilder.py
			   			   		  fileparsers (function: createNetworkFile)
               			   		  networkbuilder (function: checkEdgeAdmissible)
               			   		  summaryJSON.py

From within this folder, call 

. ./random_network_mainscript.sh NETWORK_SPEC NUMBER_OF_PERTURBATIONS MAX_NUM_NODES PATH_TO_DSGRN

The NETWORK_SPEC is a text file containing a network following DSGRN format.

The NUMBER_OF_PERTURBATIONS and the MAX_NUM_NODES specify how many distinct perturbations to make that have less than or equal to MAX_NUM_NODES vertices in the network.

PATH_TO_DSGRN is the path to the DSGRN repository. It is used to construct the SIGNATURES path, assuming standard file structure within DSGRN.

First, random_network_mainscript.sh calls the python module random_networkbuilder.py to generate NUMBER_OF_PERTURBATIONS networks with less than or equal to MAX_NUM_NODES vertices nearby the starting network NETWORK_SPEC. These network files are stored in a locally created directory with a time stamp in standard DSGRN format (see INPUTDIR in random_network_mainscript.sh). 

Two caveats:
1) NUMBER_OF_PERTURBATIONS should not exceed the number of files allowed in a directory.
2) The combination of NUMBER_OF_PERTURBATIONS and MAX_NUM_NODES can potentially create an infinite loop in random_networkbuilder.py, if there are not a sufficient number of "admissible" networks with few enough nodes. Admissible means the numbers of in- and out-edges are such that the database for the network can be computed (see the function checkEdgeAdmissible in networkbuilder.py). I have verified that the following set of arguments terminates:

NETWORK_SPEC=$DSGRN/networks/5D_2016_02_08_cancer_withRP_essential.txt
NUMBER_OF_PERTURBATIONS=10000
MAX_NUM_NODES=8

Second, random_network_mainscript.sh loops through the generated network files and calls a qsub job for each on the script random_network_helperscript.sh. The helper script generates the database for the network using 8 cores and then performs sql searches on the output. No pattern matching is performed. The results of the sql searches are dumped in a json file (python module summaryJSON.py) along with the network specification, and then the intermediate files (network, database, and sql search results) are deleted. The json files are stored in a locally generated folder (see OUTPUTDIR in random_network_mainscript.sh). 

Third, the results will have to be concatenated when all of the jobs finish. I do this manually using the script concatenateresults.sh. Along with merging all of the results, it deletes the intermediate directories that were created locally. The call is:
 
. ./concatenateresults.sh JSONSAVEFILE OUTPUTDIR INPUTDIR DATABASEDIR

Every file in OUTPUTDIR is concatenated into JSONSAVEFILE as a member of a json list. Then OUTPUTDIR, INPUTDIR, and DATABASEDIR are all deleted (these are time-stamped intermediate folders). Do NOT put JSONSAVEFILE in OUTPUTDIR for obvious reasons.


