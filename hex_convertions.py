import binascii

def hex_b64(hexadecimals):
    byte_seq = binascii.a2b_hex(hexadecimals)
    return binascii.b2a_base64(byte_seq).strip()


if __name__ == '__main__':
    import sys
    print(hex_b64(sys.argv[1]))
