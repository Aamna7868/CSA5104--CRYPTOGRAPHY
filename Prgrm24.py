def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def factor_n(n):
    i = 2
    limit = int(n**0.5)
    while i <= limit:
        if n % i == 0:
            return i, n // i
        i += 1
    return n, 1

def main():
    e = 31
    n = 3599
    
    p, q = factor_n(n)
    
    phi_n = (p - 1) * (q - 1)
    
    d = modinv(e, phi_n)
    
    print("RSA Key Calculation")
    print("-------------------")
    print(f"Modulus n: {n}")
    print(f"Public Exponent e: {e}")
    print(f"Prime p: {p}")
    print(f"Prime q: {q}")
    print(f"Phi(n): {phi_n}")
    print(f"Private Key d: {d}")

if __name__ == "__main__":
    main()
