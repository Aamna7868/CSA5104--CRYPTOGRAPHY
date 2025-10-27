def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt(text, a, b):
    result = ""
    for char in text.upper():
        if char.isalpha():
            p = ord(char) - 65
            c = (a * p + b) % 26
            result += chr(c + 65)
        else:
            result += char
    return result

def decrypt(cipher, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "Decryption not possible (invalid 'a')."
    for char in cipher.upper():
        if char.isalpha():
            c = ord(char) - 65
            p = (a_inv * (c - b)) % 26
            result += chr(p + 65)
        else:
            result += char
    return result

text = input("Enter plaintext: ")
a = int(input("Enter value of a: "))
b = int(input("Enter value of b: "))

if gcd(a, 26) != 1:
    print("Invalid 'a' value! It must be coprime with 26.")
else:
    cipher = encrypt(text, a, b)
    plain = decrypt(cipher, a, b)
    print("\nEncrypted text:", cipher)
    print("Decrypted text:", plain)
