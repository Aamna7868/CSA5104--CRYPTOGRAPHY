def generate_cipher(keyword):
    keyword = ''.join(sorted(set(keyword.upper()), key=keyword.index))
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher = keyword + ''.join(ch for ch in letters if ch not in keyword)
    return dict(zip(letters, cipher))

def encrypt(text, keymap):
    return ''.join(keymap.get(ch, ch) for ch in text.upper())

text = input("Enter plaintext: ")
keymap = generate_cipher("CIPHER")
cipher = encrypt(text, keymap)
print("Encrypted text:", cipher)
