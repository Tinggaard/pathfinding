from .rightturn import solve as right
from .breadthfirst import solve as breadth
from .depthfirst import solve as depth
# from .dijkstra import solve as dijk
# from .astar import solve as ast

def rightturn(self):
    return right(self)


def breadthfirst(self):
    return breadth(self)


def depthfirst(self):
    return depth(self)


def dijkstra(self):
    # return dijk(self)
    pass


def astar(self):
    # return ast(self)
    pass
