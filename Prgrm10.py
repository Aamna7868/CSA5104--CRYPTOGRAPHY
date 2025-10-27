matrix = [
    ['M','F','H','I','K'],
    ['U','N','O','P','Q'],
    ['Z','V','W','X','Y'],
    ['E','L','A','R','G'],
    ['D','S','T','B','C']
]

def find_pos(ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch or (ch == 'J' and matrix[i][j] == 'I'):
                return i, j

def encrypt_playfair(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    if len(text) % 2 != 0: text += 'X'
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_pos(a)
        r2, c2 = find_pos(b)
        if r1 == r2:
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
    return result

msg = "MUST SEE YOU OVER CADOGAN WEST COMING AT ONCE"
print("Encrypted text:", encrypt_playfair(msg))
