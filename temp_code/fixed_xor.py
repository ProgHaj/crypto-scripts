import binascii

def xor(s1, s2):
    """ Takes string s1 and s2 which are strings containing hexadecimals.
    Returns a xor'd hexadecimal represented bytes"""
    h1 = binascii.a2b_hex(s1)
    h2 = binascii.a2b_hex(s2)

    h3 = bytes()
    for byte1, byte2 in zip(h1, h2):
        h3 += b"%x" % (byte1 ^ byte2)

    return h3
