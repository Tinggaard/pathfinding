#!/usr/bin/env python
from daedalus import Maze
import numpy as np

def gen_maze(size: tuple) -> np.ndarray:
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

    # other methods are available, this is just the standard for now
    maze.create_perfect()
    # other methods include:
    # create_braid
    # create_unicursal
    # create_spiral
    # create_braid_tilt
    # create_diagonal
    # create_sidewinder
    # create_recursive
    # create_prim

    # invert array, as library treats 0 as path and 1 as wall
    inv = np.array(maze, dtype=np.bool)
    return np.logical_not(inv).astype(int)



# short snippet to generate a maze and nothing else
if __name__ == '__main__':
    import sys
    from PIL import Image

    try:
        width, height, location = sys.argv[1:4]
        width, height = int(width), int(height)

    except:
        print('ERROR: No arguments given...')
        print('Usage: python generate.py width height location')
        print('E.g.')
        print('python generate.py 31 31 ../in/maze.bmp')
        sys.exit(1)

    maze = gen_maze((width, height))

    Image.fromarray((maze*255).astype(np.uint8)).save(location)
