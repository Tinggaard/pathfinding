#!/usr/bin/env python3
import sys
import re
import os.path
from time import time
# import logging

import click
import numpy as np
from PIL import Image
from daedalus import Maze

from .scheme import Graph


# vars for determining filetype
IMAGE = 1
TEXT = 2
VIDEO = 3

METHODS = {
'astar': Graph.astar,
'dijkstra': Graph.dijkstra,
'breadthfirst': Graph.breadthfirst,
'depthfirst': Graph.depthfirst,
'rightturn': Graph.rightturn
}


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, help='Ramp up verbosity level')
@click.option('-f', '--force', is_flag=True, help='Do not ask before overwriting files')
@click.option('-o', '--output', type=click.STRING, help='Path to save maze to')
@click.option('-a', '--algorithm', type=click.Choice(['astar', 'dijkstra', 'breadthfirst', 'depthfirst', 'rightturn']), default='dijkstra', show_default=True, help='Pathfinding algorithm to use')
def solve(filename, verbose, force, output, algorithm):
    """Solve maze from given inputfile, using options listed below"""
    maze = load(filename) #loading

    struct = Graph(maze) #generate struct
    alg = METHODS[algorithm] # alg to use
    start = time()
    explored, path, nodes, length = alg(struct) #solve!
    end = time()
    elapsed = round((end-start)*1000, 5)

    if not struct.solved:
        click.secho('ERROR: The algorithm could not solve the maze', fg='red', err=True)


    click.secho(f'SUCCESS: Solved {filename} in {elapsed} ms using {algorithm}', fg='green')

    if verbose:
        click.echo(f'Nodes explored: {explored}')
        click.echo(f'Nodes in path: {nodes}')
        click.echo(f'Length of path: {length}')

    if output:
        file_exists(output, force)
        struct.save_solution(output, filetype(output))


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, help='Ramp up verbosity level')
@click.option('-f', '--force', is_flag=True, help='Do not ask before overwriting files')
@click.option('-o', '--output', default='solution.mp4', type=click.STRING, show_default=True, help='Path to save maze to')
@click.option('-a', '--algorithm', type=click.Choice(['astar', 'dijkstra', 'breadthfirst', 'depthfirst', 'rightturn']), default='dijkstra', show_default=True, help='Pathfinding algorithm to use')
def visualize(filename, verbose, force, output, algorithm):
    """Visualize pathfinding algorithm as videofile on given filename"""
    maze = load(filename) #loading

    if not filetype(output) == VIDEO:
        click.secho('ERROR: Outputfile not a vide extension, valid extensions are: .flv, .mp4, .avi', fg='red', err=True)
        sys.exit(1)

    struct = Graph(maze) #generate struct
    struct.visualize()
    alg = METHODS[algorithm] # alg to use
    start = time()
    explored, path, nodes, length = alg(struct) #solve!
    end = time()
    elapsed = round((end-start)*1000, 5)

    if not struct.solved:
        click.secho('ERROR: The algorithm could not solve the maze', fg='red', err=True)


    click.secho(f'SUCCESS: Solved {filename} in {elapsed} ms using {algorithm}', fg='green')

    if verbose:
        click.echo(f'Nodes explored: {explored}')
        click.echo(f'Nodes in path: {nodes}')
        click.echo(f'Length of path: {length}')

    if output == 'solution.mp4':
        click.secho('INFO: No outputfile given, saving as default', fg='yellow')

    file_exists(output, force)
    struct.save_solution(output, filetype(output))


@cli.command()
@click.argument('filename', type=click.Path(allow_dash=True))
@click.argument('size', nargs=2, type=click.INT)
@click.option('-m', '--method', type=click.Choice(['braid', 'braid_tilt', 'diagonal', 'perfect', 'prim', 'recursive', 'sidewinder', 'spiral']), default='perfect', show_default=True, help='Generation method to use')
@click.option('-f', '--force', is_flag=True, help='Do not ask before overwriting files')
def generate(filename, size, method, force):
    """
    Generate maze from scratch

    Takes outputfile and maze size as arguments
    """
    file_exists(filename, force)
    write(filename, gen_maze(size, method))


