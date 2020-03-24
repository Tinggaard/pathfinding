import numpy as np

def solve(self):
    assert not self.solved

    start = self.start
    end = self.end

    # bool array
    visited = np.full((self.y, self.x), False)


    # initiate vars
    q = [start]
    explored = 0

    # dicretions
    # w s e n
    # 0 1 2 3
    while q:
        # explored nodes
        explored += 1

        # get first item
        current = q.pop(0)

        # stop iteration, if at the end
        if current == end:
            break

        for node in current.nearby:
            # if not a wall
            if node is not None:
                n = self.get_node(node)
                # and if not visited
                if not visited[n.location]:
                    visited[n.location] = True
                    # append the node to the list to visit
                    q.append(n)
                    # set the via node for generating path
                    n.via = self.get_node_index(current.location[0], current.location[1])

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
