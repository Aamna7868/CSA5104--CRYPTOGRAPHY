def list_to_str(lst):
    return "".join(map(str, lst))

# S-BOX Definitions
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

# Permutation Definitions
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]

permute = lambda data, p: [data[i - 1] for i in p]
left_shift = lambda data, count: data[count:] + data[:count]
binary_xor = lambda a, b: [x ^ y for x, y in zip(a, b)]

def key_generation(key):
    p10_key = permute(key, P10)
    L, R = p10_key[:5], p10_key[5:]

    # K1
    L1, R1 = left_shift(L, 1), left_shift(R, 1)
    K1 = permute(L1 + R1, P8)

    # K2
    L2, R2 = left_shift(L1, 2), left_shift(R1, 2)
    K2 = permute(L2 + R2, P8)
    
    return K1, K2

def sbox_substitution(input_data, sbox):
    row = input_data[0] * 2 + input_data[3]
    col = input_data[1] * 2 + input_data[2]
    val = sbox[row][col]
    return [val // 2, val % 2]

def f_function(right_data, subkey):
    xor_data = binary_xor(permute(right_data, EP), subkey)
    L, R = xor_data[:4], xor_data[4:]
    s0_out = sbox_substitution(L, S0)
    s1_out = sbox_substitution(R, S1)
    return permute(s0_out + s1_out, P4)

def sdes_transform(data_block, key, k_order):
    K1, K2 = key_generation(key)
    K = [K1, K2] if k_order == 1 else [K2, K1] # Subkeys for 1st and 2nd round

    IP_data = permute(data_block, IP)
    L0, R0 = IP_data[:4], IP_data[4:]
    
    # Round 1
    L1 = binary_xor(L0, f_function(R0, K[0]))
    R1 = R0
    swapped = R1 + L1
    
    # Round 2
    L2, R2 = swapped[:4], swapped[4:]
    L2_final = binary_xor(L2, f_function(R2, K[1]))
    R2_final = R2
    
    return permute(L2_final + R2_final, IP_INV)

sdes_encrypt_block = lambda pt, key: sdes_transform(pt, key, 1) # k_order=1 (K1, K2)
sdes_decrypt_block = lambda ct, key: sdes_transform(ct, key, -1) # k_order=-1 (K2, K1)

def sdes_cbc_encrypt(plaintext_bits, key_bits, iv_bits):
    block_size = len(iv_bits)
    ciphertext_bits = []
    prev_block = iv_bits
    
    for i in range(0, len(plaintext_bits), block_size):
        block = plaintext_bits[i:i + block_size]
        xor_input = binary_xor(block, prev_block)
        cipher_block = sdes_encrypt_block(xor_input, key_bits)
        ciphertext_bits.extend(cipher_block)
        prev_block = cipher_block
        
    return ciphertext_bits

def sdes_cbc_decrypt(ciphertext_bits, key_bits, iv_bits):
    block_size = len(iv_bits)
    plaintext_bits = []
    prev_block = iv_bits
    
    for i in range(0, len(ciphertext_bits), block_size):
        block = ciphertext_bits[i:i + block_size]
        dec_block = sdes_decrypt_block(block, key_bits)
        plain_block = binary_xor(dec_block, prev_block)
        plaintext_bits.extend(plain_block)
        prev_block = block
        
    return plaintext_bits

# --- Main Execution: Test Vector Verification ---
IV_BIN = "10101010"
PT_BIN = "0000000100100011"
KEY_BIN = "0111111101"
EXPECTED_CT_BIN = "1111010000001011"

IV_BITS = [int(bit) for bit in IV_BIN]
PT_BITS = [int(bit) for bit in PT_BIN]
KEY_BITS = [int(bit) for bit in KEY_BIN]

print("--- S-DES CBC Verification ---")
print(f"Key (10-bit): {KEY_BIN}")
print(f"IV (8-bit):   {IV_BIN}")
print(f"Plaintext (PT): {PT_BIN}")
print(f"Expected Ciphertext: {EXPECTED_CT_BIN}")

# ENCRYPTION
ENCRYPTED_BITS = sdes_cbc_encrypt(PT_BITS, KEY_BITS, IV_BITS)
ENCRYPTED_BIN = list_to_str(ENCRYPTED_BITS)

print("\n--- Encryption Results ---")
print(f"Calculated CT: {ENCRYPTED_BIN}")
print(f"Verification: {'SUCCESS' if ENCRYPTED_BIN == EXPECTED_CT_BIN else 'FAILED'}")

# DECRYPTION
DECRYPTED_BITS = sdes_cbc_decrypt(ENCRYPTED_BITS, KEY_BITS, IV_BITS)
DECRYPTED_BIN = list_to_str(DECRYPTED_BITS)

print("\n--- Decryption Results ---")
print(f"Decrypted PT: {DECRYPTED_BIN}")
print(f"Verification: {'SUCCESS' if DECRYPTED_BIN == PT_BIN else 'FAILED'}")