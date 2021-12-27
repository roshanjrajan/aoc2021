from __future__ import annotations

import argparse
import collections
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def get_neighbors(x: int, y:int) -> Generator[tuple[int, int], None, None]:
    yield x - 1, y
    yield x + 1, y
    yield x, y-1
    yield x, y + 1

def compute(s: str) -> int:
    data = collections.defaultdict(lambda: 9)
    lines = s.splitlines()
    for r, line in enumerate(lines):
        for c, number in enumerate(line):
            data[(r, c)] = int(number)

    total = 1
    low_points = []
    for (row, col), num in data.items():
            if all([data.get(point, 9)> num for point in get_neighbors(row, col)]):
                total += num + 1
                low_points.append((row, col))

    print(total)
    print(low_points)
    basins = []
    marked = [[False]*len(row) for row in data]
    for x, y in low_points:
        visited = set()
        stack = [(x, y)]
        while stack:
            curr_x, curr_y = stack.pop()
            visited.add((curr_x, curr_y))
            for point in get_neighbors(curr_x, curr_y):
                if point not in visited and data[point] < 9:
                    stack.append(point)

        basins.append(len(visited))

    basins.sort()
    print(basins)

    total = 1
    for basin in basins[-3:]:
        print(basin)
        total *= basin

    return total


INPUT_S = '''\
2199943210
3987894921
9856789892
8767896789
9899965678
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 1134),
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
