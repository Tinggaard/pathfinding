import scheme
import algs

class Maze(scheme.Maze):

    def rightturn(self):
        return algs.rightturn(self)


    def breadthfirst(self):
        return algs.breadthfirst(self)


    def depthfirst(self):
        return algs.depthfirst(self)


    def dijkstra(self):
        return algs.dijkstra(self)


    def astar(self):
        return algs.astar(self)
