"""Module for performing different operations on raw hex data.

Made while doing Cryptopals challenges.

s representing a type of string. In theese cases they usualy are to be
transformed strings containing hex entries.

h is of the type bytes and containing hexas.

Use .decode to turn from bytes to string, but isn't recommended unless it is
for pretty-printing."""

import binascii

def hex_b64(s1):
    """Converts from (str)hex to (str)base64

    Challenge 1 of Set1 Cryptopals"""
    h1 = binascii.a2b_hex(s1)
    return binascii.b2a_base64(h1).strip()


def xor(s1, s2):
    """ Takes string s1 and s2 which are strings containing hexadecimals.
    Returns a xor'd hexadecimal represented bytes.

    Challenge 2 of Set1 cryptopals"""
    h1 = binascii.a2b_hex(s1)
    h2 = binascii.a2b_hex(s2)

    h3 = bytes()
    for byte1, byte2 in zip(h1, h2):
        h3 += b"%x" % (byte1 ^ byte2)

    return h3
