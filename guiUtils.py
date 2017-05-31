from tkinter import *

from matplotlib.figure import Figure

from simulation import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


class GraphView(object):

    def __init__(self,myFigList):
        self.figList = myFigList
        self.window = Tk()
        self.bouton = Button(self.window, text="Close", command=self.window.quit)
        self.bouton.pack()
        self.curIndex = 0
        self.canvas = FigureCanvasTkAgg(self.figList[self.curIndex], master=self.window)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.window)
        self.toolbar.update()
        self.window.mainloop()



    def getListInfo(self):
        self.figList[self.curIndex].show()
        plt.show()


    def draw(self):
        self.canvas.draw()
        self.window.mainloop()






if __name__ == '__main__':

    figureList = list()
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

    fig1 = drawColoredGraph(Graph, Pos, numRumors, rumorSources, monitorsList)
    #fig1.show()
    #plt.show()

    #f = Figure(figsize=(5, 5), dpi=100)
    #a = f.add_subplot(111)
    #a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])


    figureList.append(fig1)

    a = GraphView([fig1])

    #a.draw()
    #a.getListInfo()
