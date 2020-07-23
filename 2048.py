from random import randint
from random import choice
from collections import defaultdict
from subprocess import call

board = {}


def startboard():
    """Fills the board with zeros"""
    global board
    for x in range(1,5):
        for y in range(1,5):
            board[(x,y)] = 0


def newblock(*, minimum=1, maximum=4):
    """Adds a new block in a random unfilled position (either two (90% chance) or four (10% chance))
    
    Returns False if there are no unfilled positions otherwise returns True
    """
    global board
    newcell = (randint(minimum, maximum),randint(minimum, maximum))
    tried = set(newcell)
    while board[newcell] != 0:
        newcell = (randint(minimum, maximum),randint(minimum, maximum))
        tried.add(newcell)
        if len(tried) == 16:
            return False
    board[newcell] = choice((2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
    return True


def getlines(row, column):
    """Returns a dictionary of lists sorted by either rows or columns

    row -- should be 1 if right -1 if left, otherwise 0
    column -- should be 1 if up -1 if down, otherwise 0
    """
    lines = defaultdict(list)
    start, stop = [[None, (1, 5), (4, 0)][column], (1, 5), (4, 0)][row]
    for x, y in board:
        for sort in range(start, stop, row + column):
            if x * abs(row) == sort or y * abs(column) == sort:
                lines[sort].append((x,y))
    return lines


def enter():
    entry = input('-- ')
    while entry not in 'wasd':
        entry = input('-- ')
    return entry


def move(entry):
    """Takes input and uses it to move cells and merge them

    entry -- players input
    """
    global board
    entry = ' wasd'.index(entry)
    row = abs(entry - 3) - 1
    column = abs(entry - 2) - 1
    for line in getlines(row, column).values():
        print(line)
        values = [board[(x, y)] for x, y in line if board[(x, y)] > 0] + [0]
        incomplete = True # Add adjacant values
        newvalues = []
        while incomplete:
            incomplete = False
            print(values)
            for e1, e2 in zip(values, values[1:]):
                print(e1, e2)
                if e1 == e2:
                    newvalues.append(e1 + e2)
                    values.remove(e1)
                    values.remove(e2)
                    incomplete = True
                    print(e1, e2, '->', e1 + e2)
                    break
                else:
                    newvalues.append(e1)
                    values.remove(e1)
                    print(e1, '!=', e2)
        values = newvalues
            # if len(values) > 1:
            #     for side in (-1, 1):
            #         if values[values.index(cell) + side] == cell:
            #             values.pop(values.index(cell) + side)
            #             values[values.index(cell)] = cell * 2
        values = values + [0] * (4 - len(values)) # Add zeros to make length four
        # if row + column == 1:
        #     values = [cell * -1 + 5 for cell in values]
        print(row, column)
        print(values)
        for (x, y), value in zip(line, values): # Update board with the modified line
            board[(x, y)] = value


def build():
    """Print board to stdout"""
    #call('clear',shell=True)
    print('---------------------')
    for y in range(4, 0, -1):
        print('|',end='')
        for x in range(1, 5):
            if x > 1:
                print('|',end='')
            print(board[(x,y)],end='')
            for _ in range(1,5 - len(str(board[(x,y)]))):
                print(' ',end='')
        print('|\n---------------------')



if __name__ == '__main__':
    startboard()
    while newblock():
        build()
        move(enter())
    build()