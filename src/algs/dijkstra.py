import numpy as np
import heapq as hq

def solve(self):

    start = self.start
    end = self.end

    # set initial value
    start.dist = 0

    # bool array
    visited = np.full((self.y, self.x), False)

    # initiate vars
    explored = 0
    goal = np.inf

    # priority queue
    pq = [start]


    # dicretions
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
                node = self.get_node(near)
                # and if not visited
                if not visited[node.location]:
                    visited[node.location] = True

                    cy, cx = current.location
                    ny, nx = node.location
                    # calculate difference in locations
                    distance = abs(cy-ny) if cy-ny != 0 else abs(cx-ny)
                    # set total distance and via node
                    node.dist = current.dist + distance
                    node.via = self.get_node_index(cy, cx)
                    print(node)

                    hq.heappush(pq, node)

    path = []
    current = end
    while current != start:
        path.append(current)
        current = self.nodes[current.via]

    # append the start node
    path.append(self.start)

    path = path[::-1]

    self.solved = True
    self.path = path
    # path, nodes explored, length of path
    return explored, path, len(path)
