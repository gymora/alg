import json
import sys

from chess import solve_board

DEFAULT_INPUT = "../input1.json"
DEFAULT_OUTPUT = "../output1.json"


def read_input(input_file):
    return json.load(
        open(input_file)
    )


def write_output(output, output_file):
    json.dump(
        output, open(output_file, 'w')
    )


def main(argv):
    input_file = argv[0] if len(argv) > 0 else DEFAULT_INPUT
    output_file = argv[1] if len(argv) > 1 else DEFAULT_OUTPUT
    input_problem = read_input(input_file)
    output = solve_board(input_problem)
    write_output(output, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
