import sys
import pickle
from itertools import permutations
letters = 'abcdefghijklmnopqrstuvwxyz'.upper()
bias = {
 'A' :  8.55   ,     'K' :  0.81    ,    'U' :  2.68,
 'B' :  1.60   ,     'L' :  4.21    ,    'V' :  1.06,
 'C' :  3.16   ,     'M' :  2.53    ,    'W' :  1.83,
 'D' :  3.87   ,     'N' :  7.17    ,    'X' :  0.19,
 'E' : 12.10   ,     'O' :  7.47    ,    'Y' :  1.72,
 'F' :  2.18   ,     'P' :  2.07    ,    'Z' :  0.11,
 'G' :  2.09   ,     'Q' :  0.10    ,
 'H' :  4.96   ,     'R' :  6.33    ,
 'I' :  7.33   ,     'S' :  6.73    ,
 'J' :  0.22   ,     'T' :  8.94
}

grams2 = {
'TH' :  2.71     ,   'EN' :  1.13    ,    'NG' :  0.89,
'HE' :  2.33     ,   'AT' :  1.12    ,    'AL' :  0.88,
'IN' :  2.03     ,   'ED' :  1.08    ,    'IT' :  0.88,
'ER' :  1.78     ,   'ND' :  1.07    ,    'AS' :  0.87,
'AN' :  1.61     ,   'TO' :  1.07    ,    'IS' :  0.86,
'RE' :  1.41     ,   'OR' :  1.06    ,    'HA' :  0.83,
'ES' :  1.32     ,   'EA' :  1.00    ,    'ET' :  0.76,
'ON' :  1.32     ,   'TI' :  0.99    ,    'SE' :  0.73,
'ST' :  1.25     ,   'AR' :  0.98    ,    'OU' :  0.72,
'NT' :  1.17     ,   'TE' :  0.98    ,    'OF' :  0.71,
}

grams3 = {
'THE' :  1.81     ,   'ERE' :  0.31   ,     'HES' :  0.24,
'AND' :  0.73     ,   'TIO' :  0.31   ,     'VER' :  0.24,
'ING' :  0.72     ,   'TER' :  0.30   ,     'HIS' :  0.24,
'ENT' :  0.42     ,   'EST' :  0.28   ,     'OFT' :  0.22,
'ION' :  0.42     ,   'ERS' :  0.28   ,     'ITH' :  0.21,
'HER' :  0.36     ,   'ATI' :  0.26   ,     'FTH' :  0.21,
'FOR' :  0.34     ,   'HAT' :  0.26   ,     'STH' :  0.21,
'THA' :  0.33     ,   'ATE' :  0.25   ,     'OTH' :  0.21,
'NTH' :  0.33     ,   'ALL' :  0.25   ,     'RES' :  0.21,
'INT' :  0.32     ,   'ETH' :  0.24   ,     'ONT' :  0.20,
}

class frame():
    def __init__(self, frame, starting_pos):
        self.current_mapping = {}
        for letter in frame:
            self.current_mapping[letter] = letter

        self.position = starting_pos
        self.frame = frame
        self.orig_frame = frame
        self.length = len(frame)
        self.best_mapping = {}

    def move_frame(self, pos):
        self.pos = pos
        self.frame = self.get_frame(pos)

    def get_frame(self, pos, letters=letters):
        nof_letters = len(letters)
        start = pos
        current_frame = letters[pos:pos+self.length]
        pos += self.length
        if pos >= nof_letters:
            current_frame += letters[0:start]

        return current_frame

    def perms(self, val):
        if val==0:
            p = permutations(self.frame)
            for perm in p:
                yield perm
        elif val==1:
            for i in range(len(self.frame)):
                yield self.get_frame(i, self.frame)
        elif val==2:
            frame = self.frame
            import math
            sqrt = int(math.sqrt(self.length))
            frame = [self.frame[(sqrt*i % self.length + int(i/sqrt))] for i in
                     range(self.length)]

            for i in range(len(self.frame)):
                yield self.get_frame(i, self.frame)

    def ml_current_frame(self, text, comparer):
        """Most likely positions of the frame buffer in the frame.
        text = the whole text
        text_frame = the letters in the current frame, fx 'abcdef'
        Not testing every permutations, just those in cluster"""
        n = len(text)
        self.best_mapping[self.frame] = []
        best_score = 0
        best_mapping = ()
        entries = {}
        for temp_frame in self.perms(comparer):
            temp_text = text
            current_mapping = {self.orig_frame[j]: temp_frame[j] for j in
                               range(len(temp_frame))}

            for j in range(n):
                letter = text[j]
                if letter in current_mapping:
                    temp_text = temp_text[:j] + current_mapping[letter] + temp_text[j + 1:]

            score = 0
            len_temp = len(temp_text)
            for i in range(len_temp):
                letter = temp_text[i]
                score += bias[letter]/5
                if i < len_temp - 1:
                    g2 = letter + temp_text[i+1]
                    if g2 in grams2:
                        score += grams2[g2]*2

                if i < len_temp - 2:
                    g3 = letter + temp_text[i+1] + temp_text[i+2]
                    if g3 in grams3:
                        score += grams3[g3]*4

            mapping = (score, temp_text, current_mapping)
            if temp_text not in entries:
                entries[temp_text] = mapping

        entries = list(entries.values())
        entries.sort(key=lambda x: x[0])
        self.best_mapping[self.frame].extend(entries[5::-1])


def test_combinations(text, frames=(9,9,4,4), comparer=0):
    """Test different windows on the text, to see if one is better suited.
    Used for decoding a cipher which has clusters of letters, like abcdefg
    together"""


    frame_list = get_frames(frames, 0)
    f = [frame(i, 0) for i in frame_list]
    print('calculating best frames from original text')
    for fe in f:
        print('Calculating... Frame:', fe.frame)
        fe.ml_current_frame(text, comparer)
        print('Calculating... Done. Best frame:', list(fe.best_mapping.values())[0])
        pickle.dump(fe, open( fe.frame + ".p", "wb" ) )

    new_text = text
    for fe in f[::-1]:
        print('Calculating best together...')
        fe.ml_current_frame(new_text, comparer)
        new_text = list(fe.best_mapping.values())[0][0][1]
        print('Calculating... Currently best frame:', list(fe.best_mapping.values())[0])

    print('DONE')


    #print(frame_list)
    #real_text = text
    #move_frame() # to be implemented
    #swap_frame()
    #ml_pos_in_frame()

def get_frames(frames, start_index, letters=letters):
    frame_list = []
    i = start_index
    nof_letters = len(letters)
    for frame in frames:
        current_frame = letters[i:i+frame]
        i += frame
        if i >= nof_letters:
            i %= nof_letters
            current_frame += letters[0:i]

        frame_list.append(current_frame)

    return frame_list


def move_frame():
    pass

def swap_frame(frames, ):
    """swaps the frames with eachother"""
    pass



def find_ngrams(text, n=1):
    gram_dict = {}
    for i in range(len(text) - n + 1):
        gram_tuple = tuple(text[i + j] for j in range(n))
        if not gram_tuple in gram_dict:
            gram_dict[gram_tuple] = 0

        gram_dict[gram_tuple] += 1

    return gram_dict

if __name__=="__main__":
    if len(sys.argv) > 1:
        grams = find_ngrams(sys.argv[1], int(sys.argv[2]))
        print(grams)
