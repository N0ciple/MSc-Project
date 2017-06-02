# TO DO :
# DONE - fix the counter/threshold
# DONE - 1 source for all the rumors
# - Dikjjtra algorithm to find candidate
#   for the source then combine the results.

import matplotlib.pyplot as plt
import networkx as nx
plt.figure(figsize=(100,100))
import random
import numpy as np


def generateGraph(myNumNodes,myLinkProba,myGraphType):

    myGraphType = myGraphType%6

    myGraph = nx.karate_club_graph()

    if myGraphType == 1:
        # Small World
        myGraph = nx.watts_strogatz_graph(myNumNodes, 5, 0.2)
    if myGraphType == 2:
        # Tree
        myGraph = nx.balanced_tree(5,3)
    if myGraphType == 3:
        # Random Graph
        myGraph = nx.fast_gnp_random_graph(myNumNodes, 2*1/myNumNodes)
    if myGraphType == 4:
        # Random - power Law
        myGraph = nx.random_powerlaw_tree()
    if myGraphType == 5:
        # Karate club
        myGraph = nx.karate_club_graph()
    if myGraphType == 6:
        # Scale Free Graph
        myGraph = nx.scale_free_graph(myNumNodes).to_undirected()

    return myGraph

# Initiate the parameters of the graph
def initGraphParam(myG,myNumRum,myThreshMax):
    for i in range(myNumRum):
        nx.set_node_attributes(myG, 'infected'+str(i+1), False)   # Init infection state
        nx.set_node_attributes(myG, 'counter'+str(i+1), 1)
        for j in myG.nodes():
            myG.node[j]['counter'+str(i+1)] = list()                # Generate infector list

    nx.set_node_attributes(myG, 'threshold', 1)
    for i in myG.nodes():
        myG.node[i]['threshold'] = random.randint(1,myThreshMax)    # Init threshold
    return myG

# Initiate the source of the rumours
def initSourceNode(myG,myNumRum):
    nodeList = myG.nodes()
    sources = []
    index = random.choice(nodeList)
    for i in range(myNumRum):
        myG.node[index]['infected'+str(i+1)] = 1
        sources.append(index)
    sources = list(set(sources))
    return myG, sources


def initMonitoringNodes(myG,myMonitorNum,mySources,myNumRum):
    nodeList = myG.nodes()
    monitorList = list()

    for i in range(myMonitorNum):
        monitorList.append(random.choice(nodeList))

    while len(list(set(monitorList))) != myMonitorNum and len(set(mySources).intersection(set(monitorList))) != 0 :
        monitorList = list()
        for i in range(myMonitorNum):
            monitorList.append(random.choice(nodeList))
    for i in  monitorList:
        for k in range(myNumRum):
            myG.node[i]['detected'+str(k+1)] = False

    return myG,monitorList


    return myG

def colorList(myG,myNumRum):
    infected=[]
    notInfected=[]
    for j in range(myNumRum):
        for i in myG.nodes():
            if myG.node[i]['infected'+str(j+1)]:
                infected.append(i)
            else :
                notInfected.append(i)
    return infected, notInfected


def drawColoredGraph(myG,myPos,myNumRum,mySources,myMonitors=None,myIndex=None):
    infect, notInfect = colorList(myG,myNumRum)
    if myMonitors != None:
        nx.draw_networkx_nodes(myG, myPos, myMonitors, node_color='c', node_size=40)
    nx.draw_networkx_nodes(myG, myPos, infect, node_color='r', node_size=15)
    nx.draw_networkx_nodes(myG, myPos, notInfect, node_color='g', node_size=5)
    nx.draw_networkx_nodes(myG, myPos, mySources, node_color='b', node_size=5)
    nx.draw_networkx_edges(myG, myPos, width=1.0,alpha=0.1)
    #myFig = plt.figure()
    if myIndex != None:
        plt.savefig('./TestFigs/figT' + str(myIndex) + '.png')
    plt.show()
    #return myFig
    return None


