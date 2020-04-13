#!/usr/bin/env python
import sys
import os.path
import re
import argparse
from time import time
import numpy as np
from PIL import Image
import logging

# own code
import solve


# convert textfile to maze
# Taking pound (#) as wall and space ( ) as path
def load_txt(path: str) -> np.ndarray:
    # open file
    with open(path, 'r') as f:
        # replace # with 1 and " " with 0
        lines = [l.strip().replace("#", "0").replace(" ", "1")
            for l in f.readlines()]

    # converting to ints and changing shape
    maze = [[] for _ in lines]
    for no, line in enumerate(lines):

        #regex validation
        if not re.match(r'^[01]*$', line):
            print('ERROR: Textfile can only contain pounds and spaces \
                ("#" and " "), failed on line {}'.format(no+1))
            sys.exit(1)

        # converting to ints
        for num in line:
            maze[no].append(int(num))

    return np.array(maze)


# convert binary image to maze
# black (0) begin wall and white (255) being path
def load_img(path: str) -> np.ndarray:
    # convert to binary array
    return np.array(Image.open(path).convert('1')).astype(np.uint8)


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
    parser = argparse.ArgumentParser(
        description='Visualize pathfinding algorithms using mazes')

    # must take exatly 1 input
    i = parser.add_mutually_exclusive_group(required=True)
    i.add_argument('-i', '--input', type=str, help='Path to load maze from')
    i.add_argument('-g', '--generate', nargs=2, metavar=('width', 'height'),
        type=int, help='Generate maze of size (width * height)')

    # other stuff
    parser.add_argument('-v', '--verbose', action='store_true',
        help='Logging will be set to INFO instead of WARNING')
    parser.add_argument('-s', '--show', action='store_true',
        help='Show solved solution in terminal')
    parser.add_argument('-f', '--force', action='store_true',
        help='Do not ask before overwriting files')
    parser.add_argument('-o', '--output', default=None, type=str,
        help='Path to save maze to')
    parser.add_argument('-a', '--algorithm', default='dijkstra', type=str,
        choices=('astar', 'dijkstra', 'breadthfirst', 'depthfirst', 'rightturn'),
        help='Pathfinding algorithm to use')


    # parse it
    args = parser.parse_args()

    verbose = args.verbose
    output = args.output
    algorithm = args.algorithm
    show = args.show
    force = args.force

    # set log_level (for other leves, set it manually)
    log_level = logging.INFO if verbose else logging.WARNING


    logger = logging.getLogger('pathfinding')
    logger.setLevel(log_level)
    # file handler
    fh = logging.FileHandler('pathfinding.log')
    fh.setLevel(log_level)
    # console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.ERROR)
    # formatter for the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers
    logger.addHandler(fh)
    logger.addHandler(ch)

    # logger.debug('debug info her')
    # logger.info('Dette er info')
    # logger.warning('dette er en advarsel')
    # logger.error('Dette er en fejl')
    # logger.critical('dette er kritisk')


    # load input from file
    if args.input:

        # determine function to load file
        f = load(args.input)

        # load time
        start_time = time()
        struct = f(args.input)
        load_time = time()

        # log the time
        logger.info('Loading took {} ms'.format(
            round((load_time - start_time)*1000)))


    # Generate maze from size parameter
    else:
        # if g flag is set, try importing the pydaedalus module
        try:
            import generate
        except ImportError:
            raise ImportError('Module "pydaedalus" not found, \
                please ensure a C++ compiler is installed')

        # generate maze and time it
        start_time = time()
        struct = generate.gen_maze(args.generate)
        load_time = time()

        # log the time
        logger.info('Generating took {} ms'.format(
            round((load_time - start_time)*1000)))


    # generate the structure
    maze = solve.Graph(struct)

    # log time taken to generate sturcture and nodes found
    struct_time = time()
    logger.info('Constructing took {} ms'.format(
        round((struct_time - load_time)*1000)))
    logger.info('Nodes found: {}'.format(maze.node_count))

    # set solveing method
    method = methods[algorithm]

    # solve...
    explored, path, nodes, length = method(maze)
    # ms to solve
    solve_time = round((time() - struct_time)*1000, 5)

    print('{file} took {time} using {method}'.format(
        file=args.input, time=solve_time, method=args.algorithm))


    # self explanatory
    if not maze.solved:
        logger.error('The algorithm did not find a solution...')
        sys.exit(1)


    logger.info('Nodes explored: {}'.format(explored))
    logger.info('Nodes in path: {}'.format(nodes))
    logger.info('Length of path: {}'.format(length))

    # if s flag set, show the solution in terminal
    if show:
        maze.show_solution()

    logger.info('Total time elapsed: {} ms'.format(
        round((time()-start_time)*1000)))

    # if o flag is set, save the output (force if f is also set)
    if output:
        maze.save_solution(output, force)




if __name__ == '__main__':
    main()
