#include <stdio.h>

int modInverse(int a, int m) {
    a = a % m;
    for (int x = 1; x < m; x++) {
        if ((a * x) % m == 1) {
            return x;
        }
    }
    return -1;
}

void matrix_mult(int A[2][2], int B[2][2], int R[2][2]) {
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            R[i][j] = 0;
            for (int k = 0; k < 2; k++) {
                R[i][j] = (R[i][j] + A[i][k] * B[k][j]) % 26;
            }
        }
    }
}

void matrix_inverse(int P[2][2], int P_inv[2][2]) {
    int det = P[0][0] * P[1][1] - P[0][1] * P[1][0];
    det = (det % 26 + 26) % 26;
    int det_inv = modInverse(det, 26);

    P_inv[0][0] = (P[1][1] * det_inv) % 26;
    P_inv[1][1] = (P[0][0] * det_inv) % 26;
    P_inv[0][1] = (-P[0][1] * det_inv % 26 + 26) % 26;
    P_inv[1][0] = (-P[1][0] * det_inv % 26 + 26) % 26;
}

int main() {
    int K[2][2] = {{9, 4}, {5, 7}};
    int P[2][2] = {{12, 11}, {0, 4}};
    int C[2][2] = {{0, 0}, {0, 0}};
    int P_inv[2][2] = {{0, 0}, {0, 0}};
    int K_rec[2][2] = {{0, 0}, {0, 0}};

    matrix_mult(K, P, C);

    matrix_inverse(P, P_inv);

    matrix_mult(C, P_inv, K_rec);

    printf("Original Key K:\n");
    printf("%d %d\n", K[0][0], K[0][1]);
    printf("%d %d\n", K[1][0], K[1][1]);
    
    printf("Recovered Key K_rec (Attack):\n");
    printf("%d %d\n", K_rec[0][0], K_rec[0][1]);
    printf("%d %d\n", K_rec[1][0], K_rec[1][1]);

    return 0;
}
