import argparse
import hex_operations as ho
import repeating_xor
import re
import find_sequence as fs
import binascii as bi

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


def hamming_distance(str1, str2):
    bin_str1 = str1.encode()
    bin_str2 = str2.encode()
    bits1 = ho.bytes2bitsstring(bin_str1)
    bits2 = ho.bytes2bitsstring(bin_str2)

    different = 0
    for i in range(len(bits1)):
        if bits1[i] != bits2[i]:
            different += 1

    return different


def steps(args):
    """Performs the steps for breaking the specified file containing a xor
    encrypted text which after is b64'd. Returns the key."""
    with open(args.file, 'r') as seq_file:
        red_file_b64 = seq_file.read().strip()
        red_file = ho.b64_hex(red_file_b64)
        red_file = red_file.decode()

        keysize = args.KEYSIZE
        list_of_distances = []

        # Find best keysize
        for i in range(2,keysize):
            first_size  = red_file[0:i]
            second_size = red_file[i:i*2]
            third_size  = red_file[i*2:i*3]
            fourth_size = red_file[i*3:i*4]
            distance1 = hamming_distance(first_size, second_size)
            distance2 = hamming_distance(third_size, fourth_size)
            normalized_distance = (distance1 + distance2)/(i*2)  # more accurate

            list_of_distances.append([normalized_distance, i])

        sorted_list = sorted(list_of_distances, key=lambda x: x[0])
        # makes list_of_distances[0] be the smallest distance-key pair, and [1] the
        # next best etc. the list contains entries with [distance, key]

        text_blocks = break_text_into_blocks(red_file, sorted_list[1][1])
        transposed_blocks = transpose_blocks(text_blocks)

        key = b""
        for block in transposed_blocks:
            print(len(block))
            key += fs.find_char(block.encode())

        xor = ho.xor_hex(bi.a2b_hex(red_file), key)
        print(bi.a2b_hex(xor))


        return key





def break_text_into_blocks(text, keysize):
    """Returns a list with the 'text' seperated by keysize steps. so "hello",
    3 would return ["hell", "o"]"""
    return re.findall(".{1,%s}" % keysize, text)

def transpose_blocks(blocks):
    """Transpose blocks inside 'blocks'. This means that if we have 2 block
    [1,2] and [3,4] we will get [1,3] and [2,4]. If length is not the same
    (might be the case for the list block), then thoose aren't included."""
    transposed_blocks = []

    if len(blocks) == 0:
        raise Exception("Blocks need to have at least one block")

    for i in range(len(blocks[0])):
        temp_list = ""
        for block in blocks:
            if len(block) > i:
                temp_list += block[i]

        transposed_blocks.append(temp_list)

    return transposed_blocks



if __name__ == '__main__':
    args = setup()
    key = steps(args)
    print(key)
