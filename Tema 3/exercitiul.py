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
            break
        k = math.sqrt(s)
        if A[r][r] > 0:
            k = -k
        beta = s - k * A[r][r]
        u[r] = A[r][r] - k
        for i in range(r+1, n):
            u[i] = A[i][r]
        for j in range(r+1, n):
            s = 0
            for i in range(r, n):
                s += u[i] * A[i][j]
            gamma = s / beta
            for i in range(r, n):
                A[i][j] -= gamma * u[i]
        for i in range(r+1, n):
            A[i][r] = 0
        A[r][r] = k
        for j in range(0, n):
            s = 0
            for i in range(r, n):
                s += Q[i][j] * u[i]
            gamma = s / beta
            for i in range(r, n):
                Q[i][j] -= gamma * u[i]
        s = 0
        for j in range(r, n):
            s += b[j] * u[j]
        gamma = s / beta
        for i in range(r, n):
                b[i] -= gamma * u[i]

    R = A
    return Q.T, R, b


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
    A_init_x_house = np.dot(A_init, X_house)
    return np.linalg.norm(A_init_x_house - b_init)


def calculate_third_norm(X_house, s):
    return np.linalg.norm(X_house - s)/np.linalg.norm(s)


def inverse_with_qr(Q, R):
    n = Q.shape[0]
    inverse = np.zeros((n, n))

    for i in range(n):
        e = np.zeros(n)
        e[i] = 1
        y = np.dot(Q.T, e)
        x = solve_system(R, n, y)
        inverse[:, i] = x
        print("x:", x)

    print("aiciiiiii")
    print(inverse)
    return inverse

def is_positive_definite(A):
    return np.all(np.linalg.eigvals(A) > 0)

def bonus(A):
    k = 0
    Q, R = np.linalg.qr(A)

    k_max = 10000
    try:
        if not is_positive_definite(A):
            raise ValueError("Matricea nu este pozitiv definită.")
        prev = A
        Q, R = np.linalg.qr(A)
        A = R @ Q

        while np.linalg.norm(A - prev) > epsilon or k > k_max:
            k += 1
            prev = A
            Q, R = np.linalg.qr(A)
            A = R @ Q


        return A
    except np.linalg.LinAlgError as e:
        print("A apărut o eroare în timpul calculului:", e)
        return
    except ValueError as e:
        print(e)
        return


def generate_positive_definite_matrix(n):
    A = np.random.rand(n, n)
    A = 0.5 * (A + A.T)
    A += np.eye(n) * n
    positive_definite_matrix = np.dot(A, A.T)
    return positive_definite_matrix


def calculate_svd(A):
    U, S, VT = np.linalg.svd(A)
    return U, S, VT

def main():
    n = 3
    s = [3, 2, 1]
    A = [[0, 0, 4], [1, 2, 3], [0, 1, 2]]

    s = generate_vector_s(n)
    A = generate_matrix(n)
    A_bonus = generate_positive_definite_matrix(n)
    A_init = np.copy(A)
    A_init = np.array(A_init, dtype=np.float32)
    A_init2=np.copy(A_init)
    print("--------ex1----------")
    print()
    print("A:")
    print_matrix(A)
    print()
    print("s:", s)
    b = calculate_vector(A, n, s)
    b_init = np.copy(b)
    print("b:", b)

    print()
    print("--------ex5----------")
    print()

    Q, R, b = QR(A, n, b)
    inverse_qr=inverse_with_qr(Q, R)
    inverse_library = np.linalg.inv(A_init2)
    difference = np.linalg.norm(inverse_qr - inverse_library)
    print("Norma diferenței dintre inversa calculată cu QR și inversa din bibliotecă:", difference)
    print()
    print("--------ex2----------")
    print()
    print("Q:")
    print_matrix(Q)
    print("R:")
    print_matrix(R)
    print()
    print("--------ex3----------")
    print()
    X_house = solve_system(R, n, np.dot(Q.T, b_init))

    x_QR = find_x_qr_with_lib(A_init, n, b_init)

    print("x_QR:", x_QR)
    print("X_house:", X_house)
    print("norma:", calculate_norm(x_QR, X_house))

    print()
    print("--------ex4----------")
    print()

    print("norm between A_init * X_house and b_init:", calculate_second_norm(A_init, X_house, b_init))
    print("norm between A_init * x_QR and b_init:", calculate_second_norm(A_init, x_QR, b_init))
    print("norm between X_house and s:", calculate_third_norm(X_house, s))
    print("norm between x_QR and s:", calculate_third_norm(x_QR, s))

    print("--------BONUUUS----------")
    _, singular_values, _ = calculate_svd(A_bonus)
    print("singular_values: ", singular_values)
    print("bonus: ", bonus(A_bonus))




if __name__ == "__main__":
    main()