# Prompt user if file already exists and force is unset
def file_exists(filename: str, force: bool) -> None:
    if os.path.isfile(filename) and not force:
        click.confirm(f'The file "{filename}" already exists, overwrite?', abort=True)


def gen_maze(size: tuple, method: str = 'perfect') -> np.ndarray:
    width, height = size

    methods = {
        'braid': Maze.create_braid,
        'braid_tilt': Maze.create_braid_tilt,
        'diagonal': Maze.create_diagonal,
        'perfect': Maze.create_perfect,
        'prim': Maze.create_prim,
        'recursive': Maze.create_recursive,
        'sidewinder': Maze.create_sidewinder,
        'spiral': Maze.create_spiral,
        # 'unicursal': Maze.create_unicursal,
    }

    method = methods[method]

    # basic chekcs
    # maybe use logging instead...?
    if not height % 2:
        click.secho('NOTE: height must be odd, automatically incremented by 1', fg='yellow')
        height += 1

    if not width % 2:
        click.secho('NOTE: width must be odd, automatically incremented by 1', fg='yellow')
        width += 1

    # genereate maze accordingly
    maze = Maze(width, height)

    # the actual generation
    method(maze)

    # invert array, as library treats 0 as path and 1 as wall
    inv = np.array(maze, dtype=np.bool)
    return np.logical_not(inv).astype(int)


def filetype(filename: str) -> int:
    file, ext = os.path.splitext(filename)
    ext = ext.lower()
    # some image files not supported
    if ext in ['.png', '.bmp']:
        return IMAGE
    elif ext in ['.txt', '.text']:
        return TEXT
    elif ext in ['.mp4', '.flv', '.avi']:
        return VIDEO

    elif ext in ['.jpg', '.gif', '.tiff', '.jpeg', '.svg', '.jfif']:
        click.secho('ERROR: Imagefile must be of type ".png" og ".bmp"', fg='red', err=True)
        sys.exit(1)

    else:
        click.secho(f'ERROR: The filetype of the file "{filename}" is not supported, please try something else. Valid extensions include .png, .bmp, .txt, .text, .mp4, .flv and .avi', fg='red', err=True)
        sys.exit(1)


def load(filename: str) -> np.ndarray:
    extension = filetype(filename)

    if extension == IMAGE:
        return _load_img(filename)
    elif extension == TEXT:
        return _load_txt(filename)

    else:
        click.secho('ERROR: Cannot load a videofile.', fg='red', err=True)
        sys.exit(1)


# convert binary image to maze
# black (0) begin wall and white (255) being path
def _load_img(filename: str) -> np.ndarray:
    # convert to binary array
    return np.array(Image.open(filename).convert('1')).astype(np.uint8)


# convert textfile to maze
# Taking pound (#) as wall and space ( ) as path
def _load_txt(filename: str) -> np.ndarray:
    # open file
    with open(filename, 'r') as f:
        # replace # with 1 and " " with 0
        lines = [l.strip().replace("#", "0").replace(" ", "1")
            for l in f.readlines()]

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

    maze = np.array(maze)


# convenient function that reads the filetype, and the save it as an image
def write(filename: str, maze: np.ndarray) -> None:
    extension = filetype(filename)

    if extension == IMAGE:
        return _write_img(filename, maze)
    elif extension == TEXT:
        return _write_txt(filename, maze)

    else:
        click.secho('ERROR: Trying to write imagefile in the wrong context', fg='red', err=True)
        sys.exit(1)


# write maze to disk as image
def _write_img(destination: str, maze: np.ndarray) -> None:
    Image.fromarray((maze*255).astype(np.uint8)).save(destination)


# write maze to disk as text file
def _write_txt(destination: str, maze: np.ndarray) -> None:
    # create (and truncate) file
    with open(destination, 'w+') as f:
        # create normal python list, that are type independent
        for row in maze:
            tmp = []
            for val in row:
                tmp.append(str(val))
            f.write(''.join(tmp).replace('0', '#').replace('1', ' ') + '\n')


if __name__ == '__main__':
    cli()
