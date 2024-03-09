import copy

import numpy as np

epsilon = 10 ** (-5)


def validation_matrix(A):
    n = len(A)
    for i in range(n):
        if len(A[i]) != n:
            return False
    return True


def print_matrix(A, name):
    if name == "L":
        print("L matrix:")
        for i in range(len(A)):
            for j in range(len(A[i])):
                if i < j:
                    print(0, end=" ")
                else:
                    print(A[i][j], end=" ")
            print()
    elif name == "U":
        print("U matrix:")
        for i in range(len(A)):
            for j in range(len(A[i])):
                if i > j:
                    print(0, end=" ")
                elif i == j:
                    print(1, end=" ")
                else:
                    print(A[i][j], end=" ")
            print()
    else:
        print(name, "matrix:")
        for i in range(len(A)):
            for j in range(len(A[i])):
                print(A[i][j], end=" ")
            print()


def LU_decomposition(A, A_init, n):
    if not validation_matrix(A) or not validation_matrix(A_init) or A != A_init:
        print("Matrix is not valid")
        return "Matrix is not valid"

    for p in range(1, n + 1):
        for i in range(p, n + 1):
            A[i - 1][p - 1] = A_init[i - 1][p - 1] - sum(A[i - 1][k - 1] * A[k - 1][p - 1] for k in range(1, p))

        if abs(A[p - 1][p - 1]) < epsilon:
            print("Matrix cannot be decomposed")
            return "Matrix cannot be decomposed"

        for i in range(p + 1, n + 1):
            A[p - 1][i - 1] = (A_init[p - 1][i - 1] - sum(A[p - 1][k - 1] * A[k - 1][i - 1] for k in range(1, p))) / \
                              A[p - 1][p - 1]

    print_matrix(A, "A")
    print_matrix(A_init, "A_init")
    print_matrix(A, "L")
    print_matrix(A, "U")

    return A


def determinant(A):
    det_A = 1
    for i in range(len(A)):
        det_A *= A[i][i]
    return det_A


def forward_substitution(A, n, b):
    y = [0 for _ in range(n)]

    if determinant(A) == 0:
        print("Matrix is not valid")
        return "Matrix is not valid"

    for i in range(1, n + 1):
        for j in range(1, i):
            y[i - 1] += A[i - 1][j - 1] * y[j - 1]

        y[i - 1] = (b[i - 1] - y[i - 1]) / A[i - 1][i - 1]

    return y


def backward_substitution(A, n, y):
    x = [0 for _ in range(n)]

    if determinant(A) == 0:
        print("Matrix is not valid")
        return "Matrix is not valid"

    for i in range(n, 0, -1):
        for j in range(i + 1, n + 1):
            x[i - 1] += A[i - 1][j - 1] * x[j - 1]

        x[i - 1] = y[i - 1] - x[i - 1]

    return x


def verify_euclidian_norm(A_init, x, b_init):
    A_init_x_LU = []
    for i in range(n):
        sum_ = 0
        for j in range(n):
            sum_ += A_init[i][j] * x[j]
        A_init_x_LU.append(sum_)

    print("A_init_x_LU:", A_init_x_LU)

    for i in range(n):
        A_init_x_LU[i] -= b_init[i]

    print("A_init_x_LU - b_init:", A_init_x_LU)

    norm = 0
    for i in range(n):
        norm += A_init_x_LU[i] ** 2
    norm = norm ** 0.5

    print("norm:", '{0:.10f}'.format(norm))

    if norm <= 10 ** (-8):
        print("Norm is less than epsilon, so the solution is correct")
    else:
        print("Norm is greater than epsilon, so the solution is incorrect")


def solve_equation(A_init, b_init, x):
    A = np.array(A_init)

    x_ = np.array(x)
    print("x:", x)

    b = np.array(b_init)
    print("b_init:", b_init)

    x_lib = np.linalg.solve(A, b)
    print("x_lib:", x_lib)

    norm_1 = np.linalg.norm((x_ - x_lib), ord=2)
    print("||x - x_lib||_2:", norm_1)

    A_inverse = np.linalg.inv(A)
    print_matrix(A_inverse, "A_inverse")

    x_new = A_inverse.dot(b)
    print("x_new:", x_new)

    norm_2 = np.linalg.norm((x_ - x_new), ord=2)
    print("||x - A_inverse * b_init||_2:", norm_2)


def index(i, j):
    return i * (i + 1) // 2 + j


def LU_decomposition_2(A_init, n):
    # l_11, l_21, l_22, l_31, l_32, l_33
    # 1, u_12, u_13, 1, u_23, 1
    L = [1 for _ in range(0, n * (n + 1) // 2)]
    U = [1 for _ in range(0, n * (n + 1) // 2)]

    for p in range(1, n + 1):
        for i in range(p, n + 1):
            sum_ = sum(L[index(i - 1, k - 1)] * U[index(k - 1, p - 1)] for k in range(1, p))
            L[index(i - 1, p - 1)] = A_init[i - 1][p - 1] - sum_

        if abs(L[index(p - 1, p - 1)]) < epsilon:
            print("Matrix cannot be decomposed")
            return "Matrix cannot be decomposed"

        for i in range(p + 1, n + 1):
            sum_ = sum(L[index(p - 1, k - 1)] * U[index(k - 1, i - 1)] for k in range(1, p))
            U[index(p - 1, i - 1)] = (A_init[p - 1][i - 1] - sum_) / L[index(p - 1, p - 1)]

    return L, U


if __name__ == "__main__":
    # A_init = [[2, 0, 2],
    #           [1, 2, 5],
    #           [1, 1, 7]]
    #
    # b = [4, 10, 10]

    A_init = [[2.5, 2, 2],
              [5, 6, 5],
              [5, 6, 6.5]]
    b = [2, 2, 2]

    A = copy.deepcopy(A_init)

    n = len(A_init)

    LU_decomposition(A, A_init, n)

    print("det A:", determinant(A))

    y = forward_substitution(A, n, b)
    print("y:", y)
    x = backward_substitution(A, n, y)
    print("x:", x)

    verify_euclidian_norm(A_init, x, b)

    solve_equation(A_init, b, x)

    print_matrix(A, "L")
    print_matrix(A, "U")
    L, U = LU_decomposition_2(A_init, n)
    print("L:", L)
    print("U:", U)
