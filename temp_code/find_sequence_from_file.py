import find_sequence as fs
import hex_operations as ho
import sys


def get_best_sequence_xor_char(f):
    with open(f, 'r') as seq_file:
        sequences = seq_file.readlines()
        temp_max = 0
        ranking = {}
        for sequence in sequences:
            sequence = sequence.strip()

            char = fs.find_char(sequence)
            found_seq = fs.niceify_find_xor_sequence(sequence)
            found_seq = found_seq.strip()
            ranking[char] = fs.build_char_dictionary(found_seq)
            values = fs.rank_list(ranking)
            score = max(values)

            if score > temp_max:
                temp_max = score
                temp_seq = sequence
                temp_char = char
                temp_found_seq = found_seq

        print(temp_max)
        print(temp_seq)
        print(temp_char)
        print(temp_found_seq)


if __name__ == '__main__':
    get_best_sequence_xor_char(sys.argv[1])
