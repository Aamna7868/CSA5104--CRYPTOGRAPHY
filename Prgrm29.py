def rho(a):
    rho_offsets = [
        [0, 36, 3, 41, 18],
        [1, 44, 10, 45, 2],
        [62, 6, 25, 8, 20],
        [28, 27, 0, 55, 14],
        [39, 43, 15, 21, 1]
    ]
    return [[(a[y][x] << rho_offsets[y][x]) & (2**64 - 1) | (a[y][x] >> (64 - rho_offsets[y][x])) for x in range(5)] for y in range(5)]

def pi(a):
    b = [[0] * 5 for _ in range(5)]
    for y in range(5):
        for x in range(5):
            b[y][x] = a[x][(x + 3 * y) % 5]
    return b

def chi(a):
    b = [[0] * 5 for _ in range(5)]
    for y in range(5):
        for x in range(5):
            b[y][x] = a[y][x] ^ (~a[y][(x + 1) % 5] & a[y][(x + 2) % 5])
    return b

def theta(a):
    c = [0] * 5
    for x in range(5):
        c[x] = a[0][x] ^ a[1][x] ^ a[2][x] ^ a[3][x] ^ a[4][x]
    
    d = [0] * 5
    for x in range(5):
        d[x] = c[(x - 1) % 5] ^ ((c[(x + 1) % 5] << 1) & (2**64 - 1) | (c[(x + 1) % 5] >> 63))
    
    b = [[0] * 5 for _ in range(5)]
    for y in range(5):
        for x in range(5):
            b[y][x] = a[y][x] ^ d[x]
    return b

def main():
    rate_lanes = 16
    capacity_lanes = 9
    
    state = [[0] * 5 for _ in range(5)]
    
    rate_lane_indices = [(x, y) for y in range(5) for x in range(5)][:rate_lanes]
    capacity_lane_indices = [(x, y) for y in range(5) for x in range(5)][rate_lanes:]
    
    for x, y in rate_lane_indices:
        state[y][x] = 1 

    print("SHA-3 Diffusion to Capacity Lanes Simulation")
    print("------------------------------------------")
    print(f"Initial nonzero rate lanes: {rate_lanes}")
    print(f"Initial zero capacity lanes: {capacity_lanes}")
    print(f"Target: Find rounds (ignore permutation) until all 9 capacity lanes have nonzero bits.")
    
    rounds = 0
    while True:
        rounds += 1
        
        state = theta(state)
        
        nonzero_capacity_lanes = 0
        for x, y in capacity_lane_indices:
            if state[y][x] != 0:
                nonzero_capacity_lanes += 1
        
        if nonzero_capacity_lanes == capacity_lanes:
            print("\nResult: All capacity lanes have at least one nonzero bit.")
            print(f"Time to full diffusion: {rounds} round(s)")
            break
        
        state = chi(state)
        state = pi(state)
        state = rho(state)

if __name__ == "__main__":
    main()
