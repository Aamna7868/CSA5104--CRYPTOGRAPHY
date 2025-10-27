def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x

def affine_decrypt(cipher, a, b):
    a_inv = mod_inverse(a, 26)
    return ''.join(chr(((a_inv * ((ord(ch) - 65) - b)) % 26) + 65) for ch in cipher.upper() if ch.isalpha())


cipher = input("Enter ciphertext: ").upper()
a, b = 5, 25
plain = affine_decrypt(cipher, a, b)
print("Decrypted text:", plain)
