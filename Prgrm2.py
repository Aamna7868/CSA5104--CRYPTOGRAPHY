import string, random

def monoalphabetic_cipher(text):
    letters = string.ascii_uppercase
    cipher = list(letters)
    random.shuffle(cipher)
    table = str.maketrans(letters, ''.join(cipher))
    return text.upper().translate(table)

text = input("Enter the text: ")
encrypted = monoalphabetic_cipher(text)
print("\nOriginal Text : ", text)
print("Encrypted Text: ", encrypted)

