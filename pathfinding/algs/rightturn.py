def rightturn(self):
    assert not self.solved

    start = self.start
    end = self.end

    second = self.get_node(start.nearby[1][0])
    second.via = 0

    # initiate vars
    path = [start, second]
    current = second
    travelled = 0

    direction = 0


    # directions
    # w s e n
    # 0 1 2 3

    while True:

        if current == end:
            self.solved = True
            self.path = path
            # nodes explored, path, number of nodes, length of path
            return len(set(path)), path, len(path), travelled

        if current == start:
            return False, len(set(path))

        # west
        if direction % 4 == 0:
            # if there is a node the that side
            if current.nearby[0] is not None:
                cy, cx = current.location

                following = current.nearby[0]
                current = self.get_node(following[0])
                current.via = following

                self.frame(cy, cx, *current.location)

                travelled += following[1]

                path.append(current)
                direction -= 1
                continue
            direction += 1

        # south
        if direction % 4 == 1:
            if current.nearby[1] is not None:
                cy, cx = current.location

                following = current.nearby[1]
                current = self.get_node(following[0])
                current.via = following

                self.frame(cy, cx, *current.location)

                travelled += following[1]

                path.append(current)
                direction -= 1
                continue
            direction += 1

        # east
        if direction % 4 == 2:
            if current.nearby[2] is not None:
                cy, cx = current.location

                following = current.nearby[2]
                current = self.get_node(following[0])
                current.via = following

                self.frame(cy, cx, *current.location)

                travelled += following[1]

                path.append(current)
                direction -= 1
                continue
            direction += 1

        # north
        if direction % 4 == 3:
            if current.nearby[3] is not None:
                cy, cx = current.location

                following = current.nearby[3]
                current = self.get_node(following[0])
                current.via = following

                self.frame(cy, cx, *current.location)

                travelled += following[1]

                path.append(current)
                direction -= 1
                continue
            direction += 1
