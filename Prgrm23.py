# --- S-DES Constants (Permutations and S-Boxes) ---
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
BLOCK_SIZE = 8
KEY_SIZE = 10
CTR_SIZE = 8

# --- Helper Functions ---
def permute(in_arr, p_arr):
    return [in_arr[p - 1] for p in p_arr]

def left_shift(data, count):
    return data[count:] + data[:count]

def binary_xor(a, b):
    return [a[i] ^ b[i] for i in range(len(a))]

def str_to_bits(s):
    return [int(c) for c in s]

def bits_to_str(bits):
    return "".join(map(str, bits))

def increment_counter(counter):
    c = counter[:]
    for i in range(CTR_SIZE - 1, -1, -1):
        if c[i] == 0:
            c[i] = 1
            return c
        c[i] = 0
    return c

# --- S-DES Core Functions ---
def key_generation(key):
    p10_key = permute(key, P10)
    L, R = p10_key[:5], p10_key[5:]
    
    # K1
    L1, R1 = left_shift(L, 1), left_shift(R, 1)
    K1 = permute(L1 + R1, P8)
    
    # K2
    L2, R2 = left_shift(L1, 2), left_shift(R1, 2)
    K2 = permute(L2 + R2, P8)
    
    return K1, K2

def sbox_substitution(in_bits, sbox):
    row = in_bits[0] * 2 + in_bits[3]
    col = in_bits[1] * 2 + in_bits[2]
    val = sbox[row][col]
    return [val // 2, val % 2]

def f_function(r_in, subkey):
    xor_data = binary_xor(permute(r_in, EP), subkey)
    
    s0_out = sbox_substitution(xor_data[:4], S0)
    s1_out = sbox_substitution(xor_data[4:], S1)
    
    return permute(s0_out + s1_out, P4)

def sdes_encrypt_block(data_block, K1, K2):
    ip_data = permute(data_block, IP)
    L0, R0 = ip_data[:4], ip_data[4:]
    
    # --- Round 1: Calculate L1, R1 ---
    # R1 = L0 XOR F(R0, K1)
    R1 = binary_xor(L0, f_function(R0, K1))
    # L1 = R0 (Swap)
    L1 = R0
    
    # --- Round 2: Calculate L2, R2 (No final swap) ---
    # R2 = L1 XOR F(R1, K2)
    R2 = binary_xor(L1, f_function(R1, K2))
    # L2 = R1
    L2 = R1
    
    # Output is L2 || R2, followed by inverse initial permutation
    return permute(L2 + R2, IP_INV)

# --- S-DES CTR Mode (Encryption/Decryption) ---
def sdes_ctr_mode(data_bits, key_bits, counter_bits):
    data_len = len(data_bits)
    K1, K2 = key_generation(key_bits)
    current_counter = counter_bits[:]
    output_bits = []

    for i in range(0, data_len, BLOCK_SIZE):
        keystream_block = sdes_encrypt_block(current_counter, K1, K2)
        
        data_block = data_bits[i:i + BLOCK_SIZE]
        
        ciphertext_block = binary_xor(data_block, keystream_block)
        output_bits.extend(ciphertext_block)
        
        current_counter = increment_counter(current_counter)
        
    return output_bits

# --- Main Execution ---
def main():
    while True:
        try:
            input_key = input("Enter 10-bit binary Key (e.g., 0111111101): ")
            if not all(c in '01' for c in input_key) or len(input_key) != KEY_SIZE:
                print(f"Error: Key must be exactly {KEY_SIZE} binary bits.")
                continue
            
            input_ctr = input(f"Enter {CTR_SIZE}-bit binary Counter Start (e.g., 00000000): ")
            if not all(c in '01' for c in input_ctr) or len(input_ctr) != CTR_SIZE:
                print(f"Error: Counter must be exactly {CTR_SIZE} binary bits.")
                continue

            input_pt = input("Enter binary Plaintext (multiple of 8 bits, e.g., 000000010000001000000100): ")
            data_len = len(input_pt)
            if data_len % BLOCK_SIZE != 0 or data_len == 0:
                print(f"Error: Plaintext length must be a positive multiple of {BLOCK_SIZE} bits (currently {data_len}).")
                continue
            if not all(c in '01' for c in input_pt):
                print("Error: Plaintext must only contain '0' and '1'.")
                continue

            break
        except EOFError:
            print("\nExiting program.")
            return

    key_bits = str_to_bits(input_key)
    pt_bits = str_to_bits(input_pt)
    counter_bits = str_to_bits(input_ctr)
    
    data_len = len(input_pt)
    
    print("\n--- S-DES CTR Mode Execution ---")
    print(f"Key ({KEY_SIZE}-bit): {input_key}")
    print(f"Counter Start ({CTR_SIZE}-bit): {input_ctr}")
    print(f"Plaintext ({data_len}-bit): {input_pt}")

    # ENCRYPTION
    encrypted_bits = sdes_ctr_mode(pt_bits, key_bits, counter_bits)
    encrypted_bin = bits_to_str(encrypted_bits)

    print("\n--- Encryption Results ---")
    print(f"Calculated Ciphertext: {encrypted_bin}")
    
    # DECRYPTION (CTR decryption is identical to encryption)
    decrypted_bits = sdes_ctr_mode(encrypted_bits, key_bits, counter_bits)
    decrypted_bin = bits_to_str(decrypted_bits)

    print("\n--- Decryption Results ---")
    print(f"Decrypted Plaintext: {decrypted_bin}")
    
    verification = "SUCCESS" if decrypted_bin == input_pt else "FAILED"
    print(f"Decryption Verification: {verification}")

if __name__ == "__main__":
    main()
