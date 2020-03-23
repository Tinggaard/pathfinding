def solve(self):
    assert not self.solved

    start = self.nodes[0]
    end = self.nodes[-1]

    second = self.nodes[start.nearby[1][0]]
    second.via = 0

    # initiate vars
    path = [start, second]
    current = second

    direction = 0

    # dicretions
    # w s e n
    # 0 1 2 3



    while True:

        if current == end:
            self.solved = True
            self.path = path
            # path, nodes explored, length of path
            return True, [len(set(path)), path, len(path)]

        if current == start:
            return False, len(set(path))

        # west
        if direction % 4 == 0:
            if current.nearby[0] is not None:
                prev = current.nearby[0][0]
                current = self.nodes[prev]
                current.via = prev

                path.append(current)
                direction -= 1
                continue
            direction += 1

        # south
        if direction % 4 == 1:
            if current.nearby[1] is not None:
                prev = current.nearby[1][0]
                current = self.nodes[prev]
                current.via = prev

                path.append(current)
                direction -= 1
                continue
            direction += 1

        # east
        if direction % 4 == 2:
            if current.nearby[2] is not None:
                prev = current.nearby[2][0]
                current = self.nodes[prev]
                current.via = prev

                path.append(current)
                direction -= 1
                continue
            direction += 1

        # north
        if direction % 4 == 3:
            if current.nearby[3] is not None:
                prev = current.nearby[3][0]
                current = self.nodes[prev]
                current.via = prev
                path.append(current)
                direction -= 1
                continue
            direction += 1
