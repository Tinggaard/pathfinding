# Pathfinding algorithms
A school project on pathfinding algorithms based on mazes, by Jens Tinggaard.

## Prerequisites
Requires installation of `numpy`, `pillow` and `pydaedalus`.
Furthermore `pydaedalus` requires a `C++` compiler to be installed.
The program will run without the library, however some of the functionality (maze generation) will be limited.


I'd recommend creating a virtual environment:

### Using Python3
```shell
git clone https://github.com/Tinggaard/pathfinding.git
cd pathfinding
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Using pypy
```shell
git clone https://github.com/Tinggaard/pathfinding.git
cd pathfinding
pypy -m venv venv-pypy
source venv-pypy/bin/activate
pip install -r requirements.txt
```
Check that the virtual environment is working:
```shell
which python
```

# Usage
```shell
./main.py [-h] (-i INPUT | -g width height) [-v] [-s] [-f] [-o OUTPUT]
          [-a {astar,dijkstra,breadthfirst,depthfirst,rightturn}]
```
E.g.
```shell
python main.py -i ../mazes/perfect/101.png -o ../out/solution.png -vs
```

The script accepts bitmap files and portable network graphics (`.bmp` and `.png`) as images.

It can also read (and generate) textfiles, with pounds (`#`) as wall, and whitespace (` `) as path.

## Generating your own mazes
The file `generate.py` can be used to generate mazes of a specific size (and algorithm to come - only `create_perfect()` for now).

Use it with:
```shell
./generate.py width height location
```
E.g.
```shell
./generate.py 151 101 ../mazes/maze.bmp
```
