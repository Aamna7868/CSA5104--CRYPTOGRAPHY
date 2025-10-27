import string

def playfair_matrix(key):
    key = ''.join(dict.fromkeys(key.upper().replace('J','I')))
    matrix = list(key) + [c for c in string.ascii_uppercase if c not in key and c!='J']
    return [matrix[i*5:(i+1)*5] for i in range(5)]

def playfair_cipher(text, key):
    m = playfair_matrix(key)
    text = text.upper().replace('J','I')
    if len(text)%2: text += 'X'
    res = ''
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1 = c1 = r2 = c2 = 0
        for r in range(5):
            if a in m[r]: r1, c1 = r, m[r].index(a)
            if b in m[r]: r2, c2 = r, m[r].index(b)
        if r1==r2: res += m[r1][(c1+1)%5] + m[r2][(c2+1)%5]
        elif c1==c2: res += m[(r1+1)%5][c1] + m[(r2+1)%5][c2]
        else: res += m[r1][c2] + m[r2][c1]
    return res

text = input("Enter the text: ")
key = input("Enter the key: ")
encrypted = playfair_cipher(text, key)
print("\nOriginal Text : ", text)
print("Encrypted Text: ", encrypted)
