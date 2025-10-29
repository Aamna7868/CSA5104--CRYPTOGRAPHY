def find_d(e, phi_n):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    y2 = 0
    temp_phi = phi_n
    
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2 - temp1 * x1
        y = y2 - temp1 * y1
        
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    
    if temp_phi == 1:
        d = y2
        if d < 0:
            d += phi_n
    return d

def encrypt(m, e, n):
    return pow(m, e, n)

def main():
    p = 43
    q = 59
    n = p * q
    e = 13
    
    phi_n = (p - 1) * (q - 1)
    d = find_d(e, phi_n)
    
    plaintext_characters = [i for i in range(26)]
    
    codebook = {}
    
    print("RSA Character-by-Character Encryption is INSECURE")
    print("------------------------------------------------")
    print(f"Modulus N (p*q): {n}")
    print(f"Public Key e: {e}")
    
    print("\nStep 1: Attacker constructs the Codebook (Dictionary Attack)")
    print("The message space is only 26 characters (0-25).")
    
    for m in plaintext_characters:
        c = encrypt(m, e, n)
        codebook[c] = m
    
    print("\nGenerated Codebook (Ciphertext -> Plaintext Mapping):")
    print(codebook)
    
    encrypted_message = [2430, 240, 2715, 2430, 240, 1500, 240]
    
    print("\nStep 2: Attacker intercepts message (C):")
    print(encrypted_message)
    
    decrypted_message = []
    
    for c in encrypted_message:
        if c in codebook:
            decrypted_message.append(codebook[c])
        else:
            decrypted_message.append("?")
            
    print("\nStep 3: Attacker instantly decrypts the message (M):")
    print(decrypted_message)
    print("The encryption is broken without needing the private key 'd'.")
    print(f"The correct private key is d = {d}, but it was never needed.")

if __name__ == "__main__":
    main()
