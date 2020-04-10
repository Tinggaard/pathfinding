#!/usr/bin/env python
from daedalus import Maze
import numpy as np

def gen_maze(size: tuple, method = Maze.create_perfect) -> np.ndarray:
    width, height = size

    # basic chekcs
    if not height % 2:
        print('NOTE: height must be odd, automatically incremented by 1')
        height += 1

    if not width % 2:
        print('NOTE: width must be odd, automatically incremented by 1')
        width += 1

    # genereate maze accordingly
    maze = Maze(width, height)

    method(maze)


    # invert array, as library treats 0 as path and 1 as wall
    inv = np.array(maze, dtype=np.bool)
    return np.logical_not(inv).astype(int)


# autogenerate images of sizes and methods
def auto_gen():

    methods = [
        Maze.create_braid,
        Maze.create_braid_tilt,
        Maze.create_diagonal,
        Maze.create_perfect,
        Maze.create_prim,
        Maze.create_recursive,
        Maze.create_sidewinder,
        Maze.create_spiral,
        Maze.create_unicursal,
    ]

    sizes = [
        51,
        101,
        501,
        1001,
        2501,
        5001,
    ]

    for method in methods:
        for size in sizes:
            mz = gen_maze((size, size), method)

            loc = '../mazes/' + method.__name__.split('_', 1)[1] + '/' + str(size) + '.png'
            print('Saving to: ', loc)

            Image.fromarray((mz*255).astype(np.uint8)).save(loc)


# short snippet to generate a maze and nothing else
if __name__ == '__main__':
    import sys
    from PIL import Image
    import os.path

    # auto_gen()

    try:
        width, height, location = sys.argv[1:4]
        width, height = int(width), int(height)

    except:
        print('ERROR: No arguments given...')
        print('Usage: ./generate.py width height location')
        print('E.g.')
        print('python generate.py 31 31 ../in/maze.bmp')
        sys.exit(1)

    if os.path.isfile(location):
        i = input('WARNING: File "{}" already exists, overwrite (yes/no)? '.format(location)).lower()
        # if not yes or y
        if i != 'yes' and i != 'y':
            print('Aborting')
            return

    maze = gen_maze((width, height))

    Image.fromarray((maze*255).astype(np.uint8)).save(location)
