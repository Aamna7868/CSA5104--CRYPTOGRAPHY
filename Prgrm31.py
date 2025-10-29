def left_shift_and_xor(l, block_size):
    if block_size == 64:
        r = 0x1B
        msb_mask = 1 << 63
    elif block_size == 128:
        r = 0x87
        msb_mask = 1 << 127
    else:
        return 0
    
    msb_set = (l & msb_mask) != 0
    l_shifted = (l << 1) & (msb_mask * 2 - 1)
    
    if msb_set:
        return l_shifted ^ r
    else:
        return l_shifted

def main():
    l_64_msb_clear = 0x0000000000000001
    l_64_msb_set = 0x8000000000000001
    l_128_msb_clear = 0x00000000000000000000000000000001
    l_128_msb_set = 0x80000000000000000000000000000001

    k1_64_c = left_shift_and_xor(l_64_msb_clear, 64)
    k2_64_c = left_shift_and_xor(k1_64_c, 64)
    
    k1_64_s = left_shift_and_xor(l_64_msb_set, 64)
    k2_64_s = left_shift_and_xor(k1_64_s, 64)

    k1_128_c = left_shift_and_xor(l_128_msb_clear, 128)
    k2_128_c = left_shift_and_xor(k1_128_c, 128)
    
    k1_128_s = left_shift_and_xor(l_128_msb_set, 128)
    k2_128_s = left_shift_and_xor(k1_128_s, 128)
    
    print("CMAC Subkey Generation Demo")
    print("---------------------------")

    print("64-bit Block Size (R=0x1B)")
    print("L (MSB clear):", hex(l_64_msb_clear))
    print("K1:", hex(k1_64_c))
    print("K2:", hex(k2_64_c))

    print("\nL (MSB set):", hex(l_64_msb_set))
    print("K1:", hex(k1_64_s))
    print("K2:", hex(k2_64_s))
    
    print("\n128-bit Block Size (R=0x87)")
    print("L (MSB clear):", hex(l_128_msb_clear))
    print("K1:", hex(k1_128_c))
    print("K2:", hex(k2_128_c))

    print("\nL (MSB set):", hex(l_128_msb_set))
    print("K1:", hex(k1_128_s))
    print("K2:", hex(k2_128_s))

if __name__ == "__main__":
    main()
