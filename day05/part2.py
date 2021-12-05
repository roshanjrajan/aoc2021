from __future__ import annotations

import argparse
import numpy as np
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# def print_graph(graph: list[int][int]) -> None:
#     graph_printable = []
#     for i, row in enumerate(graph):
#         if i >= 10:
#             break
#         graph_printable.append(row[:10])

#     print(graph_printable)

def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    lines = s.splitlines()
    graph = [[0]*1000 for _ in range(1000)]
    for line in lines:
        left, right = line.split(' -> ')
        left_y, left_x = left.strip().split(',')
        left_y, left_x = int(left_y), int(left_x)

        right_y, right_x = right.strip().split(',')
        right_y, right_x = int(right_y), int(right_x)

        if right_y != left_y and right_x != left_x:
            if right_y < left_y:
                if right_x < left_x:
                    x = right_x
                    for i in range(right_y, left_y+1):
                        graph[x][i] += 1
                        x += 1
                else:
                    x = right_x
                    for i in range(right_y, left_y+1):
                        graph[x][i] += 1
                        x -= 1
            else:
                if left_x < right_x:
                    x = left_x
                    for i in range(left_y, right_y+1):
                        graph[x][i] += 1
                        x += 1
                else:
                    x = left_x
                    for i in range(left_y, right_y+1):
                        graph[x][i] += 1
                        x -= 1

        if right_x == left_x:
            small, big = min(left_y, right_y), max(left_y, right_y)
            for i in range(small, big + 1):
                graph[right_x][i] += 1
        elif right_y == left_y:
            small, big = min(left_x, right_x), max(left_x, right_x)
            for i in range(small, big + 1):
                graph[i][left_y] += 1

        #print(np.matrix(graph))

    count = 0
    for row in graph:
        for i, _ in enumerate(row):
            if row[i] > 1:
                count += 1
    return count


INPUT_S = '''\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 5),
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
