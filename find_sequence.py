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

        ranking[char] = {}
        for char_in_seq in binascii.a2b_hex(temp_h3):
            if not ranking[char].get(char_in_seq):
                ranking[char][char_in_seq] = 0

            ranking[char][char_in_seq] += 1




    temp_i = 0
    temp_rank = 0

    for i, rank in enumerate(rank_list(ranking)):
        if rank > temp_rank:
            temp_rank = rank
            temp_i = i

    return int2hexbyte(temp_i)



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
        values = [[val_e, 0.12],
                  [val_t, 0.91],
                  [val_a, 0.82],
                  [val_o, 0.75],
                  [val_i, 0.7],
                  [val_n, 0.67]]

        for val in values:
            score += val[0] * val[1]

        rank.append(score)

    return rank


def find_xor_char(sequence):
    return xor_hex(binascii.a2b_hex(sequence), find_char(sequence))


if __name__ == '__main_':
    print(find_char('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
    print(binascii.a2b_hex(find_xor_char('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')))

