import os

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def pad(data, block_size=8):
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    return data[:-data[-1]]

def simple_encrypt(block, key):
    return bytes([(b + key[i % len(key)]) % 256 for i, b in enumerate(block)])

def simple_decrypt(block, key):
    return bytes([(b - key[i % len(key)]) % 256 for i, b in enumerate(block)])

plaintext = input("Enter plaintext: ").encode()
key = input("Enter key (8 chars): ").encode()
if len(key) != 8:
    print("Key must be 8 bytes long!")
    exit()

iv = os.urandom(8)
print("Generated IV (hex):", iv.hex())

# CBC Encryption
data = pad(plaintext)
ciphertext = b''
prev = iv
for i in range(0, len(data), 8):
    block = data[i:i+8]
    enc = simple_encrypt(xor(block, prev), key)
    ciphertext += enc
    prev = enc

print("\nCiphertext (hex):", ciphertext.hex())

# CBC Decryption
decrypted = b''
prev = iv
for i in range(0, len(ciphertext), 8):
    block = ciphertext[i:i+8]
    dec = xor(simple_decrypt(block, key), prev)
    decrypted += dec
    prev = block

plaintext_out = unpad(decrypted)
print("Decrypted text:", plaintext_out.decode())
