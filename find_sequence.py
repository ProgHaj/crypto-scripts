import binascii
from hex_operations import xor_hex
from hex_operations import xor
from hex_operations import int2hexbyte
import matplotlib.pyplot as plt

def find_char(sequence, _plot=False):
    h1 = binascii.a2b_hex(sequence)
    return find_char_hex(h1, _plot)

def find_char_hex(h1, _plot=False):

    # Character? not letter? hmm. Should be this

    ranking = {}
    amount_of_bytes = 1


    for char in range(amount_of_bytes * 256):
        h2 = int2hexbyte(char)

        temp_h3 = xor_hex(h1,h2)

        ranking[char] = build_char_dictionary(binascii.a2b_hex(temp_h3))

    temp_i = 0
    temp_rank = 0

    for i, rank in enumerate(rank_list(ranking, _plot)):
        if rank > temp_rank:
            temp_rank = rank
            temp_i = i

    #rank = rank_list(ranking, _plot)
    #scores = [[int2hexbyte(char), score] for char, score in enumerate(rank)]
    #scores_sorted =sorted(scores, key=lambda x: x[1], reverse=True)
    ### TO BE ADDED IF I NEED THE SECOND BEST and so on.

    temp_h3 = xor_hex(h1,int2hexbyte(temp_i))

    return int2hexbyte(temp_i)



def build_char_dictionary(string1):
    ranking = {}
    for char_in_seq in string1:
        if not ranking.get(char_in_seq):
            ranking[char_in_seq] = 0

        ranking[char_in_seq] += 1

    return ranking



def rank_list(ranking_dict, _plot=False):
    """apply some ranking"""

    # TODO: temporary fix, please make mor generalize

    rank = []
    normalize = len(ranking_dict.items())

    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', ' ']
    values  = ['8.167','1.492','2.782','4.253','12.702','2.228','2.015','6.094',
               '6.966','0.153','0.772','4.025','2.406','6.749', '7.507','1.929',
               '0.095','5.987','6.327','9.056','2.758','0.978','2.360','0.150',
               '1.974','0.074', '13']

    for key, value in ranking_dict.items():
        score = 0
        for i in range(len(letters)):
            temp   = value.get(ord(letters[i])) or 0
            score += temp * float(values[i])



        rank.append(score)

    if _plot:
        plot(rank)


    return rank


def plot(result):
    plt.plot(range(1,len(result) + 1), result, 'ro')
    plt.axis([0, len(result), 0, max(result)])
    plt.ylabel('Score')
    plt.show()



def find_xor_sequence(sequence):
    return xor_hex(binascii.a2b_hex(sequence), find_char(sequence))


def niceify_find_xor_sequence(seq):
    return binascii.a2b_hex(find_xor_sequence(seq))


if __name__ == '__main__':
    print(find_char('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
    print(niceify_find_xor_sequence('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
