import math
import random
import numpy as np

epsilon = 1e-5

def calculate_p_q(A):
    n = len(A)
    p = 0
    q = 0
    max = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[i][j]) > max:
                max = abs(A[i][j])
                p = i
                q = j
    return p, q

def calculate_c_s_t (A, p, q):
    if A[p][q] == 0:
        c = 1
        s = 0
        t = 0
    else:
        alpha = (A[p][p] - A[q][q]) / (2 * A[p][q])
        if alpha >= 0:
            t = -alpha + math.sqrt(1 + alpha ** 2)
        else:
            t = -alpha - math.sqrt(1 + alpha ** 2)
        c = 1 / math.sqrt(1 + t ** 2)
        s = t / math.sqrt(1 + t ** 2)
    return c, s, t


def is_not_diagonal(A):
    n = len(A)
    for i in range(n):
        for j in range(n):
            if i != j and abs(A[i][j]) > epsilon:
                return True
    return False

def jacobi(A):
    k = 0
    U = np.identity(len(A))
    n = len(A)
    k_max = 1000
    while k < k_max and is_not_diagonal(A):
        p, q = calculate_p_q(A)
        c, s, t = calculate_c_s_t(A, p, q)
        for j in range(n):
            if j != p and j != q:
                A[p][j] = c * A[p][j] + s * A[q][j]
                A[q][j] = -s * A[j][p] + c * A[q][j]
                A[j][p] = A[p][j]
                A[p][p] = A[p][p] + t * A[p][q]
                A[q][q] = A[q][q] - t * A[p][q]
                A[p][q] = 0
        for i in range(n):
            copie = U[i][p]
            U[i][p] = c * U[i][p] + s * U[i][q]
            U[i][q] = -s * copie + c * U[i][q]
        k += 1
    return A, U

def generate_symmetric_matrix(n):
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            A[i][j] = random.randint(1, 10)
            A[j][i] = A[i][j]
    return A

def matrix_norm(matrix):
    return np.linalg.norm(matrix, ord='fro')

def print_matrix(A):
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end=" ")
        print()
def main():

    n = 5
    epsilon = 10 ** (-9)
    A = generate_symmetric_matrix(n)
    A_init = np.copy(A)
    print("A_init:")
    print_matrix(A_init)
    A, U = jacobi(A)
    print("A:")
    print_matrix(A)
    print("U:")
    print_matrix(U)
    A_final = np.dot(np.dot(U.T, A_init), U)
    print("A_Final:")
    print_matrix(A_final)

    # Formarea matricei diagonale Λ din valorile proprii aproximative
    eigenvalues = np.diag(A)

    # Verificarea A_init * U ≈ U * Λ prin calcularea normei matriceale a diferenței
    norm_difference = matrix_norm(np.dot(A_init, U) - np.dot(U, np.diag(eigenvalues)))
    print("Norma matriceală a diferenței între A_init * U și U * Λ:", norm_difference)


if __name__ == "__main__":
    main()