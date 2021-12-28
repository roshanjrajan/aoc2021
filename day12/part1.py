from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def try_path(connections: dict[str, list[str]], curr_node: str, curr_path:list[str]) -> int:
    print(curr_path)
    if curr_node == "end":
        print("reached end")
        return 1

    total = 0
    for next_node_option in connections[curr_node]:
        if next_node_option == "end":
            print(curr_path + [next_node_option])
            total += 1
        elif next_node_option.islower() and next_node_option not in curr_path:
            next_path = curr_path + [next_node_option]
            total += try_path(connections, next_node_option, next_path)
        elif next_node_option.islower() and next_node_option in curr_path:
            continue
        elif next_node_option.isupper():
            next_path = curr_path + [next_node_option]
            total += try_path(connections, next_node_option, next_path)

    return total


def compute(s: str) -> int:
    lines = s.splitlines()
    connections = defaultdict(list)
    for line in lines:
        left, right = line.split("-")
        connections[left].append(right)
        connections[right].append(left)


    return try_path(connections, "start", ["start"])


INPUT_S = '''\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''

INPUT2_S = '''\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
'''

INPUT3_S = '''\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 10),
        (INPUT2_S, 19),
        (INPUT3_S, 226),
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
