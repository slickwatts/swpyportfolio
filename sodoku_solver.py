# ===============================================
#                  Sudodku Solver
#
# Author: Slick
# Date  :
# ===============================================
import random as r
import sys


def rowcheck(board, row, col):
    """Checks the row of the specified block, returns True if no clash"""
    for x, r_o_w in enumerate(board):
        if x != row:
            continue
        for y, value in enumerate(board[x]):
            if y == col:
                continue
            if board[x][y] == board[row][col]:
                return False
    return True


def colcheck(board, row, col):
    """Checks the column of the specified block, returns True if no clash"""
    for i, r_o_w in enumerate(board):
        if i == row:
            continue
        elif r_o_w[col] == board[row][col]:
            return False
    return True


def subsquare_check(board, row, col):
    """Checks the subsquare of the specified block, returns True if no clash"""
    box_to_check = board[row][col]
    # ================TOP 3 Column CHECK======================
    if 0 <= row <= 2:
        # top left subsquare check
        if 0 <= col <= 2:
            for x, r in enumerate(board[:2+1]):
                for y, val in enumerate(r[:2+1]):
                    if [x, y] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
        # top mid subsquare check
        elif 3 <= col <= 5:
            for x, r in enumerate(board[:2+1]):
                for y, val in enumerate(r[3:(5+1)]):
                    if [x, y+3] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
        # top right subsquare check
        elif 6 <= row <= 8:
            for x, r in enumerate(board[:2+1]):
                for y, val in enumerate(r[6:]):
                    if [x, y+6] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
    # ================MID 3 Column CHECK======================
    elif 3 <= row <= 5:
        # mid left subsquare check
        if 0 <= col <= 2:
            for x, r_o_w in enumerate(board[3:(5 + 1)]):
                for y, val in enumerate(r_o_w[:2 + 1]):
                    if [x+3, y] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
        # mid mid subsquare check
        elif 3 <= col <= 5:
            for x, r_o_w in enumerate(board[3:(5 + 1)]):
                for y, val in enumerate(r_o_w[3:(5 + 1)]):
                    if [x+3, y+3] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
        # mid right subsquare check
        elif 6 <= col <= 8:
            for x, r in enumerate(board[3:(5 + 1)]):
                for y, val in enumerate(r[6:]):
                    if [x+3, y+6] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
    # ================BOT 3 Column CHECK======================
    elif 6 <= row <= 8:
        # bot left subsquare check
        if 0 <= col <= 2:
            for x, r in enumerate(board[6:]):
                for y, val in enumerate(r[:2 + 1]):
                    if [x+6, y] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
        # bot mid subsquare check
        elif 3 <= col <= 5:
            for x, r in enumerate(board[6:]):
                for y, val in enumerate(r[3:(5 + 1)]):
                    if [x+6, y+3] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
        # bot right subsquare check
        elif 6 <= col <= 8:
            for x, r in enumerate(board[6:]):
                for y, val in enumerate(r[6:]):
                    if [x+6, y+6] == [row, col]:
                        continue
                    elif val == box_to_check:
                        return False
    return True


def good_placement(board, row, col):
    """Tests for a good placement, returns True if all tests pass"""
    if board[row][col] == 0:
        return False
    if not colcheck(board, row, col):
        return False
    if not rowcheck(board, row, col):
        return False
    if not subsquare_check(board, row, col):
        return False
    return True


def place_digit(board, row, col):
    guess = r.choice([1,2,3,4,5,6,7,8,9])
    board[row].pop(col)
    board[row].insert(col, guess)


def backtrack(board, row, col):
    """Walks the board backwards, starting at the hanging block, and
       replaces all values with zero"""
    target = board[row][col]
    i = col
    board[row].pop(i)
    board[row].insert(i, 0)
    i -= 1

    while board[row][i] != target:
        # for x in range(col,col+nums_to_walk_back):
        if i == -1:
            row -= 1
            i = 8
        # replace the value in the board square with zero
        board[row].pop(i)
        board[row].insert(i, 0)
        i -= 1

    board[row].pop(i)
    board[row].insert(i, 0)


def print_board(board):
    print('_' * 44)
    for i, row in enumerate(board):
        print('\n')
        for x, value in enumerate(row):
            if (x + 1) % 3 == 0:
                print(f"{value}  | ", end="")
                if x == 8 and (i + 1) % 3 == 0:
                    print('\n' + '_' * 44)
            else:
                print(f"{value}    ", end="")
    print('\n')


def board_is_solved(board):
    for x in range(len(board)):
        for y in range(len(board[x])):
            if not good_placement(board, x, y) or board[x][y] == 0:
                return False
        return True


def solve(board, buffer_max=500):
    SOLVED = False
    buffer = 0
    while not SOLVED:
        # targeting each cell on the board individually
        for row in range(len(board)):
            for col in range(len(board[row])):
                # if cell == 0, then add a random number
                if board[row][col] == 0:
                    try:
                        #changes that number until it has no clashes
                        while not good_placement(board, row, col):
                            place_digit(board, row, col)
                            buffer += 1
                            if buffer > buffer_max:
                                backtrack(board, row, col)
                                solve(board)
                        if board_is_solved(board):
                            SOLVED = True
                    except RecursionError:
                        backtrack(board, row, col)
                        solve(board)
    print_board(board)
    print("Solved! Double check to make sure.")
    sys.exit(0)


sudoku_board = [
 [0,0,6,0,4,0,0,9,7],
 [0,4,0,7,3,0,0,1,0],
 [0,1,7,0,9,2,0,3,0],
 [6,0,0,0,7,0,0,8,0],
 [1,0,5,0,6,0,9,0,3],
 [0,2,0,0,1,0,0,0,6],
 [0,5,0,9,8,0,1,6,0],
 [0,9,0,0,5,6,0,7,0],
 [8,6,0,0,2,0,3,0,0]]
sdk2 = [[0,0,0,0,0,0,0,0,0] for x in range(9)]

if __name__ == '__main__':
    solve(sdk2)