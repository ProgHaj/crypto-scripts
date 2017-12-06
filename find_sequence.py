import binascii
from hex_operations import xor_hex
from hex_operations import xor
from hex_operations import int2hexbyte

def find_char(sequence):
    h1 = binascii.a2b_hex(sequence)

    # Character? not letter? hmm. Should be this

    ranking = {}
    amount_of_bytes = 1


    for char in range(amount_of_bytes * 256):
        h2 = int2hexbyte(char)

        temp_h3 = xor_hex(h1,h2)

        ranking[char] = build_char_dictionary(binascii.a2b_hex(temp_h3))

    temp_i = 0
    temp_rank = 0

    for i, rank in enumerate(rank_list(ranking)):
        if rank > temp_rank:
            temp_rank = rank
            temp_i = i

    return int2hexbyte(temp_i)



def build_char_dictionary(string1):
    ranking = {}
    for char_in_seq in string1:
        if not ranking.get(char_in_seq):
            ranking[char_in_seq] = 0

        ranking[char_in_seq] += 1

    return ranking



def rank_list(ranking_dict):
    """apply some ranking"""

    # TODO: temporary fix, please make mor generalize

    rank = []

    for key, value in ranking_dict.items():
        score = 0
        val_e = value.get(ord('e')) or 0
        val_t = value.get(ord('t')) or 0
        val_a = value.get(ord('a')) or 0
        val_o = value.get(ord('o')) or 0
        val_i = value.get(ord('i')) or 0
        val_n = value.get(ord('n')) or 0

        val_s = value.get(ord('s')) or 0
        val_h = value.get(ord('h')) or 0
        val_r = value.get(ord('r')) or 0
        val_d = value.get(ord('d')) or 0
        val_l = value.get(ord('l')) or 0
        val_u = value.get(ord('u')) or 0

        values = [[val_e, 0.12],
                  [val_t, 0.91],
                  [val_a, 0.82],
                  [val_o, 0.75],
                  [val_i, 0.7],
                  [val_n, 0.67],

                  [val_s, 0.63],
                  [val_h, 0.61],
                  [val_r, 0.6],
                  [val_d, 0.43],
                  [val_l, 0.4],
                  [val_u, 0.28]]

        for val in values:
            score += val[0] * val[1]

        rank.append(score)

    return rank


def find_xor_sequence(sequence):
    return xor_hex(binascii.a2b_hex(sequence), find_char(sequence))


def niceify_find_xor_sequence(seq):
    return binascii.a2b_hex(find_xor_sequence(seq))


if __name__ == '__main__':
    print(find_char('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
    print(niceify_find_xor_sequence('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
