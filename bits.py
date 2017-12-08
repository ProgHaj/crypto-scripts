import binascii
from enum import Enum, auto

class Type(Enum):
    BITS  = auto()
    HEX   = auto()
    TEXT  = auto()
    BYTES = auto()

    def get_list():
        return [Type.BITS, Type.HEX, Type.TEXT, Type.BYTES]


class BitConverter():
    def __init__(self, number):
        self.number = number
        self.bits   = '{0:b}'.format(number)
        self.byte   = '{0:x}'.format(number)
        self.hex    = binascii.unhexlify(self.byte)
        #self.text   =


    def __xor__(self, bc):
        b1 = self.bits
        b2 = bc.bits

        b3 = ""

        for i in range(max(len(b1),len(b2))):
            b3 += ((b1[i % len(b1)] + b2[i % len(b2)]) % 2)

        return b3

    def __equals__(self, bc):
        return self.bits == bc.bits

    def __gt__(self, bc):
        return int(self.bits, 2) > int(bc.bits, 2)

    def __lt__(self, bc):
        return int(self.bits, 2) < int(bc.bits, 2)

    def update_bits(self, bits):
        self.bits = bits



    def to_string(self):
        string = "bits: "
        string += self.bits
        string += "\n"
        string += "text:"
        string += self.text
        string += "\n"
        string += "b64:"
        string += self.b64
        string += "\n"
        string += "hex:"
        string += self.hex
        string += "\n"
        string += "bytes:"
        string += self.bytes
        return string








