# Pathfinding algorithms
A school project on pathfinding algorithms based on mazes, by Jens Tinggaard.

## Prerequisites
Requires installation of `numpy`, `opencv-python` and `pydaedalus`.

I'd recommend creating a virtual environment:
```shell
git clone https://github.com/Tinggaard/pathfinding.git
cd pathfinding
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```shell
python main.py (-i INPUT | -g width height) [-v] [-s]
```
E.g.
```shell
python main.py -i ../in/tiny.png -vs
```
