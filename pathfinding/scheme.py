# std lib
import sys
import os.path
from time import time

# 3rd party
import click
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera

# 1st party
from pathfinding import algs


# vars for determining filetype
IMAGE = 1
TEXT = 2
VIDEO = 3


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


# class containing the whole data structure
class Graph:
    def __init__(self, maze: np.ndarray):
        self.maze = maze
        self.animate = False

        self.x = maze.shape[1]
        self.y = maze.shape[0]

        # start and end nodes for algs
        self.first = (0, np.argmax(maze[0]))
        self.last = (self.y-1, np.argmax(maze[-1]))

        self.nodes = self.get_nodes()
        self.node_count = len(self.nodes)

        self.start = self.nodes[self.first] # Node(self.first)
        self.end = self.nodes[self.last] # Node(self.last)

        # connect nodes
        self.gen_graph()

        self.solved = False
        self.path = None


    # if printing the Graph class, return the np.ndarray structure
    def __repr__(self) -> str:
        return str(self.maze)


    # find nodes on map
    def get_nodes(self) -> dict:
        # initiate dict
        nodes = {self.first: Node(self.first), self.last: Node(self.last)}

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
                nodes[(y,x)] = Node((y,x))

        return nodes


    # used to get a node, from a specified index
    # hashes the location, and finds the node
    def get_node(self, location: tuple) -> Node:
        return self.nodes[location]


    # generate graph structure to tell nearby nodes for every node
    def gen_graph(self) -> None:
        # first Node
        first = self.start
        y, x = first.location
        for dn in range(self.y - y):
            tmp = y+dn+1
            if self.maze[tmp, x+1] or self.maze[tmp, x-1] or tmp == self.y-1:
                # south node
                first.nearby[1] = ((tmp, x), dn+1)
                break

        #last Node
        last = self.end
        y, x = last.location
        for up in range(y):
            tmp = y-up-1
            if self.maze[tmp, x+1] or self.maze[tmp, x-1] or tmp == 0:
                # north node
                last.nearby[3] = ((tmp, x), up+1)
                break

        # all other nodes
        # skip the first and last node (first two declared)
        for node in self.nodes.values():

            # if the first or last node, skip
            if node.location[0] == 0 or node.location[0] == self.y - 1:
                continue

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
                        node.nearby[3] = ((tmp, x), up+1)
                        break
                    # if right or left are path or above is not, save length and exit
                    if self.maze[tmp, x+1] or self.maze[tmp, x-1] \
                        or not self.maze[tmp-1, x]:

                        node.nearby[3] = ((tmp, x), up+1)
                        break

            if below:
                # incement y with 1
                for dn in range(self.y - y):
                    tmp = y+dn+1
                    # if found end node
                    if tmp == self.y-1:
                        node.nearby[1] = ((tmp, x), dn+1)
                        break

                    # if right or left are path or below is not, save length and exit
                    if self.maze[tmp, x+1] or self.maze[tmp, x-1] \
                        or not self.maze[tmp+1, x]:

                        node.nearby[1] = ((tmp, x), dn+1)
                        break

            if left:
                # decrement x with 1
                for lt in range(x):
                    tmp = x-lt-1
                    # if up or down are path or left is not, save length and exit
                    if self.maze[y+1, tmp] or self.maze[y-1, tmp] \
                        or not self.maze[y, tmp-1]:

                        node.nearby[0] = ((y, tmp), lt+1)
                        break

            if right:
                # increment x with 1
                for rt in range(self.x - x):
                    tmp = x+rt+1
                    # if up or down are path or right is not, save length and exit
                    if self.maze[y+1, tmp] or self.maze[y-1, tmp] \
                        or not self.maze[y, tmp+1]:

                        node.nearby[2] = ((y, tmp), rt+1)
                        break



    # used to write image, used in assignment...
    def save_nodes(self, destination: str):
        writable = self.maze.copy()*255

        # make array 3D
        writable = writable[..., np.newaxis]
        writable = np.concatenate((writable, writable, writable), axis=2)

        for location in self.nodes.keys():
            writable[location] = np.array([255, 0, 0])

        Image.fromarray(writable).save(destination)



    # decorator, to check if solved flag is set...
    def _solved(func):
        def checker(self, *args, **kwargs):
            if self.solved:
                return func(self, *args, **kwargs)
            click.secho('ERROR: Graph not solved, cannot show solution', fg='red', err=True)
        return checker


    # convenient function that reads the filetype, and the save it as an image
    @_solved
    def save_solution(self, destination: str, extension: int) -> None:

        if extension == IMAGE:
            return self._save_solution_img(destination)

        elif extension == TEXT:
            self._save_solution_text(destination)

        elif extension == VIDEO:
            return self._save_solution_vid(destination)


    # write maze solution to disk as image
    def _save_solution_img(self, destination: str) -> None:
        mz = self.maze.copy()*255

        # make array 3D
        mz = mz[..., np.newaxis]
        mz = np.concatenate((mz, mz, mz), axis=2)

        count = len(self.path)

        for i in range(count - 1):
            c = self.path[i].location #current
            n = self.path[i+1].location #next

            # red -> green
            val = int((i/count)*255)
            bgr = [255 - val, val, 0]

            # y vals are the same: going horizontal
            if c[0] == n[0]:
                for loc in range(min(c[1], n[1]), max(c[1], n[1]) + 1):
                    mz[c[0], loc] = bgr

            # x vals are the same: going vertical
            else:
                for loc in range(min(c[0], n[0]), max(c[0], n[0]) + 1):
                    mz[loc, c[1]] = bgr

        Image.fromarray(mz).save(destination)


    def _save_solution_txt(self, destination: str) -> None:
        sol = []
        # create normal python list, that are type independent
        for row in self.maze:
            tmp = []
            for val in row:
                tmp.append(str(val))
            sol.append(tmp)

        # if fancy flag not set
        if not fancy:
            for node in self.path:
                y, x = node.location
                sol[y][x] = 'n'
            # create (and truncate) file
            with open(destination, 'w+') as f:
                # create normal python list, that are type independent
                for line in sol:
                    f.write(''.join(line).replace('0', '#').replace('1', ' ') + '\n')
            return


    def _save_solution_vid(self, destination: str):
        assert self.animate

        for _ in range(20): # video finishes too early - cannot see solution
            plt.imshow(self.mz)
            self.cam.snap()
        count = len(self.cam._photos)
        if count > 2000:
            click.confirm(f'Videofile will take some time to render, due to the amount of frames in solution ({count} frames in total), continue?', abort=True)
        anim = self.cam.animate(blit=True, interval=30)
        anim.save(destination)


    # set the animate var to true
    def visualize(self):
        if self.x * self.y >= 100000:
            click.confirm('Maze is very large, are you sure you want to animate it?', abort=True)

        self.animate = True

        self.mz = self.maze.copy()*255
        # make array 3D
        self.mz = self.mz[..., np.newaxis]
        self.mz = np.concatenate((self.mz, self.mz, self.mz), axis=2)

        # colors
        self.EXPLORED = np.array([255, 0 , 0], dtype=np.uint8) #red
        self.CURRENT = np.array([255, 255, 0], dtype=np.uint8) #green
        self.PARENT = np.array([0, 255, 0], dtype=np.uint8) # green
        self.mz[self.last] = np.array([0, 0, 255], dtype=np.uint8) #blue

        self.cam = Camera(plt.figure())

        self.implot = plt.imshow(self.mz, interpolation='nearest', aspect='equal', vmin=0, vmax=255, cmap="RdBu")
        self.implot.set_cmap('hot')
        plt.axis('off')
        self.cam.snap()


    # decorator, to check if animate flag is set...
    def _animate(func):
        def checker(self, *args, **kwargs):
            if self.animate:
                return func(self, *args, **kwargs)
        return checker


    @_animate
    def frame(self, cy, cx, ny, nx):
        miny, maxy = sorted([cy, ny])
        minx, maxx = sorted([cx, nx])
        self.mz[miny:maxy+1, minx:maxx+1] = self.EXPLORED
        self.mz[ny, nx] = self.CURRENT
        self.mz[cy, cx] = self.PARENT
        plt.imshow(self.mz)
        self.cam.snap()
        self.mz[ny, nx] = self.EXPLORED
        self.mz[cy, cx] = self.EXPLORED


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
