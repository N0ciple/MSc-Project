from networkUtils import *


def generateGraphReady(myNumNodes,myLinkProba,myMaxThreshold,myNumRumors,myNumMonitors,):
    # mGraph generation
    print("Generating mGraph")
    mGraph = generateGraph(myNumNodes, myLinkProba, 1)
    print("----- DONE\nGetting layout")
    pos = nx.spring_layout(mGraph)
    print("----- DONE\nSetting default attributes")
    mGraph = initGraphParam(mGraph, myNumRumors, myMaxThreshold)
    print("----- DONE\nChoosing the source")
    mGraph, myRumorSources = initSourceNode(mGraph, myNumRumors)
    print("----- DONE\nChoosing the monitoring nodes")
    mGraph, myMonitorsList = initMonitoringNodes(mGraph, myNumMonitors, myRumorSources, myNumRumors)
    print("----- DONE")
    print('Mlist : ', myMonitorsList, '\nSlist : ', myRumorSources)

    return mGraph, pos, myRumorSources, myMonitorsList

def updateMonitorTrig(curStep,myMonitorTrigger,myMonitorList,myG,myNumRum):
    for k in myMonitorList:
        for l in range(myNumRum):
            if myG.node[k]['infected' + str(l + 1)] and not myG.node[k]['detected' + str(l + 1)]:
                myMonitorTrigger.append((k, l + 1, curStep))
                myG.node[k]['detected' + str(l + 1)] = True
                # Sort by monitoring node and by rumour index

        myMonitorList = sorted(myMonitorTrigger, key=lambda x: (x[0], x[1]))
    return myMonitorList

def printMonitorTrig(myMonitorTrig):
    print('\nMonitoring Nodes :')
    prev = 0
    for i in myMonitorTrig:
        if prev == 0 or i[0] != prev:
            print('Monitoring node number : ', i[0], '\n\tinfected by rumor : ', i[1], '\tat step : ', i[2])
            prev = i[0]
        else:
            print('\tinfected by rumor : ', i[1], '\tat step : ', i[2])
            prev = i[0]
    return None

def findSet(myG,mySourceNode,myRadius):
    possible_set = list()
    curSet = findNeighDegN(myG,mySourceNode,myRadius)

    return  curSet






if __name__ == '__main__':

    figureList = list()
    # Parameters definition
    numRumors = 4
    maxThreshold = 1
    numMonitors = 10
    propagProba = 1
    numNodes = 50
    linkProba = 0.2
    monitorTrigger = list()
    numStep = 100



    Graph, Pos, rumorSources, monitorsList = generateGraphReady(numNodes,linkProba,maxThreshold,numRumors,numMonitors)

    fig1 =  drawColoredGraph(Graph, Pos, numRumors, rumorSources, monitorsList)

    figureList.append(fig1)

    print("Starting infection")
    infections = [[] for n in range(numRumors)]



    for j in range(5):
        print("====================================================\n\n\n\n\n\n\n\n====================================================")

        for i in Graph.nodes():
            if i in monitorsList:
                print("Node ",str(i),"\t",Graph.node[i])

        Graph = infectionForward(Graph, propagProba, numRumors)

        monitorTrigger = updateMonitorTrig(j,monitorTrigger,monitorsList,Graph,numRumors)

        print(monitorTrigger)
        printMonitorTrig(monitorTrigger)

        fig2 = drawColoredGraph(Graph, Pos, numRumors, rumorSources, monitorsList)
        #fig2.show()
    plt.show()

