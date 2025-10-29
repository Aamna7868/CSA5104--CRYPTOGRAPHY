import os
import struct

def encrypt_block(key, block):
    block_int = struct.unpack('>Q', block)[0]
    key_int = struct.unpack('>Q', key)[0]
    encrypted_int = block_int ^ key_int
    return struct.pack('>Q', encrypted_int)

def cbc_mac(key, message):
    block_size = 8
    num_blocks = len(message) // block_size
    
    chaining_value = b'\x00' * block_size
    
    for i in range(num_blocks):
        block = message[i * block_size : (i + 1) * block_size]
        xor_block = bytes(a ^ b for a, b in zip(block, chaining_value))
        chaining_value = encrypt_block(key, xor_block)
        
    return chaining_value

def main():
    block_size = 8
    
    key = b'SECRET-K'
    
    X = b'MESSAGE!'
    
    T = cbc_mac(key, X)
    
    X_xor_T = bytes(a ^ b for a, b in zip(X, T))
    
    X_prime = X + X_xor_T
    
    T_prime = cbc_mac(key, X_prime)
    
    print("CBC-MAC Forgery Attack Demonstration")
    print("-----------------------------------")
    print("Initial Message X:")
    print(X)
    print("MAC T for X:")
    print(T.hex())
    
    print("\nAdversary constructs forged message X':")
    print("X' = X || (X XOR T)")
    print("Forged Message X':")
    print(X_prime)
    
    print("\nMAC T' for forged message X':")
    print(T_prime.hex())
    
    print("\nCheck Forgery (T == T'):")
    print(T == T_prime)

if __name__ == "__main__":
    main()
