def generate_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = ""
    for ch in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in matrix:
            matrix += ch
    return [list(matrix[i:i+5]) for i in range(0, 25, 5)]

def find_pos(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j

def decrypt_playfair(cipher, matrix):
    cipher = cipher.replace("J", "I").replace(" ", "")
    result = ""
    for i in range(0, len(cipher), 2):
        a, b = cipher[i], cipher[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)
        if r1 == r2:
            result += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
        elif c1 == c2:
            result += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
    return result

matrix = generate_matrix("MFHIJKUNOPQZVWX YELARGDSTBC".replace(" ", ""))
cipher = ("KXJEYUREBEZWEHEWRYTUHEYFSKREHEGOYFIWTTTUOLKSY"
          "CAJPOBOTEIZONTXBYBNTGONEYCUZWRGDSONSXBOUYWRHEBAAHYUSEDQ")
print("Decrypted text:", decrypt_playfair(cipher, matrix))
