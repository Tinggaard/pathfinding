#!/usr/bin/env python
# official libraries
import sys
import os.path
import re
# import argparse
from time import time
import numpy as np
import cv2 as cv

# own code
import solve


# convert textfile to maze
# Taking pound (#) as wall and space ( ) as path
def load_txt(path: str) -> np.ndarray:
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

        # converting to ints
        for num in line:
            maze[no].append(int(num))

    return np.array(maze)


# convert binary image to maze
# black (0) begin wall and white (255) being path
def load_img(path: str) -> np.ndarray:
    # open file
    maze = cv.imread(path, cv.IMREAD_GRAYSCALE)

    # anything under 128 is white, anything over i black
    return maze // 128



def main() -> None:
    path = sys.argv[1]

    if not os.path.isfile(path):
        raise FileNotFoundError('The requested file was not found')

    file, ext = os.path.splitext(path)
    if ext.lower() in ['.jpg', '.gif', '.tiff', '.bmp', '.jpeg', '.svg', '.jfif']:
        print('Imagefile must be of type ".png", exiting...')
        sys.exit(1)

    func = load_img if ext.lower() == '.png' else load_txt


    start_time = time()
    print('Loading input')
    struct = func(path)

    construct_time = time()
    print('Loading took {} ms'.format(round((construct_time - start_time)*1000, 8)))
    print()

    print('Constructing graph')
    maze = solve.Maze(struct)

    end_time = time()
    print('Constructing took {} ms'.format(round((end_time - construct_time)*1000, 8)))
    print('Nodes found:', maze.node_count)
    print()

    maze.leftturn()

    print('Success!')



if __name__ == '__main__':
    main()
