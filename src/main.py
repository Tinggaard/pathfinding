#!/usr/bin/env python
import sys
import os.path
import re
import argparse
from time import time
import numpy as np
from PIL import Image

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
    # convert to binary array
    return np.array(Image.open(path)) // 255


def load(path: str) -> object:

    # try locating the file
    if not os.path.isfile(path):
        raise FileNotFoundError('The requested file was not found')

    file, ext = os.path.splitext(path)
    # some image files not supported
    if ext.lower() in ['.jpg', '.gif', '.tiff', '.jpeg', '.svg', '.jfif']:
        print('ERROR: Imagefile must be of type ".png" og ".bmp"')
        sys.exit(1)

    # method to use
    return load_img if ext.lower() == '.png' or ext.lower() == '.bmp' else load_txt


def main() -> None:


    # methods, based on argparse
    methods = {
    'astar': solve.Graph.astar,
    'dijkstra': solve.Graph.dijkstra,
    'breadthfirst': solve.Graph.breadthfirst,
    'depthfirst': solve.Graph.depthfirst,
    'rightturn': solve.Graph.rightturn
    }

    # argparse
    parser = argparse.ArgumentParser(description='Visualize pathfinding algorithms using mazes')

    # must take exatly 1 input
    i = parser.add_mutually_exclusive_group(required=True)
    i.add_argument('-i', '--input', type=str, help='Path to load maze from')
    i.add_argument('-g', '--generate', nargs=2, metavar=('width', 'height'), type=int, help='Generate maze of size (width * height)')

    # other stuff
    parser.add_argument('-v', '--verbose', action='store_true', help='Output is verbose, including timings')
    parser.add_argument('-s', '--show', action='store_true', help='Show solved solution in terminal')
    parser.add_argument('-f', '--force', action='store_true', help='Do not ask before overwriting files')
    parser.add_argument('-o', '--output', default=None, type=str, help='Path to save maze to')
    parser.add_argument('-a', '--algorithm', default='dijkstra', type=str, choices=('astar', 'dijkstra', 'breadthfirst', 'depthfirst', 'rightturn'), help='Pathfinding algorithm to use')


    # parse it
    args = parser.parse_args()

    verbose = args.verbose
    output = args.output
    algorithm = args.algorithm
    show = args.show
    force = args.force

    # verbose print: only print if verbose mode is on
    def vprint(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)


    # load input from file
    if args.input:

        f = load(args.input)

        start_time = time()
        vprint('Loading input')
        struct = f(args.input)

        construct_time = time()
        vprint('Loading took {} ms'.format(round((construct_time - start_time)*1000)))
        vprint()


    # Generate maze from size parameter
    else:
        try:
            import generate
        except ImportError:
            raise ImportError('Module "pydaedalus" not found, please ensure a C++ compiler is installed')

        start_time = time()
        vprint('Generating maze')
        struct = generate.gen_maze(args.generate)

        construct_time = time()
        vprint('Generating took {} ms'.format(round((construct_time - start_time)*1000)))
        vprint()



    vprint('Constructing graph')
    maze = solve.Graph(struct)

    end_time = time()
    vprint('Constructing took {} ms'.format(round((end_time - construct_time)*1000)))
    vprint('Nodes found:', maze.node_count)
    vprint()

    method = methods[algorithm]

    explored, path, nodes, length = method(maze)

    s = 'Success!' if maze.solved else 'The algorithm did not find a solution...'

    print(s)

    if maze.solved:

        vprint('Nodes explored:', explored)
        vprint('Nodes in path:', nodes)
        vprint('Length of path:', length)

        if show:
            maze.show_solution()

        vprint('Total time elapsed: {} ms'.format(round((time()-start_time)*1000)))

        if output:
            maze.save_solution(output, force)




if __name__ == '__main__':
    main()
