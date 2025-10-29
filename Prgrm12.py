import re

def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def hill_cipher(text, K, decrypt=False):
    text = re.sub('[^a-z]', '', text.lower())
    if len(text) % 2: text += 'x'
    nums = [ord(c) - 97 for c in text]
    if decrypt:
        det = (K[0][0]*K[1][1] - K[0][1]*K[1][0]) % 26
        inv = modinv(det, 26)
        K = [[(inv*K[1][1])%26, (-inv*K[0][1])%26],
             [(-inv*K[1][0])%26, (inv*K[0][0])%26]]
    out = ''
    for i in range(0, len(nums), 2):
        v = [(K[0][0]*nums[i] + K[0][1]*nums[i+1]) % 26,
             (K[1][0]*nums[i] + K[1][1]*nums[i+1]) % 26]
        out += chr(v[0]+97) + chr(v[1]+97)
    return out

text = input("Enter message: ")
print("Enter 2x2 key matrix:")
a = int(input("a11: "))
b = int(input("a12: "))
c = int(input("a21: "))
d = int(input("a22: "))
K = [[a, b], [c, d]]

cipher = hill_cipher(text, K)
plain = hill_cipher(cipher, K, True)

print("\nEncrypted text:", cipher)
print("Decrypted text:", plain)
