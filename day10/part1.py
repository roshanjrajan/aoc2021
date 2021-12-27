from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

syntax_points = {
    ")" : 3,
    "]" : 57,
    "}" : 1197,
    ">" : 25137
}

opposite = {
    ")" : "(",
    "]" : "[",
    "}" : "{",
    ">" : "<"
}

def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    for line in lines:
        stack = []
        for bracket in line:
            match bracket:
                case "(" | "[" | "{" | "<":
                    stack.append(bracket)
                case _:
                    if opposite[bracket] != stack.pop():
                        total += syntax_points[bracket]

    return total


INPUT_S = '''\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 26397),
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
