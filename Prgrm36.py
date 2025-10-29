import math

def encrypt_affine(p_val, a, b):
    return (a * p_val + b) % 26

def main():
    a_valid = 5
    b_valid = 8

    p1_valid = 0
    c1_valid = encrypt_affine(p1_valid, a_valid, b_valid)

    p2_valid = 13
    c2_valid = encrypt_affine(p2_valid, a_valid, b_valid)

    print("--- VALID KEY (a=5) ---")
    print("GCD(5, 26):", math.gcd(a_valid, 26))
    print("P1:", p1_valid, "-> C1:", c1_valid)
    print("P2:", p2_valid, "-> C2:", c2_valid)
    print("C1 != C2:", c1_valid != c2_valid)

    a_invalid = 2
    b_invalid = 3

    p1_invalid = 0
    c1_invalid = encrypt_affine(p1_invalid, a_invalid, b_invalid)

    p2_invalid = 13
    c2_invalid = encrypt_affine(p2_invalid, a_invalid, b_invalid)
    
    p3_invalid = 1
    c3_invalid = encrypt_affine(p3_invalid, a_invalid, b_invalid)
    
    print("--- INVALID KEY (a=2) ---")
    print("GCD(2, 26):", math.gcd(a_invalid, 26))
    print("P1:", p1_invalid, "-> C1:", c1_invalid)
    print("P2:", p2_invalid, "-> C2:", c2_invalid)
    print("C1 == C2:", c1_invalid == c2_invalid)
    print("P3:", p3_invalid, "-> C3:", c3_invalid)

if __name__ == "__main__":
    main()
