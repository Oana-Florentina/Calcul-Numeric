import random
import math
import numpy as np

epsilon = 1e-5


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


def solve_system2(R, b):
    return np.linalg.solve(R, b)


def find_x_qr_with_lib(A, n, b):
    Q, R = np.linalg.qr(A)
    x = solve_system(R, n, np.dot(Q.T, b))
    return x


def calculate_second_norm(A_init, X_house, b_init):
    print("b_init:", b_init)
    print("A_init:", A_init)
    print("X_house:", X_house)
    A_init_x_house = np.dot(A_init, X_house)
    print("A_init_x_house:", A_init_x_house)

    norm = np.linalg.norm(A_init_x_house - b_init)
    print("Norm between A_init*X_house and b_init:", norm)
    print("------------------")


def qr_decomposition(A):
    Q, R = np.linalg.qr(A)
    return Q, R


def main():
    n = 3
    s = [3, 2, 1]
    A = [[0, 0, 4], [1, 2, 3], [0, 1, 2]]
   # s = generate_vector_s(n)
   # A = generate_matrix(n)
    A_init = np.copy(A)
    A_init = np.array(A_init, dtype=np.float32)
    print("A:")
    print_matrix(A)
    print()
    print("s:", s)
    print()
    b = calculate_vector(A, n, s)
    b_init = np.copy(b)
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
    # Q, R = qr_decomposition(A_init)
    print("Q:")
    print_matrix(Q)
    print("R:")
    print_matrix(R)
    print("------------------")

    X_house = solve_system(R, n, np.dot(Q.T, b_init))

    x_QR = find_x_qr_with_lib(A_init, n, b_init)

    print("norma:", calculate_norm(x_QR, X_house))
    print("X_house:", X_house)
    print("s: ", s)
    print("x_QR:", x_QR)
    print()
    print("------------------")
    print()
    print("X_house:", X_house)

    calculate_second_norm(A_init, X_house, b_init)

    print("x_QR:", x_QR)
    print("A_init:", A_init)


if __name__ == "__main__":
    main()