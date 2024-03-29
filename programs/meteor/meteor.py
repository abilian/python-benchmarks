# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# contributed by: Olof Kraigher
# 2to3

from sys import argv

width = 5
height = 10

directions = {"E": 0, "NE": 1, "NW": 2, "W": 3, "SW": 4, "SE": 5}
rotate = {"E": "NE", "NE": "NW", "NW": "W", "W": "SW", "SW": "SE", "SE": "E"}
flip = {"E": "W", "NE": "NW", "NW": "NE", "W": "E", "SW": "SE", "SE": "SW"}
move = {
    "E": lambda x, y: (x + 1, y),
    "W": lambda x, y: (x - 1, y),
    "NE": lambda x, y: (x + (y % 2), y - 1),
    "NW": lambda x, y: (x + (y % 2) - 1, y - 1),
    "SE": lambda x, y: (x + (y % 2), y + 1),
    "SW": lambda x, y: (x + (y % 2) - 1, y + 1),
}

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

solutions = []
masks = [0 for i in range(10)]

valid = lambda x, y: (0 <= x) and (x < width) and (0 <= y) and (y < height)
legal = lambda mask, board: (mask & board) == 0
zerocount = lambda mask: sum([((1 << x) & mask) == 0 for x in range(50)])


def findFreeCell(board):
    for y in range(height):
        for x in range(width):
            if board & (1 << (x + width * y)) == 0:
                return x, y


def floodFill(board, xxx_todo_changeme):
    (x, y) = xxx_todo_changeme
    if not valid(x, y):
        return board
    if board & (1 << (x + width * y)) != 0:
        return board

    board = board | (1 << (x + width * y))

    for f in list(move.values()):
        board = board | floodFill(board, f(x, y))

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


def solveCell(cell, board, n):

    global solutions, masks, masksAtCell

    if len(solutions) >= n:
        return

    if board == 0x3FFFFFFFFFFFF:
        # Solved
        s = stringOfMasks(masks)
        solutions.append(s)
        solutions.append(inverse(s))
        return

    if board & (1 << cell) != 0:
        # Cell full
        solveCell(cell - 1, board, n)
        return

    if cell < 0:
        # Out of board
        return

    for color in range(10):
        if masks[color] == 0:
            for mask in masksAtCell[cell][color]:
                if legal(mask, board):
                    masks[color] = mask
                    solveCell(cell - 1, board | mask, n)
                    masks[color] = 0


def solve(n):
    generateBitmasks()
    solveCell(width * height - 1, 0, n)


def stringOfMasks(masks):
    s = ""
    mask = 1
    for y in range(height):
        for x in range(width):
            for color in range(10):
                if (masks[color] & mask) != 0:
                    s += str(color)
                    break
                elif color == 9:
                    s += "."
            mask = mask << 1
    return s


def inverse(s):
    ns = [x for x in s]

    for x in range(width):
        for y in range(height):
            ns[x + y * width] = s[width - x - 1 + (width - y - 1) * width]

    return s


def printSolution(solution):
    for y in range(height):
        for x in range(width):
            print(solution[x + y * width], end=" ")

        if (y % 2) == 0:
            print("")
            print("", end=" ")
        else:
            print("")


if not len(argv) > 1:
    exit()

solve(int(argv[1]))
print(len(solutions), "solutions found")
print()
printSolution(min(solutions))
print()
printSolution(max(solutions))
print()