def drawColoredGraph2(myG,myPos,myNumRum,mySources,myMonitors,myDetected):
    infect, notInfect = colorList(myG,myNumRum)
    nx.draw_networkx_nodes(myG, myPos, infect, node_color='r', node_size=15)
    nx.draw_networkx_nodes(myG, myPos, notInfect, node_color='g', node_size=5)
    nx.draw_networkx_nodes(myG, myPos, myMonitors, node_color='c', node_size=40)
    nx.draw_networkx_nodes(myG, myPos, myDetected, node_color='y', node_size=50)
    nx.draw_networkx_nodes(myG, myPos, mySources, node_color='b', node_size=5)
    nx.draw_networkx_edges(myG, myPos, width=1.0,alpha=0.1)
    #myFig = plt.figure()
    plt.savefig('./TestFigs/figEnd.png')
    plt.show()
    #return myFig
    return None





def infectionForward(myG, myProba, myNumRum):
    myG2 = myG

    for k in range(myNumRum):
        for i in myG.nodes():
            if myG.node[i]['infected'+str(k+1)]:
                neiList = myG.neighbors(i)
                # print('node ',i,' neighbors = ',neiList)
                for j in neiList:
                    if random.random() < myProba:
                        myG2.node[j]['counter'+str(k+1)].append(i)
                        # print(myG2.node[j]['counter' + str(k + 1)])
                        myG2.node[j]['counter' + str(k + 1)] = list(set(myG2.node[j]['counter'+str(k+1)]))
                        # print(myG2.node[j]['counter' + str(k + 1)])
        for l in myG2.nodes():
            if len(myG2.node[l]['counter'+str(k+1)]) >= myG2.node[l]['threshold']:
                # print('debug node ',l,'rumor : ',k,' counter : ', myG2.node[l]['counter'+str(k+1)], ' th : ',myG2.node[l]['threshold'])
                # print('infectors for ',l, ' = ',myG2.node[l]['counter'+str(k+1)])
                myG2.node[l]['infected' + str(k + 1)] = True

    return myG2


def getInfectedList (myG,myNumRum):

    infected = []
    for j in range(myNumRum):
        for i in myG.nodes():
            if myG.node[i]['infected'+str(j+1)]:
                infected.append(i)
    infected = list(set(infected))

    return infected

def isAllInfected(myG,myNumRum):
    myBool = True
    for j in range(myNumRum):
        for i in myG.nodes():
            if not myG.node[i]['infected'+str(j+1)]:
                myBool = False
    return myBool



def estimateInfected(myG,myNumRum,myRumId):
    counter = 0

    for i in myG.nodes():
        if myG.node[i]['infected'+str(myRumId)]:
            counter +=1

    return counter

def findNeighDegN(myG, mySource, myDeg):
    path_lengths = nx.single_source_dijkstra_path_length(myG, mySource)
    neigh = [node for node, length in path_lengths.items() if length == myDeg]
    return  neigh




def findPossibleSets(myG,mySources,myTrig,myNumRum):
    possibleSets = []
    for s in myTrig:
        curDeg = s[2]
        while curDeg > 1 :
            curSet = findNeighDegN(myG,s[0],curDeg)
            curDeg -= 1
        #print('node : ',s[0],' rumor : ',s[1],' degree : ',s[2],'curSet : ',curSet)
        possibleSets.append(curSet)
    print(possibleSets)


    initSet = set(possibleSets[0])
    for i in range(len(possibleSets)-1):
        initSet = initSet.intersection(possibleSets[i+1])
    return list(initSet)

    #array = np.zeros((len(myG.nodes()),1))
    #for i in possibleSets :
    #    for j in i:
    #        array[j]+=1
    #plt.hist(array,bins=len(myG.nodes()))
    #plt.show()


def findPossibleSets2(myG,mySources,myTrig,myNumRum):
    possibleSets = []
    for s in myTrig:
        curDeg =s[2]
        while curDeg>1:
            curSet = findNeighDegN(myG,s[0],curDeg)
            #print('debuuuug : ',s[0],' set : ', curSet)
            #print(curDeg)
            curDeg-=1
        #print(curSet)
        #print('node : ',s[0],' rumor : ',s[1],' degree : ',s[2],'curSet : ',curSet)
            if len(curSet)>0:
                possibleSets.append(curSet)
    print(possibleSets)
    #print(type(possibleSets[0]))

    #initSet = set(possibleSets[0])
    #for i in range(len(possibleSets)-1):
    #    initSet = initSet.intersection(possibleSets[i+1])
    #return list(initSet)

    array = np.zeros((len(myG.nodes()),1))
    for i in possibleSets :
        #print('debG ',i)
        for j in i:
            array[j]+=1
    arrayAsList = array.tolist()
    maxVal = max(arrayAsList)
    print(array)
    print('Source : ',mySources[0],' Max : ',max(arrayAsList), ' value : ',arrayAsList[mySources[0]])
    posList = list()
    for i in range(len(array)):
        if maxVal == array[i]:
            posList.append(i)
    return posList




