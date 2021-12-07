from __future__ import annotations

import argparse
import json
import os.path
from collections import defaultdict

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    fishes = defaultdict(int)
    for fish in s.splitlines()[0].split(","):
        fishes[int(fish)] += 1

    # 80 for part1 256 for part2
    for day in range(256):
        next_fishes = defaultdict(int)
        for fish in fishes:
            if fish == 0:
                next_fishes[8] += fishes[fish]
                next_fishes[6] += fishes[fish]
            else:
                next_fishes[fish - 1] += fishes[fish]
        fishes = next_fishes
        total = 0
        for fish in fishes:
            total += fishes[fish]

    total = 0
    for fish in fishes:
        total += fishes[fish]

    return total


INPUT_S = '''\
3,4,3,1,2
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
