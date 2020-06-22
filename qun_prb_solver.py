#!/usr/bin/python3.6
# ===============================================
#  8(or whatever number)Queens Problem Solver
#
# Author: Slick
# Date  : 06/05/2020
# ===============================================
from pprint import pprint
import random as r
import sys
import time


def make_board(width):
    """Makes a board of width X width size"""
    board = []
    for x in range(width):
        row = []
        for y in range(width):
            row.append(0)
        board.append(row)
    return board


def share_diag(x0, y0, x1, y1):
    """Returns True if Q's clash diagonally"""
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)
    # if dy == dx then they clash
    return dx == dy


def diag_clashes(board, r, c):
    """Return True if the queens at column c clashes with any other queen"""
    for row_num in range(len(board)):
        for space_num in range(len(board[row_num])):
            if board[row_num][space_num] == '[Q]':
                clash = share_diag(c, r, space_num, row_num)
                if clash:
                    return True


def board_check(board):
    """Returns True if board is completed"""
    queen_placed = 0
    for row in board:
        if '[Q]' in row:
            queen_placed += 1
    if queen_placed == len(board):
        return True
    else:
        return False


def already_found(board, board_list):
    """Returns True if board is in the board list"""
    if board in board_list:
        return True
    return False


def put_queen(board):
    """Main action: Places queens and checks to make sure they don't clash"""
    row = r.randint(0, len(board)-1)
    col = r.randint(0, len(board)-1)

    try:
        # Check the same row and column for clash
        if '[Q]' in board[row]:
            # print('\nWill not work (row)')
            return board
        for i in range(len(board)):
            if '[Q]' == board[i][col]:
                # print('\nWill not work (column)')
                return board
    except IndexError:
        # print('\nWill not work (Out of range)')
        return board

    # Checks for a diagonal clash
    clash = diag_clashes(board, row, col)

    # if okay to place, replaces index and column choice's 0 with a Q
    if not clash:
        try:
            del board[row][col]
            board[row].insert(col, '[Q]')
            # print('\nSuccess!')
            return board
        except IndexError:
            # print('\nProblem (Out of bounds)')
            return board
    # if there is a diagonal clash
    else:
        # print('\nWill not work (diagonal)')
        return board


def main():
    print(' 8 Queens Problem Solver '.center(45, '-'))
    try:
        # Starts by asking the desired board specs
        board_len = int(input('\nEnter the length of the board > '))
        s = int(input('Enter amount of solutions desired > '))
        try:
            buffer = input('Enter buffer depth OR\nPress ENTER for default scan (default=5000) > ')
            if int(buffer) < 5000:
                buffer = 5000
            else:
                print('\nInitializing...')
                time.sleep(2)
                buffer = int(buffer)
        except ValueError:
            time.sleep(1)
            print('\nUsing default buffer...')
            buffer = 5000
            time.sleep(2)
        # Keeps track of the # of solutions
        solutions = 0
        # a list to keep solutions
        s_ls = []
        while solutions < s:
            # initializing the first board
            board = make_board(board_len)
            loop = 1
            tries = 0
            while True:
                if loop > buffer:
                    if len(s_ls) == 0:
                        print('\nNo solutions found!\nTry changing the size of the board or increasing the buffer size')
                        sys.exit()
                    else:
                        print('\nThat\'s all she wrote!')
                        sys.exit()
                # If tries get to high, starts over with new board
                if tries > (12 * board_len):
                    board = make_board(board_len)
                    loop += 1
                    tries = 0
                board = put_queen(board)
                tries += 1
                # Checks if the board is completed
                win = board_check(board)
                # Checks if solution was already found
                duplicate = already_found(board, s_ls)
                if win and not duplicate:
                    solutions += 1
                    print(f'\nHere is Solution #{solutions}!\nvvvvvvvvvvvvvvvvvvvvv')
                    s_ls.append(board)
                    pprint(board)
                    break
    except KeyboardInterrupt:
        print(f'Good you quit while you\'re ahead...\nProbably weren\'t going to find anything else.')


if __name__ == '__main__':
    main()
