import copy
import random

import gradio as gr
import numpy as np
import pandas as pd

# app = gr.Interface(lambda name: "Bye " + name, "text", "text")

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
        # inf triunghiulara
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

    if abs(determinant(A)) < epsilon:
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
    n = len(A_init)
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


def generate_matrix(n):
    return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]


def generate_vector_s(n):
    return [random.randint(-10, 10) for _ in range(n)]


def process_matrix(random_matrix, random_vector, n, matrix_input, vector_input):
    if random_matrix:
        A_init = np.random.randint(-10, 10, size=(n, n)).tolist()
    else:
        A_init = matrix_input.values.tolist()

    if random_vector:
        b = np.random.randint(-10, 10, size=(n,)).tolist()
    else:
        b = vector_input.values.flatten().tolist()

    A = copy.deepcopy(A_init)
    LU_decomposition(A, A_init, n)

    det_A = determinant(A)
    y = forward_substitution(A, n, b)
    x = backward_substitution(A, n, y)

    verify_euclidian_norm(A_init, x, b)
    solve_equation(A_init, b, x)

    L, U = LU_decomposition_2(A_init, n)

    return pd.DataFrame(A_init, columns=[str(i) for i in range(n)]), pd.DataFrame(b, columns=[
        "0"]), f"Determinant of A: {det_A}\nY: {y}\nX: {x}\nL: {L}\nU: {U}"


def launch_interface():
    with gr.Blocks() as iface:
        n_input = gr.Number(label="Size of the matrix", value=3, precision=0, interactive=True)

        random_matrix = gr.Checkbox(label="Generate Random Matrix")
        random_vector = gr.Checkbox(label="Generate Random Vector")

        matrix_input = gr.Dataframe(
            label="Matrix Input",
            value=pd.DataFrame(np.zeros((3, 3)), columns=["0", "1", "2"]),
            row_count=3,
            col_count=3,
            type="pandas",
            interactive=True
        )

        vector_input = gr.Dataframe(
            label="Vector Input",
            value=pd.DataFrame(np.zeros((3,)), columns=["0"]),
            row_count=3,
            col_count=1,
            type="pandas",
            interactive=True
        )

        output_matrix = gr.Dataframe(label="Processed Matrix")
        output_vector = gr.Dataframe(label="Processed Vector")
        output_text = gr.Textbox(label="Results")

        def update_matrix_size(n):
            n = int(n)
            new_matrix = pd.DataFrame(np.zeros((n, n)), columns=[str(i) for i in range(n)])
            new_vector = pd.DataFrame(np.zeros((n,)), columns=["0"])
            return new_matrix, new_vector

        n_input.change(update_matrix_size, inputs=[n_input], outputs=[matrix_input, vector_input])

        btn = gr.Button("Submit")
        btn.click(process_matrix, inputs=[random_matrix, random_vector, n_input, matrix_input, vector_input],
                  outputs=[output_matrix, output_vector, output_text])

    iface.launch()


launch_interface()

# if __name__ == "__main__":
#     # A_init = [[2, 0, 2],
#     #           [1, 2, 5],
#     #           [1, 1, 7]]
#     #
#     # b = [4, 10, 10]
#
#     # A_init = generate_matrix(3)
#     #
#     # b = generate_vector_s(3)
#
#     A_init = [[2.5, 2, 2],
#               [5, 6, 5],
#               [5, 6, 6.5]]
#     b = [2, 2, 2]
#
#     A = copy.deepcopy(A_init)
#
#     n = len(A_init)
#
#     LU_decomposition(A, A_init, n)
#
#     print("det A:", determinant(A))
#
#     y = forward_substitution(A, n, b)
#     print("y:", y)
#     x = backward_substitution(A, n, y)
#     print("x:", x)
#
#     verify_euclidian_norm(A_init, x, b)
#
#     solve_equation(A_init, b, x)
#
#     print_matrix(A, "L")
#     print_matrix(A, "U")
#     L, U = LU_decomposition_2(A_init, n)
#     print("L:", L)
#     print("U:", U)
