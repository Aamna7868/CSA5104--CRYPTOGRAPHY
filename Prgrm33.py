import struct

def feistel_function(right_half, subkey):
    return right_half ^ subkey

def encrypt_block(plaintext, key):
    L, R = plaintext >> 32, plaintext & 0xFFFFFFFF
    
    key_high = key >> 32
    key_low = key & 0xFFFFFFFF
    
    for i in range(16):
        subkey = (key_high + key_low) & 0xFFFFFFFF
        
        temp = R
        R = L ^ feistel_function(R, subkey)
        L = temp
    
    ciphertext = (R << 32) | L
    return ciphertext

def decrypt_block(ciphertext, key):
    L, R = ciphertext >> 32, ciphertext & 0xFFFFFFFF
    
    key_high = key >> 32
    key_low = key & 0xFFFFFFFF
    
    round_keys = []
    for i in range(16):
        subkey = (key_high + key_low) & 0xFFFFFFFF
        round_keys.append(subkey)
    
    for i in range(15, -1, -1):
        subkey = round_keys[i]
        
        temp = L
        L = R ^ feistel_function(L, subkey)
        R = temp

    plaintext = (R << 32) | L
    return plaintext

def bytes_to_int(data):
    return struct.unpack('>Q', data)[0]

def int_to_bytes(data):
    return struct.pack('>Q', data)

def main():
    plaintext_bytes = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'
    key_bytes = b'\x13\x34\x57\x79\x9B\xBC\xDF\xF1'
    
    plaintext_int = bytes_to_int(plaintext_bytes)
    key_int = bytes_to_int(key_bytes)

    ciphertext_int = encrypt_block(plaintext_int, key_int)
    decrypted_int = decrypt_block(ciphertext_int, key_int)

    ciphertext_bytes = int_to_bytes(ciphertext_int)
    decrypted_bytes = int_to_bytes(decrypted_int)

    print("PLAINTEXT:", plaintext_bytes.hex())
    print("CIPHERTEXT:", ciphertext_bytes.hex())
    print("DECRYPTED:", decrypted_bytes.hex())

if __name__ == "__main__":
    main()
