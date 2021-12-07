from __future__ import annotations

import argparse
import os.path
import sys

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = [int(line) for line in s.splitlines()[0].split(",")]
    prev_sum  = sys.maxsize
    for pos in range(min(numbers), max(numbers) + 1):
        curr_sum = 0
        for n in numbers:
            curr_sum += abs(n - pos)

        if curr_sum > prev_sum:
            return prev_sum
        else:
            prev_sum = curr_sum

    return prev_sum


INPUT_S = '''\
16,1,2,0,4,2,7,1,2,14
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 37),
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
