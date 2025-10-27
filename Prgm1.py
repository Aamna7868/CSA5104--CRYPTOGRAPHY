def caesar_cipher(text, k):
    letters = "ABCDEFGHIJKLM." \
    "NOPQRSTUVWXYZ"
    result = ""
    for char in text.upper():
        if char in letters:
            result += letters[(letters.index(char)+k)%26]
        else:
            result += char
    return result

text = input("Enter the text: ")
k = int(input("Enter shift value (1-25): "))

if 1 <= k <= 25:
    encrypted = caesar_cipher(text, k)
    decrypted = caesar_cipher(text, 26 - k)
    print("\nOriginal Text : ", text)
    print("Encrypted Text: ", encrypted)
    print("Decrypted Text: ", decrypted)
else:
    print("Please enter a valid shift value between 1 and 25.")
