import click
from daedalus import Maze
import numpy as np


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
        click.echo('NOTE: height must be odd, automatically incremented by 1')
        height += 1

    if not width % 2:
        click.echo('NOTE: width must be odd, automatically incremented by 1')
        width += 1

    # genereate maze accordingly
    maze = Maze(width, height)

    # the actual generation
    method(maze)

    # invert array, as library treats 0 as path and 1 as wall
    inv = np.array(maze, dtype=np.bool)
    return np.logical_not(inv).astype(int)
