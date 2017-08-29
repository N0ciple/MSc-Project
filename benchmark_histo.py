from simulation import *
from detectionUtils import *
from scipy.special import comb
import os
if os.name =='nt':
    import matplotlib.pyplot as plt
import numpy as np




def chiDist(histo1, histo2):
    PmQ2 = np.power(histo1 - histo2, 2)

    # prevent 0 values in division
    histo1[histo1 == 0] = np.finfo(float).eps
    histo2[histo2 == 0] = np.finfo(float).eps
    PpQ = histo1 + histo2
    vectRes = np.divide(PmQ2, PpQ)
    res = np.sum(vectRes)
    return np.sqrt(res)






def runHistoSimulation(myI, myProba) :
    ################ STEP 1
        # Generate an graph with rumor spread

    # Parameters definition
    numRumors = 20
    maxThreshold = 1
    numMonitors = 20
    propagProba = myProba
    numNodes = 200
    linkProba = 0.3
    monitorTrigger = list()
    numStep = 100

    j = 0

    Graph, Pos, rumorSources, monitorsList = generateGraphReady(numNodes, linkProba, maxThreshold, numRumors, numMonitors)
    # fig1.savefig('./TestFigs/figT'+str(j)+'.png')
    ##print("Starting infection")
    infections = [[] for n in range(numRumors)]
    #infected = getInfectedList(Graph, numRumors)

    while (not isAllInfected(Graph, numRumors)):
        Graph = infectionForward(Graph, propagProba, numRumors)
        #infected = getInfectedList(Graph, numRumors)
        # j+1 because j=0 is step 1
        monitorTrigger = updateMonitorTrig(j + 1, monitorTrigger, monitorsList, Graph, numRumors)
        j += 1

    infected = getInfectedList(Graph, numRumors)
    ##print("----DONE")
    monitorTrigger2 = sorted(monitorTrigger, key=lambda x: (x[0], x[2]))


    HistoDict,maxStep = createHistoForMonitor(monitorTrigger2,monitorsList,numRumors)


    finalList = findAllPossibleCandidates(monitorTrigger,Graph)


    DictOfPossibleHistPerMonitor = dictOfHistoForPossibleSourcesPerMonitor(monitorsList, finalList, maxStep, propagProba, Graph)

    scoreL2, scoreChi2, numCandidat, bestCandidat = computeScores(finalList, monitorsList, DictOfPossibleHistPerMonitor, HistoDict, rumorSources)

    distToSource = len(nx.shortest_path(Graph,source=rumorSources[0],target=bestCandidat))-1

    #print("Score L2 : ", scoreL2," score chi2 : ",scoreChi2)
    #print("over ",numCandidat," possible sources")
    print("Simulation ",myI, "done")

    return scoreL2, scoreChi2, Graph, distToSource


if __name__ == '__main__':
    runHistoSimulation(1, 0.2)