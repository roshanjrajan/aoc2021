from __future__ import annotations

import argparse
import os.path
import numpy as np

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# check if the board has 5 or more None values in a row, column or diagonal
def check_board(board, number):
    for row in board:
        row_none = [cell for cell in row if not np.isnan(cell)]

        if len(row_none) == 0:
            return np.nansum(board)

    for j, _ in enumerate(board[0]):
        col = board[:,j]
        col_none = [cell for cell in col if not np.isnan(cell)]

        if len(col_none) == 0:
            return np.nansum(board)
    return None


def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    lines = s.splitlines()
    numbers = [float(num) for num in lines[0].split(",")]
    boards = []
    board = []
    for line in lines[2:]:
        if not line:
            boards.append(board)
            board = []
        else:
            board.append([float(num) for num in line.split()])

    boards.append(board)

    boards = np.array(boards)
    winners = [False]*len(boards)

    for number in numbers:
        for board_num, board in enumerate(boards):
            for row in board:
                for i, cell in enumerate(row):
                    if cell == number:
                        row[i] = np.nan
                        break

            if not winners[board_num]:
                val = check_board(board, number)
                if val:
                    winners[board_num] = True
                    last_winner = int(number) * val
    return last_winner


INPUT_S = '''\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 4512),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
