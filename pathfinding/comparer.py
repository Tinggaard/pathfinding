#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import re
import os.path
import sys

# read contents of file
def from_file(filename: str) -> str:
    if not os.path.isfile(filename):
        raise FileNotFoundError('The requested file was not found')

    with open(filename, 'r') as f:
        content = f.readlines()

    return content


def organize(load: str) -> dict:

    aliases = {
    'astar': 'a*',
    'breadthfirst': 'BF',
    'depthfirst': 'DF',
    'dijkstra': 'dijk',
    'rightturn': 'RT'
    }
    stats = {}

    for size in [51, 101, 501, 1001, 2501]:
        stats[size] = {}

        for alg in ['a*', 'BF', 'DF', 'dijk', 'RT']:
            stats[size][alg] = []


    size_pattern = re.compile(r'(?<=/)[0-9]+')
    time_pattern = re.compile(r'(?<= )[0-9\.]+(?= )')
    algorithm_pattern = re.compile(r'\w+$')

    # skip first line with date information
    for line in load[1:]:
        l = line.strip()

        # size of maze
        size = int(size_pattern.search(l).group())

        # time took to solve
        time = float(time_pattern.search(l).group())

        # using algorithm
        alg = algorithm_pattern.search(l).group()

        ag = aliases[alg]

        stats[size][ag].append(time)

    return stats


def plot_stats(stats: dict) -> None:
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 15))

    n = 1
    for s in stats.items():
        size, a = s
        algs = list(a.keys())
        observations = list(a.values())

        # row and column
        r, c = n // 2, n % 2
        n+=1

        bx = axes[r, c].boxplot(observations, labels = algs, patch_artist=True)

        axes[r, c].set_title('Maze size: {}'.format(size))
        axes[r, c].set_xlabel('Algorithms')
        axes[r, c].set_ylabel('Time spent in ms')
        axes[r, c].yaxis.grid(True) #grid

        colors = ['pink', 'lightblue', 'lightgreen', 'khaki', 'slateblue']

        for box, color in zip(bx['boxes'], colors):
            box.set_facecolor(color)

    fig.delaxes(axes[0,0])
    plt.show()


def print_stats(stats: dict) -> None:
    for s in stats.items():
        size, a = s

        # method, time
        minimum = ('', np.inf)
        maximum = ('', -np.inf)
        average = ('', np.inf)
        variance = ('', np.inf)

        for o in a.items():
            alg, timings = o

            mi = min(timings)
            ma = max(timings)
            avg = round(np.average(timings), 5)
            var = round(np.var(timings), 5)

            if mi < minimum[1]:
                minimum = (alg, mi)
            if ma > maximum[1]:
                maximum = (alg, ma)
            if avg < average[1]:
                average = (alg, avg)
            if var < variance[1]:
                variance = (alg, var)

        print('### MAZE SIZE: {} ###'.format(size))
        print('The fastest algorithm were {}, at only {} ms'.format(*minimum))
        print('The slowest algorithm were {}, at {} ms'.format(*maximum))
        print('The fastest algorithm on average were {}, at only {} ms'.format(*average))
        print('The most reliable algorithm were {}, with a variance of {}'.format(*variance))
        print()


def main(filename) -> None:
    load = from_file(filename)
    stats = organize(load)

    try:
        m = sys.argv[1].lower()

    except:
        print('ERROR: No arguments given...')
        print('Usage: ./visualizer.py (-p | -s)')
        print('E.g.')
        print('python generate.py -p')
        sys.exit(1)

    if m == '-p':
        plot_stats(stats)

    elif m == '-s':
        print_stats(stats)

    else:
        print('Argument not understood (use -p or -s) to plot or show stats.')



if __name__ == '__main__':
    main('../timings.txt')
