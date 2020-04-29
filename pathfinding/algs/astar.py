import numpy as np
import heapq as hq

def solve(self):

    start = self.start
    end = self.end

    #goal coordinates for calculating a*
    gy, gx = end.location

    # set initial value
    start.dist = 0
    start.dist_goal = np.hypot(start.location[0]-gy, start.location[1]-gx)
    start.combined = start.dist + start.dist_goal

    # bool array
    visited = np.full((self.y, self.x), False)

    # initiate vars
    explored = 0
    goal = np.inf

    # priority queue
    pq = [start]


    # directions
    # w s e n
    # 0 1 2 3

    while pq:
        # explored nodes
        explored += 1

        current = hq.heappop(pq)

        # if dist to node > to goal; break
        if current.dist > goal:
            break

        if current == end:
            goal = current.dist


        for near in current.nearby:
            # if not a wall
            if near is not None:
                node = self.get_node(near[0])
                # and if not visited
                if not visited[node.location]:
                    visited[node.location] = True

                    cy, cx = current.location
                    ny, nx = node.location

                    # animate stuff
                    self.frame(cy, cx, ny, nx)

                    # calculate difference in locations (one is always 0)
                    distance = abs(cy-ny) + abs(cx-nx)
                    # set total distance and via node
                    node.dist = current.dist + distance
                    node.via = (cy, cx)

                    # distance to goal (Pythagoras)
                    node.dist_goal = np.hypot(ny-gy, nx-gx)

                    node.combined = node.dist + node.dist_goal

                    # push new node into heap
                    hq.heappush(pq, node)

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
