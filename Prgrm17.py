
def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

def str_to_bin(s):
    return ''.join(format(ord(i), '08b') for i in s)

def bin_to_str(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

def xor(a, b):
    return ''.join('0' if i == j else '1' for i, j in zip(a, b))

def encrypt(text, key):
    text = pad(text)
    key_bin = str_to_bin(key)
    text_bin = str_to_bin(text)
    key_bin = key_bin[:len(text_bin)]
    return bin_to_str(xor(text_bin, key_bin))

def decrypt(cipher, key):
    key_bin = str_to_bin(key)
    cipher_bin = str_to_bin(cipher)
    key_bin = key_bin[:len(cipher_bin)]
    return bin_to_str(xor(cipher_bin, key_bin)).strip()

plaintext = input("Enter plaintext: ")
key = input("Enter key (8 characters): ")

if len(key) != 8:
    print("Key must be 8 characters long.")
else:
    cipher = encrypt(plaintext, key)
    print("\nEncrypted text:", cipher)
    decrypted = decrypt(cipher, key)
    print("Decrypted text:", decrypted)
