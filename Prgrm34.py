import struct

BLOCK_SIZE = 8
def cipher_encrypt(data, key):
    return data ^ key

def cipher_decrypt(data, key):
    return data ^ key

def pad_message(message):
    length = len(message)
    padding_len = BLOCK_SIZE - (length % BLOCK_SIZE)
    if length % BLOCK_SIZE == 0:
        padding_len = BLOCK_SIZE
    padding = b'\x80' + b'\x00' * (padding_len - 1)
    return message + padding

def unpad_message(padded_message):
    i = len(padded_message) - 1
    while i >= 0 and padded_message[i] == 0x00:
        i -= 1
    if i >= 0 and padded_message[i] == 0x80:
        return padded_message[:i]
    return padded_message

def bytes_to_int(data):
    return struct.unpack('>Q', data)[0]

def int_to_bytes(data):
    return struct.pack('>Q', data)

def encrypt_ecb(plaintext, key_int):
    padded_pt = pad_message(plaintext)
    ciphertext = b''
    for i in range(0, len(padded_pt), BLOCK_SIZE):
        block = padded_pt[i:i + BLOCK_SIZE]
        block_int = bytes_to_int(block)
        cipher_int = cipher_encrypt(block_int, key_int)
        ciphertext += int_to_bytes(cipher_int)
    return ciphertext

def decrypt_ecb(ciphertext, key_int):
    plaintext = b''
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        block_int = bytes_to_int(block)
        plain_int = cipher_decrypt(block_int, key_int)
        plaintext += int_to_bytes(plain_int)
    return unpad_message(plaintext)

def encrypt_cbc(plaintext, key_int, iv_int):
    padded_pt = pad_message(plaintext)
    ciphertext = b''
    prev_cipher_int = iv_int
    for i in range(0, len(padded_pt), BLOCK_SIZE):
        block = padded_pt[i:i + BLOCK_SIZE]
        block_int = bytes_to_int(block)
        xor_int = block_int ^ prev_cipher_int
        cipher_int = cipher_encrypt(xor_int, key_int)
        ciphertext += int_to_bytes(cipher_int)
        prev_cipher_int = cipher_int
    return ciphertext

def decrypt_cbc(ciphertext, key_int, iv_int):
    plaintext = b''
    prev_cipher_int = iv_int
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        block_int = bytes_to_int(block)
        decrypted_int = cipher_decrypt(block_int, key_int)
        plain_int = decrypted_int ^ prev_cipher_int
        plaintext += int_to_bytes(plain_int)
        prev_cipher_int = block_int
    return unpad_message(plaintext)

def encrypt_cfb(plaintext, key_int, iv_int):
    segment_size = BLOCK_SIZE
    ciphertext = b''
    shift_reg_int = iv_int
    for i in range(0, len(plaintext), segment_size):
        block = plaintext[i:i + segment_size]
        cipher_int = cipher_encrypt(shift_reg_int, key_int)
        block_int = bytes_to_int(block)
        output_int = cipher_int ^ block_int
        ciphertext += int_to_bytes(output_int)
        shift_reg_int = output_int
    return ciphertext

def decrypt_cfb(ciphertext, key_int, iv_int):
    segment_size = BLOCK_SIZE
    plaintext = b''
    shift_reg_int = iv_int
    for i in range(0, len(ciphertext), segment_size):
        block = ciphertext[i:i + segment_size]
        cipher_int = cipher_encrypt(shift_reg_int, key_int)
        block_int = bytes_to_int(block)
        output_int = cipher_int ^ block_int
        plaintext += int_to_bytes(output_int)
        shift_reg_int = block_int
    return plaintext

def main():
    KEY = b'ABCDEFGH'
    IV = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    PLAINTEXT = b'Short message for cipher modes.'
    
    KEY_INT = bytes_to_int(KEY)
    IV_INT = bytes_to_int(IV)

    print("MODE: ECB")
    ecb_cipher = encrypt_ecb(PLAINTEXT, KEY_INT)
    ecb_plain = decrypt_ecb(ecb_cipher, KEY_INT)
    print("PT:", PLAINTEXT.hex())
    print("CT:", ecb_cipher.hex())
    print("DT:", ecb_plain.hex())

    print("MODE: CBC")
    cbc_cipher = encrypt_cbc(PLAINTEXT, KEY_INT, IV_INT)
    cbc_plain = decrypt_cbc(cbc_cipher, KEY_INT, IV_INT)
    print("PT:", PLAINTEXT.hex())
    print("CT:", cbc_cipher.hex())
    print("DT:", cbc_plain.hex())

    print("MODE: CFB")
    cfb_cipher = encrypt_cfb(PLAINTEXT, KEY_INT, IV_INT)
    cfb_plain = decrypt_cfb(cfb_cipher, KEY_INT, IV_INT)
    print("PT:", PLAINTEXT.hex())
    print("CT:", cfb_cipher.hex())
    print("DT:", cfb_plain.hex())

if __name__ == "__main__":
    main()
