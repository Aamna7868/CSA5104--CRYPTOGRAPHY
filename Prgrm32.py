import random
import time

def modular_pow(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def rsa_sign(message, d, n):
    return modular_pow(message, d, n)

def dsa_sign_like(message, q):
    random.seed(time.time())
    k = 0
    while k == 0:
        k = random.randint(1, q - 1)
    return (k * message) % q

def main():
    n = 3599
    d = 1171
    q = 10007
    m = 1234
    
    rsa_sig1 = rsa_sign(m, d, n)
    rsa_sig2 = rsa_sign(m, d, n)

    print("RSA Signature Determinism")
    print("Message:", m)
    print("Signature 1:", rsa_sig1)
    print("Signature 2:", rsa_sig2)
    print("Signatures Match (RSA):", rsa_sig1 == rsa_sig2)

    dsa_sig1 = dsa_sign_like(m, q)
    dsa_sig2 = dsa_sign_like(m, q)

    print("\nDSA Signature Randomness")
    print("Message:", m)
    print("Signature 1:", dsa_sig1)
    print("Signature 2:", dsa_sig2)
    print("Signatures Match (DSA):", dsa_sig1 == dsa_sig2)

if __name__ == "__main__":
    main()
