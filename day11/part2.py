from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pprint

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def print_grid(grid: dict[tuple[int, int], int], size: int) -> None:
    printable = [[0]*size for _ in range(size)]
    for y, x in grid:
        printable[y][x] = grid[(y, x)]

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(printable)
    print()

def adjacent(x: int, y:int) -> Generator[tuple[int, int], None, None]:
    yield x - 1, y - 1
    yield x - 1, y
    yield x - 1, y + 1
    yield x, y - 1
    yield x, y + 1
    yield x + 1, y - 1
    yield x + 1, y
    yield x + 1, y + 1

def compute(s: str) -> int:
    lines = s.splitlines()
    grid_size = len(lines)

    grid = defaultdict(lambda: -1000000)
    for y, line in enumerate(lines):
        for x, num in enumerate(line):
            grid[(y, x)] = int(num)

    total_flashes = 0
    curr_round = 0
    while 1:
        curr_round += 1
        print_grid(grid, grid_size)
        flashed = set()
        stack = []
        for pt in grid:
            grid[pt] += 1
            if grid[pt] > 9:
                stack.append(pt)

        while stack:
            y, x = stack.pop()
            if (y, x) not in flashed:
                flashed.add((y, x))
                grid[(y, x)] = 0
                for neighbor_x, neighbor_y in adjacent(y, x):
                    if (neighbor_x, neighbor_y) in grid and (neighbor_x, neighbor_y) not in flashed:
                        grid[(neighbor_x, neighbor_y)] += 1
                        if grid[(neighbor_x, neighbor_y)] > 9:
                            stack.append((neighbor_x, neighbor_y))

        if len(flashed) == grid_size**2:
            return curr_round


    return total_flashes


INPUT_S = '''\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'''

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 195),
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
