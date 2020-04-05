import numpy as np
from _collections import deque as dq

def solve(self):
    assert not self.solved

    start = self.start
    end = self.end

    # set initial value
    start.dist = 0

    # bool array
    visited = np.full((self.y, self.x), False)


    # initiate vars
    q = dq([start])
    explored = 0
    goal = np.inf

    # directions
    # w s e n
    # 0 1 2 3
    while q:
        # explored nodes
        explored += 1

        # get last item
        current = q.popleft()

        # stop iteration, if at the end
        if current == end:
            goal = current.dist
            break

        # the current node has now been visited
        visited[current.location] = True

        for near in current.nearby[::-1]:
            # if not a wall
            if near is not None:
                node = self.get_node(near[0])
                # and if not visited
                if not visited[node.location]:

                    cy, cx = current.location
                    ny, nx = node.location
                    # calculate difference in locations (one is always 0)
                    distance = abs(cy-ny) + abs(cx-nx)
                    # set total distance and via node
                    node.dist = current.dist + distance

                    # prepend the node to the list to visit
                    q.appendleft(node)
                    # set the via node for generating path
                    node.via = (cy, cx)


    # backtrack the path
    path = []
    current = end
    while current != start:
        path.append(current)
        current = self.get_node(current.via)

    # append the start node
    path.append(self.start)

    # reverse the path (from top to bottom)
    path = path[::-1]

    self.solved = True
    self.path = path
    # nodes explored, path, number of nodes, length of path
    return explored, path, len(path), goal
