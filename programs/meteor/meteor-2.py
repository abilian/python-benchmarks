# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# contributed by Olof Kraigher
# modified by Tupteq
# 2to3

import sys

width = 5
height = 10

rotate = dict(E="NE", NE="NW", NW="W", W="SW", SW="SE", SE="E")
flip = dict(E="W", NE="NW", NW="NE", W="E", SW="SE", SE="SW")
move = dict(
    E=lambda x, y: (x + 1, y),
    W=lambda x, y: (x - 1, y),
    NE=lambda x, y: (x + (y % 2), y - 1),
    NW=lambda x, y: (x + (y % 2) - 1, y - 1),
    SE=lambda x, y: (x + (y % 2), y + 1),
    SW=lambda x, y: (x + (y % 2) - 1, y + 1),
)

solutions = []
masks = 10 * [0]

valid = lambda x, y: 0 <= x < width and 0 <= y < height
zerocount = lambda mask: sum([(1 << x) & mask == 0 for x in range(50)])


def findFreeCell(board):
    for y in range(height):
        for x in range(width):
            if board & (1 << (x + width * y)) == 0:
                return x, y


def floodFill(board, xxx_todo_changeme):
    (x, y) = xxx_todo_changeme
    if valid(x, y) and board & (1 << (x + width * y)) == 0:
        board |= 1 << (x + width * y)

        for f in list(move.values()):
            board |= floodFill(board, f(x, y))

    return board


def noIslands(mask):
    zeroes = zerocount(mask)

    if zeroes < 5:
        return False

    while mask != 0x3FFFFFFFFFFFF:
        mask = floodFill(mask, findFreeCell(mask))
        new_zeroes = zerocount(mask)

        if zeroes - new_zeroes < 5:
            return False

        zeroes = new_zeroes

    return True


def getBitmask(x, y, piece):
    mask = 1 << (x + width * y)

    for cell in piece:
        x, y = move[cell](x, y)
        if valid(x, y):
            mask = mask | (1 << (x + width * y))
        else:
            return False, 0

    return True, mask


def allBitmasks(piece, color):
    bitmasks = []
    for orientations in range(2):
        for rotations in range(6 - 3 * (color == 4)):
            for y in range(height):
                for x in range(width):
                    isValid, mask = getBitmask(x, y, piece)
                    if isValid and noIslands(mask):
                        bitmasks.append(mask)

            piece = [rotate[cell] for cell in piece]
        piece = [flip[cell] for cell in piece]

    return bitmasks


def generateBitmasks():
    global masksAtCell

    pieces = [
        ["E", "E", "E", "SE"],
        ["SE", "SW", "W", "SW"],
        ["W", "W", "SW", "SE"],
        ["E", "E", "SW", "SE"],
        ["NW", "W", "NW", "SE", "SW"],
        ["E", "E", "NE", "W"],
        ["NW", "NE", "NE", "W"],
        ["NE", "SE", "E", "NE"],
        ["SE", "SE", "E", "SE"],
        ["E", "NW", "NW", "NW"],
    ]

    masksAtCell = [[[] for j in range(10)] for i in range(width * height)]

    color = 0
    for piece in pieces:
        masks = allBitmasks(piece, color)
        masks.sort()
        cellMask = 1 << (width * height - 1)
        cellCounter = width * height - 1
        j = len(masks) - 1

        while j >= 0:
            if (masks[j] & cellMask) == cellMask:
                masksAtCell[cellCounter][color].append(masks[j])
                j = j - 1
            else:
                cellMask = cellMask >> 1
                cellCounter -= 1
        color += 1


def solveCell(cell, board):
    if to_go <= 0:
        # Got enough solutions
        pass
    elif board == 0x3FFFFFFFFFFFF:
        # Solved
        addSolutions()
    elif board & (1 << cell) != 0:
        # Cell full
        solveCell(cell - 1, board)
    elif cell < 0:
        # Out of board
        pass
    else:
        for color in range(10):
            if masks[color] == 0:
                for mask in masksAtCell[cell][color]:
                    if mask & board == 0:
                        masks[color] = mask
                        solveCell(cell - 1, board | mask)
                        masks[color] = 0


def addSolutions():
    global to_go
    s = ""
    mask = 1
    for y in range(height):
        for x in range(width):
            for color in range(10):
                if masks[color] & mask != 0:
                    s += str(color)
                    break
                elif color == 9:
                    s += "."
            mask <<= 1

    # Inverse
    ns = ""
    for y in range(height):
        for x in range(width):
            ns += s[width - x - 1 + (width - y - 1) * width]

    # Finally append
    solutions.append(s)
    solutions.append(ns)
    to_go -= 2


def printSolution(solution):
    for y in range(height):
        for x in range(width):
            print(solution[x + y * width], end=" ")

        print("")
        if y % 2 == 0:
            print("", end=" ")
    print()


def solve(n):
    global to_go
    to_go = n
    generateBitmasks()
    solveCell(width * height - 1, 0)


if __name__ == "__main__":
    solve(int(sys.argv[1]))

    print("%d solutions found\n" % len(solutions))
    printSolution(min(solutions))
    printSolution(max(solutions))
