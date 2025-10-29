def encrypt(plaintext, key):
    ciphertext = ""
    for i, ch in enumerate(plaintext.upper()):
        if ch.isalpha():
            shift = key[i]
            c = (ord(ch) - 65 + shift) % 26
            ciphertext += chr(c + 65)
        else:
            ciphertext += ch
    return ciphertext

def decrypt(ciphertext, key):
    plaintext = ""
    for i, ch in enumerate(ciphertext.upper()):
        if ch.isalpha():
            shift = key[i]
            p = (ord(ch) - 65 - shift) % 26
            plaintext += chr(p + 65)
        else:
            plaintext += ch
    return plaintext

plaintext = input("Enter plaintext: ").replace(" ", "")
key = list(map(int, input("Enter key stream (space separated numbers): ").split()))

ciphertext = encrypt(plaintext, key)
decrypted = decrypt(ciphertext, key)

print("\nCiphertext:", ciphertext)
print("Decrypted Text:", decrypted)
