import argparse
import hex_operations as ho
import repeating_xor
import re
import find_sequence as fs
import binascii as bi


DEBUG = 0

def setup():
    parser = argparse.ArgumentParser(description='This program will break'
                                     ' a base64 and repeated xor file using'
                                     ' a string of size 2->KEYSIZE')

    parser.add_argument('-f','--file',
                        required=True,
                        type=str,
                        action='store')


    parser.add_argument('--KEYSIZE',
                        required=True,
                        type=int,
                        action='store')


    return parser.parse_args()


def hamming_distance(bin_str1, bin_str2):
    bits1 = ho.bytes2bitsstring(bin_str1)
    bits2 = ho.bytes2bitsstring(bin_str2)

    different = 0
    for i in range(len(bits1)):
        if bits1[i] != bits2[i]:
            different += 1

    return different


def steps(args):
    """Performs the steps for breaking the specified file containing a xor
    encrypted text which after is b64'd. Returns top 3 found keys and entries."""
    with open(args.file, 'r') as seq_file:
        red_file_b64 = seq_file.read()
        red_file = ho.string_b642hex(red_file_b64)

        keysize = args.KEYSIZE
        list_of_distances = []

        # Find best keysize
        if DEBUG: print(red_file)

        print("hexify")

        try:
            while True:
                red_file = bi.a2b_hex(red_file)
        except:
            pass

        if DEBUG: print(red_file)

        if keysize*4 > len(red_file):
            raise Exception("Key length must be at most a fourth of the file"
                            " length -- otherwise values needs to be tweaked.")

        print("finding keysize", end="   ")

        for i in range(1,keysize):
            list_of_sizes = []
            temp_distances = []
            for j in range(1, 4): # change the end depending on text
                size1 = red_file[i*(j-1):i*j]
                for size2 in list_of_sizes:
                    temp_distances.append(hamming_distance(size2, size1))

                list_of_sizes.append(size1)


            normalized_distance = 0
            for distance in temp_distances:
                normalized_distance += distance

            normalized_distance = normalized_distance/(len(temp_distances) * i)


            list_of_distances.append([normalized_distance, i,
                                      len(temp_distances)])


        print("DONE")

        sorted_list = sorted(list_of_distances, key=lambda x: x[0])
        # makes list_of_distances[0] be the smallest distance-key pair, and [1] the
        # next best etc. the list contains entries with [distance, key]


        top_keys = [x[1] for x in sorted_list[0:3]]

        print("find best key for top 3 keysizes")

        texts = {}
        for chosen_length in top_keys:
            print("keysize: ", chosen_length)

            print("breaking text into blocks of keysize...")
            text_blocks = break_text_into_blocks(red_file, chosen_length)

            if DEBUG: print("text_blocks:")
            if DEBUG: print(text_blocks)
            print("transposing blocks...")
            transposed_blocks = transpose_blocks(text_blocks)
            if DEBUG: print("transposed_blocks:")
            if DEBUG: print(transposed_blocks)

            print("finding key...")
            key = b""
            score = 0
            close_candidates = b""

            print("b'", end="")
            for block in transposed_blocks:
                found = fs.find_char_hex(block)
                key += found[0][0]
                score += found[0][1]
                close_candidates += found[1][0]
                print(found[0][0].decode(), end="")

            print("'")

            if DEBUG: print(red_file)
            print("xoring key and file...")
            xor = ho.xor_hex(red_file, key)
            printable = bi.a2b_hex(xor)
            if DEBUG: print(printable)

            texts[chosen_length] = [printable, key, score, close_candidates]

        return texts


def break_text_into_blocks(text, keysize):
    """Returns a list with the 'text' seperated by keysize steps. so "hello",
    3 would return ["hell", "o"]"""
    return re.findall(b".{1,%i}" % keysize, text, re.MULTILINE|re.DOTALL)


def transpose_blocks(blocks):
    """Transpose blocks inside 'blocks'. This means that if we have 2 block
    [1,2] and [3,4] we will get [1,3] and [2,4]. If length is not the same
    (might be the case for the list block), then thoose aren't included."""
    transposed_blocks = []

    if len(blocks) == 0:
        raise Exception("Blocks need to have at least one block")

    for i in range(0,len(blocks[0])):
        temp_list = b""
        for block in blocks:
            if len(block) > i:
                byte = b"%x" % block[i]
                byte = byte.rjust(2, b'0')
                temp_list += byte

        if temp_list:
            temp_list_hex = bi.unhexlify(temp_list)
            transposed_blocks.append(temp_list_hex)

    return transposed_blocks


def get_best_entry(found_entries):
    entries = [[val[1], val[0], val[2]] for key, val in found_entries.items()]
    sorted_entries = sorted(entries, key=lambda x: x[2], reverse=True)
    return sorted_entries[0]


def print_entries(found_entries):
    print("Found entries:")
    for key,val in found_entries.items():
        print(key, val[1], val[2], ",    close candidate key: ", val[3])
        print(val[0])
        print()


if __name__ == '__main__':
    args = setup()
    found_entries = steps(args)
    print()
    entry = get_best_entry(found_entries)
    print("Key: ", entry[0])
    print()
    print("Text: ", entry[1].decode())
