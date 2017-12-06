import sys
import hex_operations as ho
import argparse

def repeat_xor_on_file(file_path, xor_string):
    with open(file_path, 'r') as file_name:
        read_file = read(file_name)
        ho.xor_string(file_path, xor_string)


def setup_arg_parse():
    parser = argparse.ArgumentParser(description='This program will do a'
                                     ' repeated xor on a string/file using'
                                     ' the provided string.')

    parser.add_argument('--to_be_xored',
                        required=True,
                        type=str,
                        action='store')

    parser.add_argument('--xor_val',
                        required=True,
                        type=str,
                        action='store')

    parser.add_argument('-f',
                        required=False,
                        action='store_true')

    return parser.parse_args()

if __name__ == '__main__':
    args = setup_arg_parse()
    if args.f:
        get_best_sequence_xor_char(args.get(to_be_xored), args.get(xor_val))
        repeat_xor_on_file(args.to_be_xored, args.xor_val)
    else:
        print(ho.xor_string(args.to_be_xored, args.xor_val))
