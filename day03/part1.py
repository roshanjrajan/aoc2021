from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    lines = s.splitlines()
    ones = [0]*len(lines[0])
    zeros = [0]*len(lines[0])
    for line in lines:
        for i, bit in enumerate(line):
            if bit == '0':
                zeros[i] += 1
            else:
                ones[i] += 1

    gam = epi = ""
    for i, _ in enumerate(zeros):
        if zeros[i] > ones[i]:
            gam += "0"
            epi += "1"
        elif zeros[i] < ones[i]:
            gam += "1"
            epi += "0"
        else:
            AssertionError(f"Zeros and Ones at {i=} are the same {zeros=} {ones=}")

    return int(gam, 2) * int(epi, 2)


INPUT_S = '''\

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
