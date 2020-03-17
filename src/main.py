#!/usr/bin/env python
# tiny.txt: 23 nodes
# pypy
import sys
import os
import re
import numpy as np
# import cv2

class Maze:
    def __init__(self, struct):
        self.struct = struct

        # shape of maze
        try:
            self.x = struct.shape[1]
            self.y = struct.shape[0]
        except:
            print('Shape of maze is not rectangular; exiting...')
            sys.exit(1)

        self.nodes = self.get_nodes()

        print(self.show_nodes())


    def get_nodes(self):
        nodes = []

        # iterating the maze finding nodes
        for y, line in enumerate(self.struct):
            for x, field in enumerate(line):

                # skip if wall (0 == False)
                if not field:
                    continue

                # outer path
                if y == 0 or y == self.y-1:
                    nodes.append((y,x))
                    continue

                # nodes around
                up = self.struct[y-1,x]
                down = self.struct[y+1,x]
                left = self.struct[y,x-1]
                right = self.struct[y,x+1]

                # 1 == True
                # change to bitwise?
                # if field is straight, skip it
                if ((down and up) and not (left and right)) or ((left and right) and not (down and up)):
                    continue

                nodes.append((y,x))

        return nodes


    def show_nodes(self):
        tmp = self.struct.copy()
        for node in self.nodes:
            tmp[node[0], node[1]] = 8
        return tmp









    def __repr__(self):
        return str(self.struct)


class Node:
    pass

# convert textfile to maze
# Taking pound (#) as wall and space ( ) as path
def load_txt(path):
    if not os.path.exists(path):
        raise FileNotFoundError('The requested file was not found')

    # open file
    with open(path, 'r') as f:
        # replace # with 1 and " " with 0
        lines = [l.strip().replace("#", "0").replace(" ", "1") for l in f.readlines()]

    # converting to ints and changing shape
    maze = [[] for _ in lines]
    for no, line in enumerate(lines):

        #regex validation
        if not re.match(r'^[01]*$', line):
            print('ERROR: Textfile can only contain pounds and spaces ("#" and " "), failed on line {}'.format(no+1))
            sys.exit(1)


        for num in line:
            maze[no].append(int(num))

    return np.array(maze)


# convert binary image to maze
# black (0) begin wall and white (255) being path
def load_img(path):
    pass


def main():
    path = sys.argv[1]

    struct = load_txt(path)

    maze = Maze(struct)

    # print(maze)
    print('Success!')



if __name__ == '__main__':
    main()
