import numpy as np

class Graph:
    def __init__(self, start: tuple, end: tuple, nodes: np.ndarray):
        assert len(nodes) > 1

        self.start = start
        self.end = end
        self.locations = nodes

        self.nodes = self.gen_graph()

    def gen_graph(self):
        pass




class Maze:
    def __init__(self, maze: np.ndarray):
        self.maze = maze

        # # shape of maze
        # try:
        #     self.x = maze.shape[1]
        #     self.y = maze.shape[0]
        # except:
        #     print('Shape of maze is not rectangular, exiting...')
        #     sys.exit(1)
        self.x = maze.shape[1]
        self.y = maze.shape[0]

        # start and end nodes for algs
        self.start = (0, np.argmax(maze[0]))
        self.end = (self.y-1, np.argmax(maze[-1]))

        self.nodes = self.get_nodes()
        self.node_count = len(self.nodes) + 2 # + start and end


    def __repr__(self) -> str:
        return str(self.maze)


    def get_nodes(self) -> np.ndarray:
        nodes = []

        # iterating the maze finding nodes
        for y, line in enumerate(self.maze[1:-1], 1):
            for x, field in enumerate(line):

                # skip if wall (0 == False)
                if not field:
                    continue

                # start and end
                # if y == 0 or y == self.y-1:
                #     continue

                # nodes around current
                up = self.maze[y-1,x]
                down = self.maze[y+1,x]
                left = self.maze[y,x-1]
                right = self.maze[y,x+1]

                horizontal = (down and up) and not (left or right)
                vertical = (left and right) and not (down or up)

                # if field is straight, skip it
                if vertical or horizontal:
                    continue

                # otherwise add it as a node
                nodes.append((y,x))

        return np.array(nodes)


    def show_nodes(self) -> None:
        tmp = self.maze.copy()
        for node in self.nodes:
            tmp[node[0], node[1]] = 8
        print(tmp)


    def to_graph(self) -> Graph:
        return Graph(self.start, self.end, self.nodes)






class Node:
    def __init__(self, loc: tuple, dist: int = np.inf):
        self.loc = loc
        self.dist = dist
