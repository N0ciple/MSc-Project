from networkUtils import *


def generateGraphReady():
    # mGraph generation
    print("Generating mGraph")
    mGraph = generateGraph(numNodes, linkProba, 1)
    print("----- DONE\nGetting layout")
    pos = nx.spring_layout(mGraph)
    print("----- DONE\nSetting default attributes")
    mGraph = initGraphParam(mGraph, numRumors, maxThreshold)
    print("----- DONE\nChoosing the source")
    mGraph, myRumorSources = initSourceNode(mGraph, numRumors)
    print("----- DONE\nChoosing the monitoring nodes")
    mGraph, myMonitorsList = initMonitoringNodes(mGraph, numMonitors, myRumorSources, numRumors)
    print("----- DONE")
    print('Mlist : ', myMonitorsList, '\nSlist : ', myRumorSources)
    return mGraph, pos, myRumorSources, myMonitorsList

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
    
    Graph, Pos, rumorSources, monitorsList = generateGraphReady()

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

    fig2 = drawColoredGraph(Graph, Pos, numRumors, rumorSources, monitorsList)

    fig1.show()
    fig2.show()
    #plt.show()