import math
import random
import numpy as np

epsilon = 1e-5

def generate_vector_for_symmetric_matrix(n):
    v = []
    for i in range(n):
        for j in range(i, n):
             v.append(random.randint(-10, 10))
    return v


def index(i, j):
    if i < j:
        i, j = j, i
    return i * (i + 1) // 2 + j


def calculate_p_q(A):
    n = 3
    print("n=", n)

    p = 0
    q = 0
    max = -999999
    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[index(i,j)]) > max:
                max = abs(A[index(i,j)])
                p = i
                q = j
    return p, q


def calculate_c_s_t(A, p, q):
    if A[index(p, q)] == 0:
        return 1, 0, 0

    alpha = (A[index(p, p)] - A[index(q, q)]) / (2 * A[index(p, q)])
    if alpha >= 0:
        t = -alpha + math.sqrt(1 + alpha ** 2)
    else:
        t = -alpha - math.sqrt(1 + alpha ** 2)
    c = 1 / math.sqrt(1 + t ** 2)
    s = t / math.sqrt(1 + t ** 2)
    return c, s, t


def is_not_diagonal(A, n):
    for i in range(n):
        for j in range(n):
            if i != j and abs(A[index(i,j)]) > epsilon:
                return True
    return False


def apply_rotation(A, R, n):
    # Convertim vectorul A într-o matrice
    A_matrix = np.zeros((n, n))
    index = 0
    for i in range(n):
        for j in range(i + 1):
            A_matrix[i][j] = A[index]
            A_matrix[j][i] = A[index]

            index += 1
    print("A_matrix=")
    print(A_matrix)
    # Efectuăm înmulțirea R * A_matrix * R.T
    A_matrix = np.dot(np.dot(R, A_matrix), R.T)
    print("A_matrix dupa =")
    print(A_matrix)
    # Extragem partea inferioară a matricei A_new și o convertim înapoi într-un vector
    A_new_lower_triangular = []
    for i in range(n):
        for j in range(i + 1):
            A_new_lower_triangular.append(A_matrix[i][j])
    print("A_new_lower_triangular=")
    print(A_new_lower_triangular)
    return A_new_lower_triangular


def jacobi(A):
    k = 0
    n = 3  # Calculăm dimensiunea matricei corespunzătoare vectorului A
    U = np.identity(n)
    k_max = 1000
    p, q = calculate_p_q(A)
    print("p=", p, "q=", q)
    print("A index: ", A[index(p,q)])
    print("index:", index(p, q))
    c, s, t = calculate_c_s_t(A, p, q)
    print("c=", c, "s=", s, "t=", t)
    while k <= k_max and is_not_diagonal(A, 3):
        R = np.zeros((n, n))
        for j in range(n):
            for i in range(n):
                if i == j and i != p and i != q:
                    R[i][j] = 1
                else:
                    if i == j and (i == p or i == q):
                        R[i][i] = c
                    else:
                        if i == p and j == q:
                            R[i][j] = s
                        else:
                            if i == q and j == p:
                                R[i][j] = -s
                            else:
                                R[i][j] = 0
        print("R=", R)
        # Aplicăm rotația asupra vectorului A
        A = apply_rotation(A, R, n)
        print("A=")
        print_matrix_from_vector(A, n)
        U = np.dot(U, R.T)

        p, q = calculate_p_q(A)
        print("p=", p, "q=", q)

        c, s, t = calculate_c_s_t(A, p, q)

        k += 1
        print("k=", k)
    return A, U



def generate_symmetric_matrix(n):
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            A[i][j] = random.randint(-10, 10)
            A[j][i] = A[i][j]
    return A


def matrix_norm(matrix):
    return np.linalg.norm(matrix, ord='fro')


def print_matrix_from_vector(v, n):
    for i in range(n):
        for j in range(n):
            if j <= i:
                print(v[i * (i + 1) // 2 + j], end=" ")
            else:
                print(v[j * (j + 1) // 2 + i], end=" ")
        print()

def print_matrix(A):
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end=" ")
        print()


def calculate_A_final(A_init, U, n):
    # Convertim vectorul A_init într-o matrice
    A_init_matrix = np.zeros((n, n))
    index = 0
    for i in range(n):
        for j in range(i + 1):
            A_init_matrix[i][j] = A_init[index]
            index += 1

    # Calculăm A_final
    A_final_matrix = np.dot(np.dot(U.T, A_init_matrix), U)

    # Extragem partea inferioară a matricei A_final și o convertim înapoi într-un vector
    A_final_lower_triangular = []
    for i in range(n):
        for j in range(i + 1):
            A_final_lower_triangular.append(A_final_matrix[i][j])

    return A_final_lower_triangular


def calculate_eigenvalues(A_init, U, n):
    # Convertim vectorul A_init într-o matrice
    A_init_matrix = np.zeros((n, n))
    index = 0
    for i in range(n):
        for j in range(i + 1):
            A_init_matrix[i][j] = A_init[index]
            index += 1

    # Calculăm valorile proprii aproximative ale matricei A_init
    eigenvalues = np.linalg.eigvalsh(A_init_matrix)

    # Formăm matricea diagonală Λ din valorile proprii
    eigenvalues_matrix = np.diag(eigenvalues)

    # Calculăm diferența între A_init * U și U * Λ
    difference_matrix = np.dot(A_init_matrix, U) - np.dot(U, eigenvalues_matrix)

    # Calculăm norma matriceală a diferenței
    norm_difference = np.linalg.norm(difference_matrix, ord='fro')

    return norm_difference

def main():
    n = 3
    A = generate_vector_for_symmetric_matrix(n)
    A = [0, 0, 0, 1, 1, 1]
    A_init = np.copy(A)
    print("A_init:")
    print_matrix_from_vector(A_init, n)
    print(A)

    calculate_p_q(A)
    A, U = jacobi(A)
    print("A:")
    print_matrix_from_vector(A, n)
    print("U:")
    print_matrix(U)
    A_final = calculate_A_final(A_init, U, n)
    print("A_Final:")
    print_matrix_from_vector(A_final, n)

    # Formarea matricei diagonale Λ din valorile proprii aproximative
    print("norma:", calculate_eigenvalues(A_init, U, n))


if __name__ == "__main__":
    main()