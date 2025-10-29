import math
import string
import itertools

def main():
    ENGLISH_FREQS = {
        'E': 0.12702, 'T': 0.09056, 'A': 0.08167, 'O': 0.07507, 'I': 0.06966,
        'N': 0.06749, 'S': 0.06327, 'H': 0.06094, 'R': 0.05987, 'D': 0.04253,
        'L': 0.04025, 'C': 0.02782, 'U': 0.02758, 'M': 0.02406, 'W': 0.02360,
        'F': 0.02228, 'G': 0.02015, 'Y': 0.01974, 'P': 0.01929, 'B': 0.01492,
        'V': 0.00978, 'K': 0.00772, 'J': 0.00153, 'X': 0.00150, 'Q': 0.00095,
        'Z': 0.00074
    }
    
    CIPHERTEXT = "VKXW VSWZKW XJOWR ZYOVW KXQOXW KXFOWZKW ZYOVW KXQOXW KXFOWZKW ZYOVW KXQOXW KXFOWZKW"
    
    ct_counts = {}
    total_letters = 0
    
    for char in CIPHERTEXT.upper():
        if 'A' <= char <= 'Z':
            ct_counts[char] = ct_counts.get(char, 0) + 1
            total_letters += 1

    sorted_ct_chars = sorted(ct_counts, key=ct_counts.get, reverse=True)
    sorted_en_chars = sorted(ENGLISH_FREQS, key=ENGLISH_FREQS.get, reverse=True)
    
    base_key = {sorted_ct_chars[i]: sorted_en_chars[i] for i in range(len(sorted_ct_chars))}

    top_n = 10
    top_ct_chars = sorted_ct_chars[:5]
    top_en_chars = sorted_en_chars[:5]
    
    candidate_keys = []
    
    for p in itertools.permutations(top_en_chars):
        current_key = base_key.copy()
        
        for i in range(len(top_ct_chars)):
            current_key[top_ct_chars[i]] = p[i]
        
        candidate_keys.append(current_key)
        if len(candidate_keys) >= 200: break 

    scored_candidates = []
    
    for key_map in candidate_keys:
        plaintext_chars = []
        observed_pt_counts = {c: 0 for c in string.ascii_uppercase}
        
        for char in CIPHERTEXT.upper():
            if 'A' <= char <= 'Z':
                p_char = key_map.get(char, char)
                plaintext_chars.append(p_char)
                observed_pt_counts[p_char] += 1
            else:
                plaintext_chars.append(char)

        plaintext = "".join(plaintext_chars)
        chi_square = 0.0
        
        for char, expected_freq in ENGLISH_FREQS.items():
            expected_count = expected_freq * total_letters
            observed_count = observed_pt_counts[char]
            
            if expected_count > 0:
                chi_square += (observed_count - expected_count) ** 2 / expected_count
            elif observed_count > 0:
                 chi_square += observed_count * observed_count 

        scored_candidates.append((chi_square, plaintext))
    
    scored_candidates.sort(key=lambda x: x[0])
    
    print("CIPHERTEXT:", CIPHERTEXT)
    print("TOP", min(top_n, len(scored_candidates)), "POSSIBLE PLAINTEXTS:")
    
    for i in range(min(top_n, len(scored_candidates))):
        score, plaintext = scored_candidates[i]
        
        print(f"--- CANDIDATE {i + 1} ---")
        print("SCORE (Chi^2):", score)
        print("PLAINTEXT (Partial Key):", plaintext)

if __name__ == "__main__":
    main()
