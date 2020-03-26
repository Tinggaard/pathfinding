import numpy as np

# class containing neccesary information on every node
class Node:
    def __init__(self, location: tuple):
        self.location = location # (y, x)
        # self.w = None # [node_index, dist]
        # self.s = None # [node_index, dist]
        # self.e = None # [node_index, dist]
        # self.n = None # [node_index, dist]

        # w s e n
        # [node_index, dist]
        self.nearby = [None] * 4

        self.via = None
        self.dist = np.inf

        # a*
        self.dist_goal = np.inf


    # if printing the Node class, return it's location
    def __repr__(self) -> str:
        return 'Node{}'.format(self.location)


    # two nodes are equal if they have the same location
    def __eq__(self, other) -> bool:
        return self.location == other.location


    # heapq comparison for dijkstra
    def __lt__(self, other) -> bool:
        return self.dist < other.dist


    # used to creating sets for counting explored nodes
    def __hash__(self) -> hash:
        return hash(self.location)



# class containing the whole data structure
class Graph:

    def __init__(self, maze: np.ndarray):
        self.maze = maze

        self.x = maze.shape[1]
        self.y = maze.shape[0]

        # start and end nodes for algs
        self.first = (0, np.argmax(maze[0]))
        self.last = (self.y-1, np.argmax(maze[-1]))

        self.nodes = self.get_nodes()
        self.node_count = len(self.nodes)

        # connect nodes
        self.gen_graph()

        self.start = self.nodes[0]
        self.end = self.nodes[-1]

        self.solved = False
        self.path = None


    # if printing the Graph class, return the np.ndarray structure
    def __repr__(self) -> str:
        return str(self.maze)


    # find nodes on map
    def get_nodes(self) -> list:
        nodes = [Node(self.first)]

        # iterating the maze finding nodes
        for y, line in enumerate(self.maze[1:-1], 1):
            for x, field in enumerate(line):

                # skip if wall (0 == False)
                if not field:
                    continue

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
                nodes.append(Node((y,x)))

        nodes.append(Node(self.last))
        return nodes


    # debugging function used to change number on found nodes
    def show_nodes(self) -> None:
        tmp = self.maze.copy()
        for node in self.nodes:
            tmp[node[0], node[1]] = 8
        # print(tmp)


    # function used in connection generating node connectivity
    def get_node_index(self, y, x) -> int:
        for no, node in enumerate(self.nodes):
            if node.location == (y, x):
                return no

    def get_node(self, index) -> Node:
        return self.nodes[index[0]]


    # generate graph structure to tell nearby nodes for every node
    def gen_graph(self) -> None:
        # first Node
        first = self.nodes[0]
        y, x = first.location
        for dn in range(self.y - y):
            tmp = y+dn+1
            if self.maze[tmp, x+1] or self.maze[tmp, x-1] or tmp == self.y-1:
                # south node
                first.nearby[1] = (self.get_node_index(tmp, x), dn+1)
                break

        #last Node
        last = self.nodes[-1]
        y, x = last.location
        for up in range(y):
            tmp = y-up-1
            if self.maze[tmp, x+1] or self.maze[tmp, x-1] or tmp == 0:
                # north node
                last.nearby[3] = (self.get_node_index(tmp, x), up+1)
                break

        # all other nodes
        for node in self.nodes[1:-1]:

            # current node location
            y, x = node.location

            # adjecent pixels
            above = self.maze[y-1,x]
            below = self.maze[y+1,x]
            left = self.maze[y,x-1]
            right = self.maze[y,x+1]

            if above:
                # decrement y with 1
                for up in range(y):
                    tmp = y-up-1
                    # if found start node
                    if tmp == 0:
                        node.nearby[3] = (self.get_node_index(tmp, x), up+1)
                        break
                    # if right or left are path or above is not, save length and exit
                    if self.maze[tmp, x+1] or self.maze[tmp, x-1] or not self.maze[tmp-1, x]:
                        node.nearby[3] = (self.get_node_index(tmp, x), up+1)
                        break

            if below:
                # incement y with 1
                for dn in range(self.y - y):
                    tmp = y+dn+1
                    # if found end node
                    if tmp == self.y-1:
                        node.nearby[1] = (self.get_node_index(tmp, x), dn+1)
                        break

                    # if right or left are path or below is not, save length and exit
                    if self.maze[tmp, x+1] or self.maze[tmp, x-1] or not self.maze[tmp+1, x]:
                        node.nearby[1] = (self.get_node_index(tmp, x), dn+1)
                        break

            if left:
                # decrement x with 1
                for lt in range(x):
                    tmp = x-lt-1
                    # if up or down are path or left is not, save length and exit
                    if self.maze[y+1, tmp] or self.maze[y-1, tmp] or not self.maze[y, tmp-1]:
                        node.nearby[0] = (self.get_node_index(y, tmp), lt+1)
                        break

            if right:
                # increment x with 1
                for rt in range(self.x - x):
                    tmp = x+rt+1
                    # if up or down are path or right is not, save length and exit
                    if self.maze[y+1, tmp] or self.maze[y-1, tmp] or not self.maze[y, tmp+1]:
                        node.nearby[2] = (self.get_node_index(y, tmp), rt+1)
                        break


    def show_solution(self) -> None:
        if not self.solved:
            print('Graph not solved, cannot show solution')
            return False

        sol = []
        for row in self.maze:
            tmp = []
            for val in row:
                tmp.append(str(val))

            sol.append(tmp)

        for node in self.path:
            y, x = node.location
            sol[y][x] = 'n'

        print('Solution:')
        print(''.join([' '] + [str(i) for i in range(self.y)]))
        for no, row in enumerate(sol):
            out = ''.join(row).replace('0', '▒').replace('1', ' ') # character: u"\u2592"
            print(str(no) + out)


    # remove nodes on a dead end completely
    # may implement later...
    def rm_dead_ends(self):
        # for node in self.nodes:
        #     if len(node.adj) > 2:
        #         pass
        pass
