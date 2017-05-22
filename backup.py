import networkx as nx
import matplotlib.pyplot as plt
import random

def initGraphParam(myG,myNumRum,myThreshMax):
    for i in range(myNumRum):
        nx.set_node_attributes(Graph, 'infected'+str(i+1), False)
        nx.set_node_attributes(Graph, 'counter'+str(i+1), 0)
    nx.set_node_attributes(Graph, 'threshold', 1)
    for i in myG.nodes():
        myG.node[i]['threshold'] = random.randint(1,myThreshMax)

    return myG


def initSourceNode(myG,myNumRum):
    nodeList = myG.nodes()
    sources = []
    index = random.choice(nodeList)
    for i in range(myNumRum):
        myG.node[index]['infected'+str(i+1)] = 1
        sources.append(index)
    sources = list(set(sources))
    return myG, sources


def initNodesState(myG):
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


def drawColoredGraph(myG,myPos,myNumRum,mySources):
    infect, notInfect = colorList(myG,myNumRum)
    nx.draw_networkx_nodes(myG,myPos,infect,node_color='r',node_size=15)
    nx.draw_networkx_nodes(myG, myPos, notInfect, node_color='g',node_size=5)
    nx.draw_networkx_nodes(myG, myPos, mySources, node_color='b', node_size=5)
    nx.draw_networkx_edges(myG, myPos, width=1.0,alpha=0.1)


    plt.show()
    return None


def infectionForward(myG, myProba, myNumRum):
    myG2 = myG
    for k in range(myNumRum):
        for i in myG.nodes():
            if myG.node[i]['infected'+str(k+1)]:
                neiList = myG.neighbors(i)
                for j in neiList:
                    if random.random() < myProba:
                        myG2.node[j]['counter'+str(k+1)] +=1
        for l in myG2.nodes():
            if myG2.node[l]['counter'+str(k+1)] >= myG2.node[l]['threshold']:
                myG2.node[l]['infected' + str(k + 1)] = True

    return myG2

def estimateInfected(myG,myNumRum,myRumId):
    counter = 0

    for i in myG.nodes():
        if myG.node[i]['infected'+str(myRumId)]:
            counter +=1

    return counter


def getInfectedList (myG,myNumRum):

    infected = []
    for j in range(myNumRum):
        for i in myG.nodes():
            if myG.node[i]['infected'+str(j+1)]:
                infected.append(i)
    infected = list(set(infected))

    return infected



if __name__ == '__main__':
    numRumors = 4
    maxThreshold = 3

    print("Generating graph")

    # Small World
    #Graph = nx.watts_strogatz_graph(200,5,0.1)

    # Tree
    #Graph = nx.balanced_tree(5,3)

    # Random Graph
    Graph = nx.watts_strogatz_graph(200,5,0.1)

    # Random - power Law
    #Graph = nx.random_powerlaw_tree()

    #Karate club
    #Graph = nx.karate_club_graph()

    #Scale Free Graph
    #Graph = nx.scale_free_graph(100).to_undirected()

    print("----- DONE")

    print("Getting layout")
    pos = nx.spring_layout(Graph)
    print("----- DONE")
    print("Setting default attributes")
    Graph = initGraphParam(Graph,numRumors,maxThreshold)


    print("----- DONE")
    print("Choosing the source")
    Graph, rumorSources = initSourceNode(Graph,numRumors)
    print("----- DONE")

    drawColoredGraph(Graph,pos,numRumors,rumorSources)

    print("Starting infection")
    infections = [[] for n in range(numRumors)]
    for i in range(50):
        Graph = infectionForward(Graph,0.5,numRumors)


        for j in range(numRumors):
            infections[j].append(100*estimateInfected(Graph,numRumors,j+1)/len(Graph))

        if i%10 == 0 :
            drawColoredGraph(Graph, pos,numRumors,rumorSources)
            for k in range(numRumors):
                print("Infected  by ", k+1 ,": ",100*estimateInfected(Graph,numRumors,k+1)/len(Graph),"%"," - ",estimateInfected(Graph,numRumors,k+1))
            print('----------')
        print(getInfectedList(Graph,numRumors))




    for i in range(numRumors):
        plt.plot(infections[i], label='Rumor '+str(i+1))

    plt.title('Percentage of the nodes infected for each rumor')
    plt.legend()
    plt.show()











