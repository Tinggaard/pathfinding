import numpy as np
# class containing neccesary information on every node
class Node:
    def __init__(self, location: tuple):
        self.location = location # (y, x)

        # w s e n
        # [location, dist]
        self.nearby = [None] * 4

        # location of node travelled by
        self.via = None
        # tracking distance travelled
        self.dist = np.inf

        # a*
        self.dist_goal = np.inf

        # set to be combined self.dist_goal and self.dist
        self.combined = np.inf


    # if printing the Node class, return it's location
    def __repr__(self) -> str:
        return 'Node{}'.format(self.location)


    # two nodes are equal if they have the same location
    def __eq__(self, other) -> bool:
        return self.location == other.location


    # heapq comparison for dijkstra and a*
    def __lt__(self, other) -> bool:
        return self.combined < other.combined


    # used to creating sets for counting explored nodes
    def __hash__(self) -> hash:
        return hash(self.location)


    # # iterate the neighbours
    # def __iter__(self):
    #     pass
    #
    # # self.location[index]
    # def __getitem__(self, index):
    #     pass
