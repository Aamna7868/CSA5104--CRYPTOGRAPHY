import string

def calculate_frequencies(text):
    freq = {}
    total_letters = 0
    for char in text.upper():
        if 'A' <= char <= 'Z':
            freq[char] = freq.get(char, 0) + 1
            total_letters += 1
    
    sorted_freq = {}
    for char, count in freq.items():
        sorted_freq[char] = count / total_letters if total_letters > 0 else 0
    
    return sorted_freq

def solve_cipher(ciphertext, known_freqs):
    ciphertext_freqs = calculate_frequencies(ciphertext)
    
    sorted_cipher_chars = sorted(ciphertext_freqs, key=ciphertext_freqs.get, reverse=True)
    sorted_known_chars = sorted(known_freqs, key=known_freqs.get, reverse=True)
    
    mapping = {}
    
    for c_char, p_char in zip(sorted_cipher_chars, sorted_known_chars):
        mapping[c_char] = p_char
    
    plaintext = ""
    for char in ciphertext.upper():
        if char in mapping:
            plaintext += mapping[char]
        else:
            plaintext += char
            
    return plaintext, mapping

def main():
    KNOWN_ENGLISH_FREQS = {
        'E': 0.1270, 'T': 0.0906, 'A': 0.0817, 'O': 0.0751, 'I': 0.0697,
        'N': 0.0675, 'S': 0.0633, 'H': 0.0609, 'R': 0.0599, 'D': 0.0425,
        'L': 0.0403, 'C': 0.0278, 'U': 0.0276, 'M': 0.0241, 'W': 0.0236,
        'F': 0.0223, 'G': 0.0202, 'Y': 0.0197, 'P': 0.0193, 'B': 0.0129,
        'V': 0.0098, 'K': 0.0077, 'J': 0.0015, 'X': 0.0015, 'Q': 0.0010,
        'Z': 0.0007
    }
    
    CIPHERTEXT = "QEB NFPZRY F YROOL F KRRB YROOL YROOL F YROOL KRRB YROOL"
    
    plaintext, mapping = solve_cipher(CIPHERTEXT, KNOWN_ENGLISH_FREQS)
    
    print("CIPHERTEXT:", CIPHERTEXT)
    print("--- MOST LIKELY PLAINTEXT ---")
    print("PLAINTEXT:", plaintext)
    print("MAPPING:", mapping)

if __name__ == "__main__":
    main()
