import argparse
import hex_operations as ho
import repeating_xor

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
    with open(args.file, 'r') as seq_file:
        red_file = seq_file.read()

        keysize = args.KEYSIZE
        list_of_distances = []

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
        # next best etc.

        print(sorted_list[0:10])







if __name__ == '__main__':
    args = setup()
    steps(args)

