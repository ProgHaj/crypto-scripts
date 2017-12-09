# crypto-scripts
This repository contains a set of scripts created while doing The Matasano Crypto Challenges.



## Problems
### set 1 project 6
Had a problem with project 6 which took a bit too much time to solve. I made a test script to generate a working encrypted + b64 file from a text and a key. My code passed my test when the text was small, but when I produced longer text it would introduce a bug, and the correct text wouldn't be found. 

After some debugging I found out that my regex findall script didn't include \n (and \r or so as well) which made my text seperator not seperate as it should. This was easilly fixed by including re.MULTILINE|re.DOTALL in the findall call.

Learnt how to properly use binascii.hexlify and binascii.unhexlify during the debugging which was a big plus.
