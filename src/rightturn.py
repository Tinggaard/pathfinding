def solve(self):

    start = self.nodes[0]
    end = self.nodes[-1]


    # initiate vars
    current = start
    path = [current]
    # count = 1

    direction = 1

    # dicretions
    # w s e n
    # 0 1 2 3

    while True:

        if current == end:
            return path, len(path)

        # west
        if direction % 4 == 0:
            if current.w is not None:
                current = self.nodes[current.w[0]]
                path.append(current)
                # count += 1
                direction -= 1
                continue
            direction += 1

        # south
        if direction % 4 == 1:
            if current.s is not None:
                current = self.nodes[current.s[0]]
                path.append(current)
                # count += 1
                direction -= 1
                continue
            direction += 1

        # east
        if direction % 4 == 2:
            if current.e is not None:
                current = self.nodes[current.e[0]]
                path.append(current)
                # count += 1
                direction -= 1
                continue
            direction += 1

        # north
        if direction % 4 == 3:
            if current.n is not None:
                current = self.nodes[current.n[0]]
                path.append(current)
                # count += 1
                direction -= 1
                continue
            direction += 1
