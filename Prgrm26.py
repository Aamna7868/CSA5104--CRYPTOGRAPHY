def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_phi(e, d, n):
    k = e * d - 1
    i = n - 1
    while i > n * 0.8:
        if k % i == 0:
            return i
        i -= 1
    return None

def factor_from_phi(n, phi_n):
    s = n - phi_n + 1
    delta = s * s - 4 * n
    sqrt_delta = int(delta**0.5)
    p = (s + sqrt_delta) // 2
    q = (s - sqrt_delta) // 2
    return p, q

def main():
    n_modulus = 3599
    e_public = 31
    d_leaked = 3031

    print("RSA Safety Check: Modulus Reuse After Key Leak")
    print("---------------------------------------------")
    print(f"Known Modulus N: {n_modulus}")
    print(f"Leaked Public Key e: {e_public}")
    print(f"Leaked Private Key d: {d_leaked}")
    
    phi_n = find_phi(e_public, d_leaked, n_modulus)
    
    print("\n--- Attacker's Discovery ---")
    print(f"Attacker calculates Phi(N): {phi_n}")
    
    p, q = factor_from_phi(n_modulus, phi_n)
    
    print(f"Attacker factors N: p={p}, q={q}")
    
    print("\n--- Security Conclusion ---")
    print("Is it safe to generate new keys (e', d') with the same N?")
    
    if p * q == n_modulus:
        print("Answer: NO. The entire system is compromised.")
        print("Because the attacker knows N and Phi(N), they can instantly factor N.")
        print("This means they can calculate the new private key d' for any new public key e' Bob chooses.")

if __name__ == "__main__":
    main()
