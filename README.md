# Pathfinding algorithms
A school project on pathfinding algorithms based on mazes, by Jens Tinggaard.

## Prerequisites
Requires installation of `numpy`, `pillow`, `matplotlib` and `pydaedalus`.
Furthermore `pydaedalus` requires a `C++` compiler to be installed.
The program will run without the library, however some of the functionality (maze generation) will be limited.
`matplotlib` is only used to visualize the stats on the different algorithms, the pathfinding can run without it.

I'd recommend creating a virtual environment:

### Using Python3
```shell
git clone https://github.com/Tinggaard/pathfinding.git
cd pathfinding
virtualenv venv
. venv/bin/activate
```

Check that the virtual environment is working:
```shell
which python
```

The easiest way to use the program is simply
```shell
pip install .
```
After running the above command, one can, by typing `pathfinding` access the main function of the program.
*Please note* that the program is still under heavy development, so the installation is only intented simplify the installation of 3rd party libraries, as well as making a convenient alias for executing the script.

# Usage
```shell
pathfinding [-h] (-i INPUT | -g width height) [-v] [-s] [-f] [-o OUTPUT]
            [-a {astar,dijkstra,breadthfirst,depthfirst,rightturn}]
```
E.g.
```shell
pathfinding -i /mazes/perfect/101.png -o /out/solution.png -vs
```

The script accepts bitmap files and portable network graphics (`.bmp` and `.png`) as images.

It can also read (and generate) textfiles, with pounds (`#`) as wall, and whitespace (` `) as path.

## Generating your own mazes
The file `generate.py` can be used to generate mazes of a specific size (and algorithm to come - only `create_perfect()` for now).

Use it with:
```shell
./src/generate.py width height location
```
E.g.
```shell
./src/generate.py 151 101 /mazes/maze.bmp
```

## Comparing algorithms
I've created the script called [`timer.sh`](https://github.com/Tinggaard/pathfinding/blob/master/timer.sh), which can time all images in a subfolder of the `mazes` folder, using all the available algorithms.

The script can be called like as follows:
```shell
./timings.sh [-v]
```
After running, a textfile ([`timings.txt`](https://github.com/Tinggaard/pathfinding/blob/master/timings.txt)) is created, with stats on all the runs. This output can then be filtered out.

### Visualising the differences
The file [`src/visualizer.py`](https://github.com/Tinggaard/pathfinding/blob/master/src/visualizer.py), can either plot or print some of the stats generated from the output of the shell script above.

```shell
./src/visualizer.py (-p | -s)
```
`-p` to plot or `-s` to show in the terminal.
