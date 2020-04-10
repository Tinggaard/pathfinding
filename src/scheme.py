import numpy as np
from PIL import Image
import os.path

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


    # heapq comparison for dijkstra
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
    def get_nodes(self) -> list:
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


    # debugging function used to change number on found nodes
    def show_nodes(self) -> None:
        tmp = self.maze.copy()
        for node in self.nodes:
            tmp[node[0], node[1]] = 8
        print(tmp)


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
                    if self.maze[tmp, x+1] or self.maze[tmp, x-1] or not self.maze[tmp-1, x]:
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
                    if self.maze[tmp, x+1] or self.maze[tmp, x-1] or not self.maze[tmp+1, x]:
                        node.nearby[1] = ((tmp, x), dn+1)
                        break

            if left:
                # decrement x with 1
                for lt in range(x):
                    tmp = x-lt-1
                    # if up or down are path or left is not, save length and exit
                    if self.maze[y+1, tmp] or self.maze[y-1, tmp] or not self.maze[y, tmp-1]:
                        node.nearby[0] = ((y, tmp), lt+1)
                        break

            if right:
                # increment x with 1
                for rt in range(self.x - x):
                    tmp = x+rt+1
                    # if up or down are path or right is not, save length and exit
                    if self.maze[y+1, tmp] or self.maze[y-1, tmp] or not self.maze[y, tmp+1]:
                        node.nearby[2] = ((y, tmp), rt+1)
                        break


    def show_solution(self) -> None:
        if not self.solved:
            print('ERROR: Graph not solved, cannot show solution')
            return False

        sol = []
        # create normal python list, that are type independent
        for row in self.maze:
            tmp = []
            for val in row:
                tmp.append(str(val))
            sol.append(tmp)

        # mark all nodes
        for node in self.path:
            y, x = node.location
            sol[y][x] = 'n'

        # print it all
        for row in sol:
            print(''.join(row).replace('0', '▒').replace('1', ' ')) # character: u"\u2592"



    # def scale_image(self, scale):
    #     return cv.resize(self.maze, (0,0), fx=scale, fy=scale)


    # write maze to disk as image
    def save_image(self, destination: str) -> None:
        Image.fromarray((self.maze*255).astype(np.uint8)).save(destination)


    # write maze to disk as text file
    def save_text(self, destination: str) -> None:
        # create (and truncate) file
        with open(destination, 'w+') as f:
            # create normal python list, that are type independent
            for row in self.maze:
                tmp = []
                for val in row:
                    tmp.append(str(val))
                f.write(''.join(tmp).replace('0', '#').replace('1', ' ') + '\n')


    # convenient function that reads the filetype, and the save it as an image
    def save(self, destination: str, force: bool = False) -> None:
        if not force:
            if os.path.isfile(destination):
                i = input('WARNING: File "{}" already exists, overwrite (yes/no)? '.format(destination)).lower()
                # if not yes or y
                if i != 'yes' and i != 'y':
                    print('Aborting')
                    return

        file, ext = os.path.splitext(destination)

        if ext.lower() in ['.jpg', '.gif', '.tiff', '.jpeg', '.svg', '.jfif']:
            print('NOTE: will only write images to types of ".bmp" and ".png"')
            print('other formats compress the image, and makes it unusable')
            return False

        elif ext.lower() in ['.png', '.bmp']:
            return self.save_image(destination)

        if ext.lower() not in ['.txt', '.text']:
            print('NOTE: writing as textfile, as format was not understood')
            print('use the ".txt" or ".text" extension to dismiss this note')

        return self.save_text(destination)


    # write maze solution to disk as image
    def save_solution_image(self, destination: str) -> None:
        if not self.solved:
            print('ERROR: Graph not solved, cannot show solution')
            return False

        file, ext = os.path.splitext(destination)
        if not ext.lower() in ['.bmp', '.png']:
            print('ERROR: Can only save images to ".bmp" or ".png" type')
            return False

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


    def save_solution_text(self, destination: str, fancy: bool = True) -> None:
        if not self.solved:
            print('ERROR: Graph not solved, cannot show solution')
            return False

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

        # otherwise, we makin' it fancy!

        # filling out the nodes
        def filled(field):
            return field not in ['0', '1']


        for i in range(len(self.path) - 1):
            c = self.path[i].location #current
            n = self.path[i+1].location #next

            # y vals are the same: going horizontal
            if c[0] == n[0]:
                # new_v = False
                for loc in range(min(c[1], n[1]), max(c[1], n[1]) + 1):
                    sol[c[0]][loc] = '━'

            # x vals are the same: going vertical
            else:
                # new_v = True
                for loc in range(min(c[0], n[0]), max(c[0], n[0]) + 1):
                    sol[loc][c[1]] = '┃'

            top = filled(sol[c[0]-1][c[1]])
            btm = filled(sol[c[0]+1][c[1]])
            lft = filled(sol[c[0]][c[1]-1])
            rht = filled(sol[c[0]][c[1]+1])

            if top and btm:
                sol[c[0]][c[1]] = '┃'
                continue

            if lft and rht:
                sol[c[0]][c[1]] = '━'
                continue

            if lft and top:
                sol[c[0]][c[1]] = '┛'
                continue

            if rht and top:
                sol[c[0]][c[1]] = '┗'
                continue

            if rht and btm:
                sol[c[0]][c[1]] = '┏'
                continue

            if lft and btm:
                sol[c[0]][c[1]] = '┓'
                continue

        # create (and truncate) file
        with open(destination, 'w+') as f:
            # create normal python list, that are type independent
            for line in sol:
                f.write(''.join(line).replace('0', '▒').replace('1', ' ') + '\n')


    # convenient function that reads the filetype, and the save it as an image
    def save_solution(self, destination: str, force: bool = False, fancy: bool = False) -> None:
        if not force:
            if os.path.isfile(destination):
                i = input('WARNING: File "{}" already exists, overwrite (yes/no)? '.format(destination)).lower()
                # if not yes or y
                if i != 'yes' and i != 'y':
                    print('Aborting')
                    return

        file, ext = os.path.splitext(destination)

        if ext.lower() in ['.jpg', '.gif', '.tiff', '.jpeg', '.svg', '.jfif']:
            print('NOTE: will only write images to types of ".bmp" and ".png"')
            print('other formats compress the image, and makes it unusable')
            return False

        elif ext.lower() in ['.png', '.bmp']:
            return self.save_solution_image(destination)

        if ext.lower() not in ['.txt', '.text']:
            print('NOTE: writing as textfile, as format was not understood')
            print('use the ".txt" or ".text" extension to dismiss this note')

        return self.save_solution_text(destination, fancy)


    # remove nodes on a dead end completely
    # may implement later...
    def rm_dead_ends(self):
        # for node in self.nodes:
        #     if len(node.adj) > 2:
        #         pass
        pass
