from __future__ import annotations

import argparse
import os.path

import pytest
import pprint

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def print_data(data: set[tuple[int, int]]) -> None:
    max_y = 0
    max_x = 0

    for y, x in data:
        max_x = max(max_x, x + 1)
        max_y = max(max_y, y + 1)

    printable = [["."]*max_x for _ in range(max_y)]

    for y, x in data:
        printable[y][x] = "#"

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(printable)
    print()

def compute(s: str) -> int:
    lines = s.splitlines()
    data = set()
    instructions = []
    for line in lines:
        if not line:
            continue

        if "," in line:
            x, y = line.split(",")
            data.add((int(y), int(x)))
        elif "=" in line:
            before, split_line = line.split("=")
            instructions.append((before[-1], int(split_line)))
        else:
            print("not supposed to happen")

    print(data)
    print(instructions)

    for direction, line_num in [instructions[0]]:
        next_data = set()
        for (y, x) in data:
            if direction == "y":
                if y < line_num:
                    next_data.add((y, x))
                elif y > line_num:
                    new_y = line_num - (y - line_num)
                    next_data.add((new_y, x))
            elif direction == "x":
                if x < line_num:
                    next_data.add((y, x))
                elif x > line_num:
                    new_x = line_num - (x - line_num)
                    next_data.add((y, new_x))

    return len(next_data)


INPUT_S = '''\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 17),
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
