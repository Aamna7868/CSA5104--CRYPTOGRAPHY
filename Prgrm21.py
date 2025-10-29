def block_cipher(block, key):
    res = bytearray(block)
    for i in range(len(res)):
        res[i] ^= key[i % len(key)]
    return bytes(res)

def iso_pad_plaintext(data, block_size):
    remaining = block_size - (len(data) % block_size)
    padding_len = remaining if remaining != 0 else block_size
    padding = bytearray([0x80])
    padding.extend(bytes([0x00] * (padding_len - 1)))
    return data + bytes(padding)

def iso_unpad_plaintext(padded_data):
    i = len(padded_data) - 1
    while i >= 0 and padded_data[i] == 0x00:
        i -= 1
    if i >= 0 and padded_data[i] == 0x80:
        return padded_data[:i]
    return padded_data

# --- ECB Mode ---
def ecb_encrypt(plaintext, key, iv=None):
    block_size = len(key) 
    ciphertext = b''
    for i in range(0, len(plaintext), block_size):
        ciphertext += block_cipher(plaintext[i:i + block_size], key)
    return ciphertext

def ecb_decrypt(ciphertext, key, iv=None):
    block_size = len(key)
    plaintext = b''
    for i in range(0, len(ciphertext), block_size):
        plaintext += block_cipher(ciphertext[i:i + block_size], key)
    return plaintext

# --- CBC Mode ---
def cbc_encrypt(plaintext, key, iv):
    block_size = len(iv)
    ciphertext = b''
    prev_block = iv
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        xor_input = bytes(a ^ b for a, b in zip(block, prev_block))
        cipher_block = block_cipher(xor_input, key)
        ciphertext += cipher_block
        prev_block = cipher_block
    return ciphertext

def cbc_decrypt(ciphertext, key, iv):
    block_size = len(iv)
    plaintext = b''
    prev_block = iv
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        dec_block = block_cipher(block, key)
        plaintext += bytes(a ^ b for a, b in zip(dec_block, prev_block))
        prev_block = block
    return plaintext

# --- CFB Mode ---
def cfb_encrypt(plaintext, key, iv):
    block_size = len(iv)
    ciphertext = b''
    prev_block = iv
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        keystream = block_cipher(prev_block, key)
        cipher_block = bytes(a ^ b for a, b in zip(block, keystream))
        ciphertext += cipher_block
        prev_block = cipher_block
    return ciphertext

def cfb_decrypt(ciphertext, key, iv):
    block_size = len(iv)
    plaintext = b''
    prev_block = iv
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        keystream = block_cipher(prev_block, key)
        plaintext += bytes(a ^ b for a, b in zip(block, keystream))
        prev_block = block
    return plaintext

# --- Main Execution (Consolidated) ---
BLOCK_SIZE = 8
KEY_SIZE = BLOCK_SIZE
IV_SIZE = BLOCK_SIZE

# Simplified Input and Default Fallbacks
PLAINTEXT = input("Enter Plaintext (ASCII):").encode('ascii') or b'Default short message.'
KEY = input(f"Enter {KEY_SIZE}-byte ASCII Key (default: 'A8chars!'):").encode('ascii').ljust(KEY_SIZE, b' ') or b'A8chars!'
IV = input(f"Enter {IV_SIZE}-byte ASCII IV (default: '01234567'):").encode('ascii').ljust(IV_SIZE, b' ') or b'01234567'

PADDED_PLAINTEXT = iso_pad_plaintext(PLAINTEXT, BLOCK_SIZE)

MODES = {
    "ECB": (ecb_encrypt, ecb_decrypt),
    "CBC": (cbc_encrypt, cbc_decrypt),
    "CFB": (cfb_encrypt, cfb_decrypt)
}

print("\n--- Encryption/Decryption Summary ---")
print(f"Key: {KEY!r}, IV: {IV!r}")
print(f"Padded PT: {PADDED_PLAINTEXT!r}")

for name, (enc_func, dec_func) in MODES.items():
    # CBC and CFB require IV, ECB uses it as an optional parameter (iv=None)
    CT = enc_func(PADDED_PLAINTEXT, KEY, IV if name != "ECB" else None)
    PT = dec_func(CT, KEY, IV if name != "ECB" else None)
    UNPAD = iso_unpad_plaintext(PT)
    
    print(f"\n--- {name} Mode ---")
    print(f"CT: {CT!r}")
    print(f"Decrypted: {UNPAD!r}")
