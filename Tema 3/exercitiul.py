import random
import math
import numpy as np

epsilon = 10 ** (-5)


def calculate_vector(A, n, s):
    b = np.zeros(n)
    for i in range(n):
        sum = 0
        for j in range(n):
            sum = sum + A[i][j] * s[j]
        b[i] = sum
    return b


def generate_matrix(n):
    return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]


def generate_vector_s(n):
    return [random.randint(-10, 10) for _ in range(n)]


def QR(A, n, b):
    Q = np.identity(n)
    for r in range(n-1):
        u = np.zeros(n)
        s = 0
        for i in range(r, n):
            s += A[i][r] ** 2
        if s < epsilon:
            continue
        k = math.sqrt(s)
        if A[r][r] > 0:
            k = -k
        beta = s - k * A[r][r]
        u[r] = A[r][r] - k
        for i in range(r+1, n):
            u[i] = A[i][r]
        for j in range(r, n):
            s = 0
            for i in range(r, n):
                s += u[i] * A[i][j]
            gamma = s / beta
            for i in range(r, n):
                A[i][j] -= gamma * u[i]
        for i in range(r+1, n):
            A[i][r] = 0
        for i in range(r, n):
            s = 0
            for j in range(r, n):
                s += Q[i][j] * u[j]
            gamma = s / beta
            for j in range(r, n):
                Q[i][j] -= gamma * u[j]
        for i in range(r, n):
            s = 0
            for j in range(n):
                s += b[j] * u[j]
            gamma = s / beta
            b[i] -= gamma * u[i]

    R = A
    return Q, R, b


def print_matrix(A):
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end=" ")
        print()


def calculate_norm(x_house, x_lib):
    return np.linalg.norm(x_house - x_lib)


def solve_system(R, n, b):
    x = np.zeros(n)
    x[n-1] = b[n-1] / R[n-1][n-1]
    for i in range(n-2, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= R[i][j] * x[j]
        x[i] /= R[i][i]
    return x


def find_x_qr_with_lib(A, n, b):
    Q, R = np.linalg.qr(A)
    x = solve_system(R, n, b)
    return x



def main():
    n = 3
    s = generate_vector_s(n)
    A = generate_matrix(n)
    A_init = np.copy(A)
    print("A:")
    print_matrix(A)
    print()
    print("s:", s)
    print()
    b = calculate_vector(A, n, s)
    print("b:", b)
    print("------------------")
    print()

    Q, R, b = QR(A, n, b)

    print("Q:")
    print_matrix(Q)
    print("R:")
    print_matrix(R)
    print("------------------")
    print()

    X_house = solve_system(R, n, b)
    x_QR = find_x_qr_with_lib(A_init, n, b)

    print("norma:", calculate_norm(x_QR, X_house))
    print("X_house:", X_house)
    print("x_QR:", x_QR)
    print()

if __name__ == "__main__":
    main()