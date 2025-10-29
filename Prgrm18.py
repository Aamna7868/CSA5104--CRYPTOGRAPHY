def left_shift(bits, n):
    return bits[n:] + bits[:n]

# Input key from user (64-bit key as binary string)
key = input("Enter 64-bit key (as 0s and 1s): ")

if len(key) != 64:
    print("Error: Key must be 64 bits long.")
else:
    # Initial permutation choice 1 (removing parity bits)
    pc1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,
           10,2,59,51,43,35,27,19,11,3,60,52,44,36,
           63,55,47,39,31,23,15,7,62,54,46,38,30,22,
           14,6,61,53,45,37,29,21,13,5,28,20,12,4]

    key56 = ''.join([key[i-1] for i in pc1])
    C, D = key56[:28], key56[28:]

    shift_schedule = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    pc2 = [14,17,11,24,1,5,3,28,15,6,21,10,
           23,19,12,4,26,8,16,7,27,20,13,2,
           41,52,31,37,47,55,30,40,51,45,33,48,
           44,49,39,56,34,53,46,42,50,36,29,32]

    keys = []
    for shift in shift_schedule:
        C, D = left_shift(C, shift), left_shift(D, shift)
        combined = C + D
        subkey = ''.join([combined[i-1] for i in pc2])
        keys.append(subkey)

    print("\nGenerated 16 Subkeys:")
    for i, k in enumerate(keys, 1):
        print(f"K{i}: {k}")

    print("\nNote: Each subkey’s first 24 bits come from C (left 28 bits) "
          "and the second 24 bits come from D (right 28 bits).")
