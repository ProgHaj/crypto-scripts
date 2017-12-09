import hex_operations as ho
import sys

path = "files/"

text   = sys.argv[1]
key    = sys.argv[2]
number = int(sys.argv[3])

xor = ho.xor_string(text, key)
print(xor)

b64 = ho.hex2b64(xor)
print(b64)

with open(path + "test" + str(number), "w") as test:
    test.write(b64.decode())


