import numpy as np
from networkUtils import *



def chiDist(histo1, histo2):
    PmQ2 = np.power(histo1 - histo2, 2)

    # prevent 0 values in division
    histo1[histo1 == 0] = np.finfo(float).eps
    histo2[histo2 == 0] = np.finfo(float).eps
    PpQ = histo1 + histo2
    vectRes = np.divide(PmQ2, PpQ)
    res = np.sum(vectRes)
    return np.sqrt(res)


def createHistoForMonitor(monitorTrigger2,monitorsList,numRumors):
    ################ STEP 2
    # Create the histogram of rumor reception step for each monitoring node

    # Find the maximum number of steps :
    maxStep = -1
    for step in monitorTrigger2:
        if step[2] > maxStep:
            maxStep = step[2]

    # create array for each monitoring node
    HistoDict = dict()

    # Fill in the array
    for monitor in monitorsList:
        HistoDict[monitor] = np.zeros((maxStep + 1, 1))
        for elem in monitorTrigger2:
            if monitor == elem[0]:
                HistoDict[monitor][elem[2]] += 1
        HistoDict[monitor] = np.cumsum(HistoDict[monitor]) / numRumors

    return HistoDict,maxStep



def findAllPossibleCandidates(monitorTrigger,Graph):

    ################ STEP 3
    # Find all possible candidates based on set intersections

    setList = []

    for i in monitorTrigger:
        nodeSet = findSet2(Graph, i[0], i[2])
        setList.append(nodeSet)

    finalSet = set.intersection(*setList)
    ##print("Real Source = ", rumorSources[0])
    ##print("Detected Source = ", list(finalSet))
    finalList = list(finalSet)

    return finalList




def dictOfHistoForPossibleSourcesPerMonitor(monitorsList,finalList,maxStep,propagProba,Graph):


    ################ STEP 4
    # Create the histogram for each monitoring node, for each possible source
    # i.e. Step 1: the whole graph, Step 2: only the possible sources determined with set intersection.


    # Benchmarking of the metrics

    #detectedList =[]
    #scoreL2 = []
    #scoreChi2 = []

    DictOfPossibleHistPerMonitor = {}
    for monitor in monitorsList:
        sourceHisto = {}
        monitorToTest = monitor
        for source in finalList:
            if source not in monitorsList:
                sourceHisto[source] = np.zeros((maxStep + 1, 1))
                for i in range(0, maxStep + 1):
                    sourceHisto[source][i] = calculProba(propagProba,
                                                         len(nx.shortest_path(Graph, source, monitorToTest)) - 1, i)
        DictOfPossibleHistPerMonitor[monitor] = sourceHisto


    return DictOfPossibleHistPerMonitor



def computeScores(finalList,monitorsList,DictOfPossibleHistPerMonitor,HistoDict,rumorSources):

    scoreDictL2 = {}
    scoreDictChi2 = {}
    for i in finalList:
        scoreDictL2[i] = 0
        scoreDictChi2[i] = 0

    for monitorToTest in monitorsList:
        monitorRankingL2 = []
        monitorRankingChi2 = []

        for source in finalList:

            if source not in monitorsList:

                d = np.linalg.norm(DictOfPossibleHistPerMonitor[monitorToTest][source] - HistoDict[monitorToTest])
                d2 = chiDist(DictOfPossibleHistPerMonitor[monitorToTest][source], np.transpose(HistoDict[monitorToTest][np.newaxis]))
                monitorRankingL2.append((source,d))
                monitorRankingChi2.append((source,d2))
        print("step 0",monitorRankingL2)

        monitorRankingL2 = sorted(monitorRankingL2, key=lambda x: x[1])
        monitorRankingChi2 = sorted(monitorRankingChi2, key=lambda x: x[1])
        print("step 1",monitorRankingL2)

        monitorRankingL2 = [ elem[0] for elem in monitorRankingL2]
        monitorRankingChi2 = [ elem[0] for elem in monitorRankingChi2]
        print("step 2",monitorRankingL2)

        for i in finalList :
            if i not in monitorsList:
                scoreDictL2[i] += monitorRankingL2.index(i)
                scoreDictChi2[i] += monitorRankingChi2.index(i)
                print("step 3", scoreDictL2)

    scoreListL2 = sorted( scoreDictL2.items(),key=lambda x: x[1])
    scoreListChi2 = sorted( scoreDictChi2.items(),key=lambda x: x[1])
    print("step 4",scoreListL2)
    scoreListL2 = [ elem[0] for elem in scoreListL2]
    scoreListChi2 = [elem[0] for elem in scoreListChi2]
    print("step 5",scoreListL2)
    return  scoreListL2.index(rumorSources[0]),scoreListChi2.index(rumorSources[0]),len(finalList)