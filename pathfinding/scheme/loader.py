import sys
import re
from os import path

import click
from PIL import Image
import numpy as np


def load(filename: str) -> object:
    file, ext = path.splitext(filename)
    # some image files not supported
    if ext.lower() in ['.jpg', '.gif', '.tiff', '.jpeg', '.svg', '.jfif']:
        click.echo('ERROR: Imagefile must be of type ".png" og ".bmp"')
        sys.exit(1)

    elif ext.lower() in ['.png', '.bmp']:
        return _load_img(filename)

    elif ext.lower() in ['.txt', '.text']:
        return _load_txt(filename)

    else:
        click.echo('Weird inputfile, did not understand')


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


# convert binary image to maze
# black (0) begin wall and white (255) being path
def _load_img(filename: str) -> np.ndarray:
    # convert to binary array
    return np.array(Image.open(filename).convert('1')).astype(np.uint8)
