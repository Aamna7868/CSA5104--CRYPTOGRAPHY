import math

def main():
    KNOWN_ENGLISH_FREQS = [
        0.0817, 0.0149, 0.0278, 0.0425, 0.1270, 0.0223, 0.0202, 0.0609, 
        0.0697, 0.0015, 0.0077, 0.0403, 0.0241, 0.0675, 0.0751, 0.0193, 
        0.0010, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 
        0.0197, 0.0007
    ]
    
    CIPHERTEXT = "YJQQO RZ JSIJNSXJ SIJSIJNSXJ RZ YJQQO JSIJNSXJ"
    
    total_letters = sum(1 for char in CIPHERTEXT.upper() if 'A' <= char <= 'Z')

    candidate_results = []
    
    for key_shift in range(26):
        plaintext = ""
        observed_counts = [0] * 26
        
        for char in CIPHERTEXT.upper():
            if 'A' <= char <= 'Z':
                original_index = ord(char) - ord('A')
                decrypted_index = (original_index - key_shift + 26) % 26
                p_char = chr(decrypted_index + ord('A'))
                plaintext += p_char
                observed_counts[decrypted_index] += 1
            else:
                plaintext += char

        chi_square = 0.0
        for i in range(26):
            expected_count = KNOWN_ENGLISH_FREQS[i] * total_letters
            observed_count = observed_counts[i]
            if expected_count > 0:
                chi_square += (observed_count - expected_count) ** 2 / expected_count
        
        candidate_results.append((chi_square, plaintext, key_shift))
    
    candidate_results.sort(key=lambda x: x[0])
    
    top_n = 10
    
    print("CIPHERTEXT:", CIPHERTEXT)
    print("TOP", min(top_n, len(candidate_results)), "POSSIBLE PLAINTEXTS:")
    
    for i in range(min(top_n, len(candidate_results))):
        score, plaintext, key = candidate_results[i]
        
        print(f"--- CANDIDATE {i + 1} ---")
        print("KEY (Shift):", key)
        print("SCORE (Chi^2):", score)
        print("PLAINTEXT:", plaintext)

if __name__ == "__main__":
    main()
