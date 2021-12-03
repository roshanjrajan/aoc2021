from __future__ import annotations

import argparse
import json
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# largest
def compute_prefix_1(lines: list)->str:
    if len(lines) == 1:
        return lines[0]
    lines.sort()
    first_bit = lines[0][0]
    for i, line in enumerate(lines):
        bit = line[0]
        if bit != first_bit:
            if i <= len(lines)/2:
                return bit + compute_prefix_1([line[1:] for line in lines[i:]])
            else:
                return first_bit + compute_prefix_1([line[1:] for line in lines[:i]])

    return lines[0]

def compute_prefix(lines: list)->str:
    if len(lines) == 1:
        return lines[0]
    lines.sort()
    first_bit = lines[0][0]
    for i, line in enumerate(lines):
        bit = line[0]
        if bit != first_bit:
            if i <= len(lines)/2:
                return first_bit + compute_prefix([line[1:] for line in lines[:i]])
            else:
                return bit + compute_prefix([line[1:] for line in lines[i:]])

    
def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    lines = s.splitlines()

    sample = lines

    oxy = compute_prefix_1(sample)
    co2 = compute_prefix(sample)

    print(oxy, co2)
    return int(oxy, 2)* int(co2, 2)


INPUT_S = '''\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 230),
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
