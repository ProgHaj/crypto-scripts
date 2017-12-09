
#https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
# High lvl overview:
#
# KeyExpansions — round keys are derived from the cipher key using Rijndael's key schedule. AES requires a separate 128-bit round key block for each round plus one more.
#
# InitialRound
### AddRoundKey—each byte of the state is combined with a block of the round key using bitwise xor.
# Rounds
### SubBytes — a non-linear substitution step where each byte is replaced with another according to a lookup table.
### ShiftRows — a transposition step where the last three rows of the state are shifted cyclically a certain number of steps.
### MixColumns — a mixing operation which operates on the columns of the state, combining the four bytes in each column.
### AddRoundKey
# Final Round (no MixColumns)
### SubBytes
### ShiftRows
### AddRoundKey.
