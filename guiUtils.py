from tkinter import *
from simulation import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphView(object):

    def __init__(self,myFigList):
        self.figList = myFigList
        self.window = Tk()
        self.bouton = Button(self.window, text="Close", command=self.window.quit)
        self.bouton.pack()
        self.window.mainloop()
        self.curIndex = 0
        self.canvas = FigureCanvasTkAgg(self.figList[self.curIndex], master=self.window)



if __name__ == '__main__':

    numRumors = 1
    maxThreshold = 1
    numMonitors = 10
    propagProba = 1
    numNodes = 50
    linkProba = 0.2
    monitorTrigger = list()
    numStep = 100

    Graph, Pos, rumorSources, monitorsList = generateGraphReady(numNodes, linkProba, maxThreshold, numRumors,
                                                                numMonitors)

