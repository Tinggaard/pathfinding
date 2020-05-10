# Pathfinding algorithms
A school project on pathfinding algorithms based on mazes, by Jens Tinggaard.

## Prerequisites
Requires installation of `numpy`, `pillow`, `matplotlib`, `click`, `celluloid` and `pydaedalus`.
Furthermore `pydaedalus` requires a `C++` compiler to be installed.
The program will run without the library, however some of the functionality (maze generation) will be limited. *NOTE: this is not tested very often, last test were mid april 2020.*
`matplotlib` and `celluloid` is used to visualize the stats on the different algorithms and render the videootput, the pathfinding can run without it.

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
pip install -e .
```
After running the above command, one can, by typing `pathfinding` access the main function of the program.
*Please note* that the program is still under heavy development, so the installation is only intented simplify the installation of 3rd party libraries, as well as making a convenient alias for executing the script.

# Usage
```shell
pathfinding [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate   Generate maze from scratch Takes outputfile and maze size as...
  solve      Solve maze from given inputfile, using options listed below
  visualize  Visualize pathfinding algorithm as videofile on given filename
```
E.g.
```shell
pathfinding solve mazes/perfect/101.png -o out/solution.png -v
```
To get help on a specific command, run
```shell
pathfinding COMMAND --help
```
Which will show all arguments and available options for the specific command.

# Requirements
The script accepts bitmap files and portable network graphics (`.bmp` and `.png`) as images.

It can also read (and generate) textfiles, with pounds (`#`) as wall, and whitespace (` `) as path.

Furthermore, it can also create an animation of the solution as a videofile, using the `visualize` command. It is not very fast though, as every frame needs to be saved, and stitched together using `ffmpeg`.

## Generating your own mazes
The command `generate` can be used to generate mazes of a specific size and given creation routine.

Use it with:
```shell
pathfinding generate location width height (-m METHOD -f)
```
E.g.
```shell
pathfinding generate mazes/maze.png 100 150
```

## Comparing algorithms
I've created the script called [`timer.sh`](https://github.com/Tinggaard/pathfinding/blob/master/timer.sh), which can time all images in a subfolder of the `mazes` folder, using all the available algorithms.

The script can be called like as follows:
```shell
./timings.sh [-v]
```
After running, a textfile ([`timings.txt`](https://github.com/Tinggaard/pathfinding/blob/master/timings.txt)) is created, with stats on all the runs. This output can then be filtered out.

### Visualising the differences
The file [`pathfinding/comparer.py`](https://github.com/Tinggaard/pathfinding/blob/master/pathfinding/comparer.py), can either plot or print some of the stats generated from the output of the shell script above.

```shell
./src/comparer.py
```
