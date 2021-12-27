from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def get_basin(data: list[int][int], marked: list[int][int], index: tuple[int, int] ) -> int:
    row, col = index
    value = data[row][col]
    marked[row][col] = True
    print(value, index)
    if value == 9:
        return 0

    total = 1
    if col - 1 >= 0 and data[row][col-1] == value + 1 and not marked[row][col-1]:
        total += get_basin(data, marked, (row, col-1))

    if col + 1 < len(data[row]) and data[row][col+1] == value + 1 and not marked[row][col+1]:
        total += get_basin(data, marked, (row, col+1))

    if row - 1 >= 0 and data[row-1][col] == value + 1 and not marked[row - 1][col]:
        total += get_basin(data, marked, (row-1, col))

    if row + 1 < len(data) and data[row+1][col] == value + 1 and not marked[row+1][col]:
        total += get_basin(data, marked, (row+1, col))

    print(value, index, total)
    return total



def compute(s: str) -> int:
    data = []
    lines = s.splitlines()
    for line in lines:
        numbers = []
        for number in line:
            numbers.append(int(number))
        data.append(numbers)

    basins = []
    low_points = []
    for row, _ in enumerate(data):
        for col, _ in enumerate(data[row]):
            num = data[row][col]
            neighbors = []
            if col - 1 >= 0:
                neighbors.append(data[row][col-1])

            if col + 1 < len(data[row]):
                neighbors.append(data[row][col+1])

            if row - 1 >= 0:
                neighbors.append(data[row-1][col])

            if row + 1 < len(data):
                neighbors.append(data[row+1][col])


            less_than_neighbors = [neighbor for neighbor in neighbors if neighbor <= num]

            if len(less_than_neighbors) == 0:
                low_points.append((row, col))

    marked = [[False]*len(row) for row in data]
    for point in low_points:
        basins.append(get_basin(data, marked, point))
        print()

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
        (INPUT_S, 1),
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
