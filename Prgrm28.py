def pow_mod(base, exponent, modulus):
    return pow(base, exponent, modulus)

def main():
    q = 23
    a = 5
    public_flaw_a = 3
    
    xA = 6
    xB = 15

    print("Diffie-Hellman Protocol Security Analysis")
    print("----------------------------------------")
    print(f"Public Prime (q): {q}")
    print(f"Public Generator (a): {a}")
    
    print("\nPart 1: Flawed Exchange (x^a mod q)")
    print(f"Alice's secret xA: {xA}")
    print(f"Bob's secret xB: {xB}")
    print(f"Public exponent a (flawed): {public_flaw_a}")
    
    YA_flawed = pow_mod(xA, public_flaw_a, q)
    YB_flawed = pow_mod(xB, public_flaw_a, q)
    
    print(f"Alice sends YA = xA^a mod q: {YA_flawed}")
    print(f"Bob sends YB = xB^a mod q: {YB_flawed}")
    
    print("\n--- Security of Flawed Exchange ---")
    print("Problem: This is INSECURE.")
    print("Attack Method: Finding the secret x is trivial.")
    print(f"Since x is usually a small integer (0 to {q-1}), an attacker (Eve) can find xA by simply checking:")
    
    found_xA = None
    for x_guess in range(1, q):
        if pow_mod(x_guess, public_flaw_a, q) == YA_flawed:
            found_xA = x_guess
            break
            
    print(f"Eve finds Alice's secret xA: {found_xA}")
    print("This is a simple root-finding problem, not the hard Discrete Logarithm Problem.")
    
    print("\nPart 2: Correct Diffie-Hellman Exchange (a^x mod q)")
    print("Method: Alice and Bob agree on a shared secret key K.")
    
    
    YA_secure = pow_mod(a, xA, q)
    YB_secure = pow_mod(a, xB, q)
    
    print(f"Alice sends YA = a^xA mod q: {YA_secure}")
    print(f"Bob sends YB = a^xB mod q: {YB_secure}")
    
    K_Alice = pow_mod(YB_secure, xA, q)
    K_Bob = pow_mod(YA_secure, xB, q)
    
    print(f"Alice computes K = YB^xA mod q: {K_Alice}")
    print(f"Bob computes K = YA^xB mod q: {K_Bob}")
    print(f"Shared Key Agreement: {K_Alice == K_Bob}")
    
    print("\n--- Security of Diffie-Hellman ---")
    
    print("Can Eve break the system without finding the secret numbers?")
    print("Yes. Without authentication, Eve can perform a Man-in-the-Middle (MITM) attack.")
    print("Eve pretends to be Bob to Alice, and Alice to Bob, establishing two separate keys.")
    
    print("\nCan Eve find the secret numbers?")
    print("No (Infeasible). Finding xA from YA, a, and q requires solving the Discrete Logarithm Problem (DLP).")
    print("This is computationally infeasible for sufficiently large prime q.")

if __name__ == "__main__":
    main()
