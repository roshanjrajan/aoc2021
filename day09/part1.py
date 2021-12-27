from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    data = []
    lines = s.splitlines()
    for line in lines:
        numbers = []
        for number in line:
            numbers.append(int(number))
        data.append(numbers)

    total = 0
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
                total += num + 1

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
        (INPUT_S, 15),
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
