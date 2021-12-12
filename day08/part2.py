from __future__ import annotations

import argparse
import os.path
import pytest

from collections import defaultdict

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

segment_from_index = [
    [0, 1, 2, 3, 4, 5],
    [1, 2],
    [0, 1, 3, 4, 6],
    [0, 1, 2, 3, 6],
    [1, 2, 5, 6],
    [0, 2, 3, 5, 6],
    [0, 2, 3, 4, 5, 6],
    [0, 1, 2],
    [0, 1, 2, 3, 4, 5, 6],
    [0, 1, 2, 3, 5, 6]
]


def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass
    total = 0
    unique_lens = [2, 3, 4, 7]
    unique_numbers = [1, 7, 4, 8]
    lines = s.splitlines()
    for line in lines:
        inputs_raw, outputs_raw = line.split(" | ")
        solutions = [""]*10
        segments = [""]*7
        length_to_number = defaultdict(list)
        inputs = inputs_raw.split()

        for input_s in inputs:
            input_s = "".join(sorted(input_s))
            if len(input_s) in unique_lens:
                solutions[unique_numbers[unique_lens.index((len(input_s)))]] = input_s

            length_to_number[len(input_s)].append(input_s)

        # compare len(3) with len(2) to get segment in
        curr_char = set(list(length_to_number[3][0])).difference(set(list(length_to_number[2][0]))).pop()
        segments[0] = curr_char

        # compare len(7) with len(6) to find segment at 1
        checker = list(length_to_number[2][0])
        for value in length_to_number[6]:
            difference = set(list(length_to_number[7][0])).difference(set(list(value))).pop()

            if difference in checker:
                segments[1] = difference
                break

        # knowing segment at 1 helps you find segment at 2
        char_for_num_2 = [x for x in checker if x != segments[1]][0]
        segments[2] = char_for_num_2

        # compare len(6) with (len(4) + segment[0])
        checker = list(length_to_number[4][0]) + [segments[0]]
        for value in length_to_number[6]:
            difference = set(list(value)).difference(set(checker))

            if len(difference) == 1:
                segments[3] = difference.pop()
                break


        # compare len(5) with known
        checker = segments
        for value in length_to_number[5]:
            difference = set(list(value)).difference(set(checker))

            if len(difference) == 1:
                segments[6] = difference.pop()
                break

        char_for_num_6 = [x for x in length_to_number[4][0] if x not in segments][0]
        segments[5] = char_for_num_6


        char_for_num_4 = [x for x in length_to_number[7][0] if x not in segments][0]
        segments[4] = char_for_num_4

        for i, segment_index in enumerate(segment_from_index):
            curr_number = "".join(sorted([segments[x] for x in segment_index]))
            solutions[i] = curr_number

        # Match outputs to solution
        outputs = outputs_raw.split()

        output_num = ""
        for output in outputs:
            output = "".join(sorted(output))

            output_num += str(solutions.index(output))

        total += int(output_num)


    return total

INPUT_1 = '''acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'''

INPUT_S = '''\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_1, 5353),
        (INPUT_S, 61229),
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
