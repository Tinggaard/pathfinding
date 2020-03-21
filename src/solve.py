import scheme
import rightturn
# import dijkstra
# import a_star

class Maze(scheme.Maze):

    def rightturn(self):
        return rightturn.solve(self)


    def dijkstra(self):
        pass
        # return dijkstra.solve(self)


    def a_star(self):
        pass
        # return a_star.solve(self)
