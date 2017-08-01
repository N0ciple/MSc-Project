from simulation import *
from scipy.special import comb
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


################ STEP 1
    # Generate an graph with rumor spread

# Parameters definition
numRumors = 10
maxThreshold = 1
numMonitors = 50
propagProba = 0.2
numNodes = 500
linkProba = 0.2
monitorTrigger = list()
numStep = 100

j = 0

Graph, Pos, rumorSources, monitorsList = generateGraphReady(numNodes, linkProba, maxThreshold, numRumors, numMonitors)
# fig1.savefig('./TestFigs/figT'+str(j)+'.png')
print("Starting infection")
infections = [[] for n in range(numRumors)]
#infected = getInfectedList(Graph, numRumors)

while (not isAllInfected(Graph, numRumors)):
    Graph = infectionForward(Graph, propagProba, numRumors)
    #infected = getInfectedList(Graph, numRumors)
    # j+1 because j=0 is step 1
    monitorTrigger = updateMonitorTrig(j + 1, monitorTrigger, monitorsList, Graph, numRumors)
    j += 1

infected = getInfectedList(Graph, numRumors)
print("----DONE")
monitorTrigger2 = sorted(monitorTrigger, key=lambda x: (x[0], x[2]))






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









################ STEP 3
    # Find all possible candidates based on set intersections


setList = []

for i in monitorTrigger:
    nodeSet = findSet2(Graph, i[0], i[2])
    setList.append(nodeSet)

finalSet = set.intersection(*setList)
print("Real Source = ", rumorSources[0])
print("Detected Source = ", list(finalSet))
finalList = list(finalSet)






################ STEP 4
    # Create the histogram for each monitoring node, for each possible source
    # i.e. Step 1: the whole graph, Step 2: only the possible sources determined with set intersection.


#Benchmarking of the metrics

scoreL2 = []
scoreChi2 = []

DictOfPossibleHistPerMonitor = {}
for monitor in monitorsList:
    sourceHisto = {}
    monitorToTest = monitor

    for source in finalList:
        if source not in monitorsList :
            sourceHisto[source]=np.zeros((maxStep+1,1))
            for i in range(0,maxStep+1):
                sourceHisto[source][i] = calculProba(propagProba,len(nx.shortest_path(Graph,source,monitorToTest))-1,i)
    DictOfPossibleHistPerMonitor[monitor] = sourceHisto



################ STEP 5
    # Compute scores

    dList = []
    dListChi = []

    for i in finalList:
        if i not in monitorsList:
            # plt.bar(range(0,maxStep+1),sourceHisto[i])
            # plt.show()
            d = np.linalg.norm(sourceHisto[i] - HistoDict[monitorToTest])
            d2 = chiDist(sourceHisto[i], np.transpose(HistoDict[monitorToTest][np.newaxis]))
            dList.append((i, d))
            dListChi.append((i, d2))
            # print("Dist =",d)
    dListSorted = sorted(dList, key=lambda x: x[1])
    dListChiSorted = sorted(dListChi, key=lambda x: x[1])

    classement = [v[0] for v in dListSorted]
    classementChi = [v[0] for v in dListChiSorted]

    print(rumorSources)
    scoreL2.append(classement.index(rumorSources[0]))
    scoreChi2.append(classementChi.index(rumorSources[0]))

    print("classment de la source (L2) ", classement.index(rumorSources[0]))
    print("\tclassment de la source (Chi) ", classementChi.index(rumorSources[0]))

print("\n\n=====================\nscore moyen L2", np.mean(scoreL2))
print("score moyen Chi2",np.mean(scoreChi2))