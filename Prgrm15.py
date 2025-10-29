import re

def decrypt(ct, k):
    return ''.join(chr((ord(c)-65-k)%26+65) if c.isalpha() else c for c in ct.upper())

def score(t):
    freq = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    t = re.sub('[^A-Z]', '', t.upper())
    return sum(freq.index(c) if c in freq else 26 for c in t)

ct = input("Enter ciphertext: ")
n = int(input("How many top plaintexts to show? "))

res = []
for k in range(26):
    pt = decrypt(ct, k)
    res.append((score(pt), k, pt))

for s, k, pt in sorted(res, reverse=False)[:n]:
    print(f"\nShift={k} -> {pt}")
