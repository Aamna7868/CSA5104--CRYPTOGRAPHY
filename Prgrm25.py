 def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_prime_factors(n, factor):
    if n % factor == 0 and factor > 1:
        return factor, n // factor
    return None, None

def main():
    e = 31
    n = 3599
    
    m_sharing_factor = 61
    
    g = gcd(m_sharing_factor, n)

    print("RSA Common Factor Break Demonstration")
    print("-----------------------------------")
    print(f"Modulus N: {n}")
    print(f"Plaintext Block M: {m_sharing_factor}")
    print(f"Greatest Common Divisor G = gcd(M, N): {g}")

    if g > 1:
        p, q = find_prime_factors(n, g)
        
        print("\nCommon factor found (G > 1). RSA is broken.")
        print("This means the security relies on factoring, and a factor was found.")
        print(f"G = {g} is a prime factor of N.")
        print("Prime p:", p)
        print("Prime q:", q)
        print("The factors of N are instantly revealed.")
    else:
        print("\nNo common factor found (G = 1). RSA remains secure.")
        
if __name__ == "__main__":
    main()
