import random
import math
import numpy as np

epsilon = 10 ** (-5)


def calculate_vector(A, n, s):
    b = 0
    for j in range(1, n):
        for i in range(1, n):
            b += A[i][j] * s[j]
    return b
def generate_matrix(n):
    return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]

def generate_vector_s(n):
    return [random.randint(-10, 10) for _ in range(n)]

def QR(A, n, b):
    Q = np.identity(len(A))
    u = np.zeros(n)
    s=0
    for r in range (1, n-1):
        for i in range (1, n):
            s = s + A[i][r] ** 2
        if s < epsilon:
            break;
        k = math.sqrt(s)
        if A[r][r] > 0:
            k = -k
        beta = s - k * A[r][r]
        u[r] = A[r][r] - k
        for i in range (r+1, n):
            u[i] = A[i][r]
        for j in range (r+1, n):
            s = 0
            for i in range (r, n):
                s = s + u[i] * A[i][j]
            gamma = s / beta
            for i in range (r, n):
                A[i][j] = A[i][j] - gamma * u[i]
        A[r][r] = k
        for i in range (r+1, n):
            A[i][r] = 0
        for i in range (r, n):
            s = 0
            for j in range (r, n):
                s = s + b[i] * u[i]
            gamma = s / beta
        for i in range ( r, n):
            b[i] = b[i] - gamma * u[i]
        for j in range (1, n):
            s = 0
            for i in range (r, n):
                s = s + Q[i][j] * u[i]
            gamma = s / beta
            for i in range (r, n):
                Q[i][j] = Q[i][j] - gamma * u[i]
    return Q, A, b

def print_matrix(A):
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end=" ")
        print()

def main():
    n =3
    s = generate_vector_s(n)
    A = generate_matrix(n)
    print("A:")
    print_matrix(A)
    print()
    calculate_vector(A, n, s)
    print("s:", s)
    print()
    Q, R, b = QR(A, n, s)
    print("Q:")
    print_matrix(Q)
    print()
    print("R:")
    print_matrix(R)
    print()
    print("b:", b)
    print()



if __name__ == "__main__":
    main()