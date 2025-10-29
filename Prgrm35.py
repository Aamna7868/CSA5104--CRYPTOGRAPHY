import random
import string

def encrypt_otp(plaintext, key_stream):
    ciphertext = ""
    for p, k in zip(plaintext.upper(), key_stream):
        if 'A' <= p <= 'Z':
            p_val = ord(p) - ord('A')
            c_val = (p_val + k) % 26
            ciphertext += chr(c_val + ord('A'))
        else:
            ciphertext += p
    return ciphertext

def decrypt_otp(ciphertext, key_stream):
    plaintext = ""
    for c, k in zip(ciphertext.upper(), key_stream):
        if 'A' <= c <= 'Z':
            c_val = ord(c) - ord('A')
            p_val = (c_val - k) % 26
            plaintext += chr(p_val + ord('A'))
        else:
            plaintext += c
    return plaintext

def main():
    PLAINTEXT = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    KEY_LENGTH = len(PLAINTEXT)
    
    random.seed(42)
    KEY_STREAM = [random.randint(0, 25) for _ in range(KEY_LENGTH)]

    CIPHERTEXT = encrypt_otp(PLAINTEXT, KEY_STREAM)
    DECRYPTED_TEXT = decrypt_otp(CIPHERTEXT, KEY_STREAM)

    print("PLAINTEXT:", PLAINTEXT)
    print("KEY_STREAM_SAMPLE:", KEY_STREAM[:10])
    print("CIPHERTEXT:", CIPHERTEXT)
    print("DECRYPTED_TEXT:", DECRYPTED_TEXT)
    print("VERIFICATION:", PLAINTEXT == DECRYPTED_TEXT)

if __name__ == "__main__":
    main()
