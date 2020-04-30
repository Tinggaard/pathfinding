#!/usr/bin/env python3
import click
from pathfinding import load, write, gen_maze
from os import path


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, help='Ramp up verbosity level')
@click.option('-f', '--force', is_flag=True, help='Do not ask before overwriting files')
@click.option('-s', '--show', is_flag=True, help='Show solved solution in terminal')
@click.option('-o', '--output', default='solution.png', type=click.STRING, show_default=True, help='Path to save maze to')
@click.option('-a', '--algorithm', type=click.Choice(['astar', 'dijkstra', 'breadthfirst', 'depthfirst', 'rightturn']), default='dijkstra', show_default=True, help='Pathfinding algorithm to use')
def solve(filename, verbose, force, show, output, algorithm):
    """Solve input maze"""
    maze = load(filename)

    if output:
        file_exists(output, force)


@cli.command()
@click.argument('filename', type=click.Path(allow_dash=True))
@click.argument('size', nargs=2, type=click.INT)
@click.option('-m', '--method', type=click.Choice(['braid', 'braid_tilt', 'diagonal', 'perfect', 'prim', 'recursive', 'sidewinder', 'spiral']), default='perfect', show_default=True, help='Generation method to use')
@click.option('-f', '--force', is_flag=True, help='Do not ask before overwriting files')
def generate(filename, size, method, force):
    """Generate maze from scratch"""
    file_exists(filename, force)
    write(filename, gen_maze(size, method))


# Prompt user if file already exists and force is unset
def file_exists(filename, force):
    if path.isfile(filename) and not force:
        click.confirm(f'The file "{filename}" already exists, overwrite?', abort=True)


if __name__ == '__main__':
    cli()
