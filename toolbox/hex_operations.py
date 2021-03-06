"""Module for performing different operations on raw hex data.

Made while doing Cryptopals challenges.

s representing a type of string. In theese cases they usualy are to be
transformed strings containing hex entries.

h is of the type bytes and containing hexas.

Use .decode to turn from bytes to string, but isn't recommended unless it is
for pretty-printing."""

import binascii

def string_hex2b64(s1):
    """Converts from (str)hex to base64"""
    h1 = binascii.a2b_hex(s1)
    return binascii.b2a_base64(h1, newline=False)


def string_b642hex(s1):
    """Converts from (str)base64 to hex"""
    h1 = binascii.a2b_base64(s1)
    return binascii.b2a_hex(h1)

def hex2b64(h1):
    """Converts from hex to base64"""
    return binascii.b2a_base64(h1, newline=False)

def b642hex(h1):
    """Converts from hex to base64"""
    h1 = binascii.a2b_base64(s1)
    return binascii.b2a_hex(h1)

def xor(s1, s2):
    """ Takes string s1 and s2 which are strings containing hexadecimals.
    Returns a xor'd hexadecimal represented bytes.

    Challenge 2 of Set1 cryptopals"""
    h1 = binascii.a2b_hex(s1)
    h2 = binascii.a2b_hex(s2)
    return xor_hex(h1,h2)


def xor_string(s1, s2):
    """ Takes string s1 and s2 which are strings containing characters.
    Returns a xor'd hexadecimal represented bytes.
    """
    h1 = s1.encode()
    h2 = s2.encode()
    return xor_hex(h1,h2)


def xor_hex(h1,h2):
    """ Takes hexbytes h1 and h2

    Returns a xor'd hexadecimal represented bytes.
    """

    h3 = bytes()
    if not len(h1) == len(h2):
        for i, byte1 in enumerate(h1):
            temp = b"%x" % (byte1 ^ h2[i % len(h2)])
            h3 +=  temp.rjust(2, b'0')
    else:
        for byte1, byte2 in zip(h1, h2):
            temp = b"%x" % (byte1 ^ byte2)
            h3 +=  temp.rjust(2, b'0')

    return h3



def bytes2bitsstring(h1):
    """Returns a string containing bits of a bytestring bytes"""
    bits = ""
    for byte in h1:
        bits += "{0:b}".format(byte).rjust(8, '0')

    return bits

def int2hexbyte(i):
    temp_hex = "%x" % i
    return binascii.a2b_hex(temp_hex.rjust(len(temp_hex) + (len(temp_hex) % 2),'0'))