# if __name__ == '__main__':
#     numRumors = 4
#     maxThreshold = 1
#     numMonitors = 3
#     propagProba = 0.05
#     numNodes = 200
#     monitorTrigger = list()
#     numStep = 100
#
#     print("Generating graph")
#
#     # Small World
#     Graph = nx.watts_strogatz_graph(numNodes, 5, 0.2)
#
#     # Tree
#     # Graph = nx.balanced_tree(5,3)
#
#     # Random Graph
#     # Graph = nx.fast_gnp_random_graph(numNodes, 2*1/numNodes)
#
#     # Random - power Law
#     # Graph = nx.random_powerlaw_tree()
#
#     # Karate club
#     # Graph = nx.karate_club_graph()
#
#     # Scale Free Graph
#     # Graph = nx.scale_free_graph(100).to_undirected()
#
#     print("----- DONE")
#
#     print("Getting layout")
#     pos = nx.spring_layout(Graph)
#     print("----- DONE")
#     print("Setting default attributes")
#     Graph = initGraphParam(Graph,numRumors,maxThreshold)
#
#
#     print("----- DONE")
#     print("Choosing the source")
#     Graph, rumorSources = initSourceNode(Graph,numRumors)
#     print("----- DONE")
#
#     print('Choosing the monitoring nodes')
#     Graph, monitorsList = initMonitoringNodes(Graph,numMonitors,rumorSources,numRumors)
#     print("----- DONE")
#     print('Mlist : ', monitorsList,'\nSlist : ',rumorSources)
#
#     drawColoredGraph(Graph,pos,numRumors,rumorSources,monitorsList)
#
#     print("Starting infection")
#     infections = [[] for n in range(numRumors)]
#
#     for i in range(numStep):
#         Graph = infectionForward(Graph,propagProba,numRumors)
#
#
#         for j in range(numRumors):
#             infections[j].append(100*estimateInfected(Graph,numRumors,j+1)/len(Graph))
#
#
#         for k in monitorsList :
#             for l in range(numRumors):
#                 if Graph.node[k]['infected'+str(l+1)] and not Graph.node[k]['detected'+str(l+1)]:
#                     monitorTrigger.append((k,l+1,i))
#                     Graph.node[k]['detected' + str(l + 1)]=True
#
#         if i%floor(numStep*10/100) == 0 :
#             drawColoredGraph(Graph, pos,numRumors,rumorSources,monitorsList)
#             for k in range(numRumors):
#                 print("Infected  by ", k+1 ,": ",100*estimateInfected(Graph,numRumors,k+1)/len(Graph),"%"," - ",estimateInfected(Graph,numRumors,k+1))
#             print('---------- step : ',i)
#
#
#     # Sort by monitoring node and by rumour index
#     monitorTrigger = sorted(monitorTrigger, key=lambda x : (x[0], x[1]))
#     #print('monitoring ', monitorTrigger)
#     print('\nMonitoring Nodes :')
#     prev = 0
#     for i in monitorTrigger:
#         if prev == 0 or i[0] != prev :
#             print('Monitoring node number : ',i[0],'\n\tinfected by rumor : ',i[1],'\tat step : ',i[2])
#             prev = i[0]
#         else :
#             print('\tinfected by rumor : ',i[1],'\tat step : ',i[2])
#             prev=i[0]
#
#
#
#
#     posSets = findPossibleSets2(Graph,rumorSources,monitorTrigger,numRumors)
#     print('possible Sets : ',posSets)
#
#     for i in range(numRumors):
#         plt.plot(infections[i], label='Rumor '+str(i+1))
#
#     plt.title('Percentage of the nodes infected for each rumor')
#     plt.legend()
#     plt.show()











