def block_cipher(block, key):
    res = bytearray(block)
    for i in range(len(res)):
        res[i] ^= key[i % len(key)]
    return bytes(res)

def pad_plaintext(data, block_size):
    padding_len = block_size - (len(data) % block_size)
    if padding_len == 0:
        padding_len = block_size
    return data + bytes([padding_len] * padding_len)

def unpad_plaintext(padded_data):
    padding_len = padded_data[-1]
    if padding_len == 0 or padding_len > len(padded_data):
        return padded_data
    return padded_data[:-padding_len]

def cbc_encrypt(plaintext, iv, key):
    block_size = len(iv)
    ciphertext = b''
    prev_block = iv
    
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        xor_block = block_cipher(bytes(a ^ b for a, b in zip(block, prev_block)), key)
        ciphertext += xor_block
        prev_block = xor_block
    return ciphertext

def cbc_decrypt(ciphertext, iv, key):
    block_size = len(iv)
    plaintext = b''
    prev_block = iv
    
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        dec_block = block_cipher(block, key)
        xor_block = bytes(a ^ b for a, b in zip(dec_block, prev_block))
        plaintext += xor_block
        prev_block = block
    return plaintext

BLOCK_SIZE = 8

print("Enter Plaintext (ASCII):")
try:
    PLAINTEXT_STR = input()
    PLAINTEXT = PLAINTEXT_STR.encode('ascii')
except:
    print("Invalid input, using default plaintext.")
    PLAINTEXT = b'Default012'

print(f"Enter 8-byte ASCII Key (e.g., 'mysecret'):")
try:
    KEY_STR = input()
    KEY = KEY_STR.encode('ascii')[:BLOCK_SIZE]
except:
    KEY = b'mysecret'

print(f"Enter 8-byte ASCII IV (e.g., 'initvect'):")
try:
    IV_STR = input()
    IV = IV_STR.encode('ascii')[:BLOCK_SIZE]
except:
    IV = b'initvect'

PADDED_PLAINTEXT = pad_plaintext(PLAINTEXT, BLOCK_SIZE)
BLOCK_COUNT = len(PADDED_PLAINTEXT) // BLOCK_SIZE

print("\n--- Original CBC Execution ---")
CIPHERTEXT = cbc_encrypt(PADDED_PLAINTEXT, IV, KEY)
DECRYPTED = cbc_decrypt(CIPHERTEXT, IV, KEY)
DECRYPTED_UNPAD = unpad_plaintext(DECRYPTED)

print(f"Plaintext (PT): {PLAINTEXT!r}")
print(f"Padded PT: {PADDED_PLAINTEXT!r} ({BLOCK_COUNT} blocks)")
print(f"Key: {KEY!r}, IV: {IV!r}")
print(f"Ciphertext (CT): {CIPHERTEXT!r}")
print(f"Decrypted PT: {DECRYPTED_UNPAD!r}")


print("\n--- a. Error in Transmitted Ciphertext (C1) ---")
# C1 is the first block of the ciphertext (indices 0 to BLOCK_SIZE-1)
C1_ERROR = bytearray(CIPHERTEXT)
if len(C1_ERROR) >= BLOCK_SIZE:
    C1_ERROR[0] ^= 0x01 # Toggle one bit in C1
    
    DECRYPTED_C_ERROR = cbc_decrypt(bytes(C1_ERROR), IV, KEY)
    DECRYPTED_C_ERROR_UNPAD = unpad_plaintext(DECRYPTED_C_ERROR)
    
    print(f"Corrupted CT: {bytes(C1_ERROR)!r}")
    print(f"Decrypted PT (Unpadded): {DECRYPTED_C_ERROR_UNPAD!r}")
    print("ANALYSIS: Error in C_i (first block) causes corruption in P_i and P_{i+1}.")
else:
    print("Ciphertext is too short to demonstrate C1 error.")


print("\n--- b. Error in Source Plaintext (P1) ---")
# P1 is the first block of the PADDED plaintext
P1_ERROR = bytearray(PADDED_PLAINTEXT)
if len(P1_ERROR) >= BLOCK_SIZE:
    P1_ERROR[0] ^= 0x01 # Toggle one bit in P1
    
    CIPHERTEXT_P_ERROR = cbc_encrypt(bytes(P1_ERROR), IV, KEY)
    DECRYPTED_P_ERROR = cbc_decrypt(CIPHERTEXT_P_ERROR, IV, KEY)
    DECRYPTED_P_ERROR_UNPAD = unpad_plaintext(DECRYPTED_P_ERROR)
    
    print(f"Corrupted Padded PT: {bytes(P1_ERROR)!r}")
    print(f"Corrupted CT: {CIPHERTEXT_P_ERROR!r}")
    print(f"Decrypted PT (Unpadded): {DECRYPTED_P_ERROR_UNPAD!r}")
    print("ANALYSIS: Error in P_i (first block) causes corruption in P_i, but P_{i+1}, P_{i+2}, etc. are corrected.")
else:
    print("Padded plaintext is too short to demonstrate P1 error.")
