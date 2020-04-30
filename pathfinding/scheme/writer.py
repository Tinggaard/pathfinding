import sys
from os import path

import click
from PIL import Image
import numpy as np


# convenient function that reads the filetype, and the save it as an image
def write(filename: str, maze: np.ndarray):
    file, ext = path.splitext(filename)

    if ext.lower() in ['.jpg', '.gif', '.tiff', '.jpeg', '.svg', '.jfif']:
        click.echo('ERROR: Imagefile must be of type ".png" og ".bmp"')
        sys.exit(1)

    elif ext.lower() in ['.png', '.bmp']:
        return _save_image(destination, maze)

    if ext.lower() in ['.txt', '.text']:
        return _save_text(destination, maze)

    click.echo('Weird inputfile, did not understand')



# write maze to disk as image
def _save_image(self, destination: str, maze: np.ndarray) -> None:
    Image.fromarray((maze*255).astype(np.uint8)).save(destination)


# write maze to disk as text file
def _save_text(self, destination: str, maze: np.ndarray) -> None:
    # create (and truncate) file
    with open(destination, 'w+') as f:
        # create normal python list, that are type independent
        for row in maze:
            tmp = []
            for val in row:
                tmp.append(str(val))
            f.write(''.join(tmp).replace('0', '#').replace('1', ' ') + '\n')
