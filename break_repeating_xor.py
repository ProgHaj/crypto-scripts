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
    encrypted text which after is b64'd. Returns the key."""
    with open(args.file, 'r') as seq_file:
        red_file_b64 = seq_file.read()
        red_file = ho.b64_hex(red_file_b64)

        keysize = args.KEYSIZE
        list_of_distances = []

        # Find best keysize
        print(red_file)
        red_file = bi.a2b_hex(red_file)
        print(red_file)
        red_file = bi.a2b_hex(red_file)
        for i in range(2,keysize, 2):
            first_size  = red_file[0:i]
            second_size = red_file[i:i*2]
            third_size  = red_file[i*2:i*3]
            fourth_size = red_file[i*3:i*4]


            distance1 = hamming_distance(first_size, second_size)
            distance2 = hamming_distance(first_size, third_size)
            distance3 = hamming_distance(first_size, fourth_size)
            distance4 = hamming_distance(second_size, third_size)
            distance5 = hamming_distance(second_size, fourth_size)
            distance6 = hamming_distance(third_size, fourth_size)

            normalized_distance = (distance1 + distance2 + distance3 +
                                   distance4 + distance5 + distance6)/(6*i)  # more accurate

            list_of_distances.append([normalized_distance, i])


        sorted_list = sorted(list_of_distances, key=lambda x: x[0])
        # makes list_of_distances[0] be the smallest distance-key pair, and [1] the
        # next best etc. the list contains entries with [distance, key]

        print(sorted_list[0][1])

        text_blocks = break_text_into_blocks(red_file, sorted_list[0][1])
        print("text_blocks:")
        print(text_blocks)
        transposed_blocks = transpose_blocks(text_blocks)
        print("transposed_blocks:")
        print(transposed_blocks)
        #red_file = bi.a2b_hex(red_file.encode())

        key = b""
        for block in transposed_blocks:
            key += fs.find_char_hex(block)[0][0]

        #red_file = bi.b2a_hex(red_file)
        print(red_file)
        xor = ho.xor_hex(red_file, key)
        #xor = ho.xor_string(red_file, key.decode())
        print(bi.a2b_hex(xor))
        print(sorted_list[0:10])
        #print(sorted_list[:30])



        return key


def break_text_into_blocks(text, keysize):
    """Returns a list with the 'text' seperated by keysize steps. so "hello",
    3 would return ["hell", "o"]"""
    return re.findall(b".{1,%i}" % keysize, text)


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
            #temp_list = "%x" % int(temp_list,2)
            #temp_list = temp_list.rjust(len(temp_list) + (len(temp_list) % 2), b'0')
            temp_list_hex = bi.unhexlify(temp_list)
            transposed_blocks.append(temp_list_hex)

    return transposed_blocks



if __name__ == '__main__':
    args = setup()
    key = steps(args)
    print(key)
