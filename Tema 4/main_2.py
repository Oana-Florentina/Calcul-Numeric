import sys

import numpy as np

epsilon = 10 ** (-5)

import re


def extract_data(file_path):
    pattern = r'(-?[\d.]+)\s*,\s*(\d+)\s*,\s*(\d+)'
    element_list = []
    try:
        f = open(file_path, "r")
        n = int(f.readline().strip())
        for line in f:
            # print(line)
            matches = re.match(pattern, line.strip())
            if matches:
                num_1 = float(matches.group(1))
                num_2 = int(matches.group(2))
                num_3 = int(matches.group(3))
                element_list.append((num_1, num_2, num_3))

        element_list.sort(key=lambda x: (x[1], x[2]))

        valori = []
        ind_col = []
        current_line = 0
        inceput_linii = [0]

        for element, line_idx, col_idx in element_list:
            while current_line < line_idx:
                inceput_linii.append(len(valori))
                current_line += 1

            valori.append(element)
            ind_col.append(col_idx)

        inceput_linii.append(len(valori))
        return n,valori, ind_col, inceput_linii

    except:
        print("Error while reading the file 1")
        sys.exit(1)


def extract_b(file_path):
    b = []
    k = 0
    pattern = r'^\s*-?\d+(\.\d+)?\s*$'
    try:
        f = open(file_path, "r")
        n = int(f.readline().strip())
        for line in f:
            if re.match(pattern, line.strip()):
                b.append(float(line.strip()))
            else:
                print("Invalid number in the file: ", line)

        return b
    except:
        print("Error while reading the file b")


def calculate_norm_error(x, old_x):
    for i in range(len(x)):
        x[i] -= old_x[i]

    sum_ = 0
    for i in range(len(x)):
        # print("old_x[i]:", old_x[i])
        sum_ += abs(x[i])

    return sum_


def Gauss_Seidel(A, b, x, n, k_max):
    k = 0
    old_x = []
    norm_error = 0
    while True:
        old_x = np.copy(x)
        for i in range(n):
            line = A[i]
            sum_ = 0
            for tuple_ in line:
                if tuple_[1] != i:
                    sum_ += tuple_[0] * x[tuple_[1]]
                else:
                    diag = tuple_[0]

            x[i] = (b[i] - sum_) / diag

        norm_error = np.linalg.norm(np.array(x) - np.array(old_x), ord=1)
        k += 1

        # print("norm_error:", norm_error)

        if k > k_max or norm_error < epsilon or norm_error > 10 ** 60:
            if k > k_max:
                print("Number of iterations is greater than k_max")

            if norm_error > 10 ** 40:
                print("Norm error is greater than 10^40")

            if norm_error < epsilon:
                print("Norm error is less than epsilon")
            break

    print("Number of iterations: ", k)
    if norm_error < epsilon:
        print("x:", x)
        print("convergenta")
        print("norm_error:", norm_error)
    else:
        print("divergenta")
        print("norm_error:", norm_error)

    return x


def norm_solution(A, x, b, n):
    prod = [0 for _ in range(n)]
    for i in range(n):
        line = A[i]
        line_sum = 0
        for tuple_ in line:
            line_sum += tuple_[0] * x[tuple_[1]]
        prod[i] = line_sum

    for i in range(n):
        prod[i] -= b[i]

    norm = max(abs(x) for x in prod)
    print("||A*x_GS||_inf:", norm)
    if norm < epsilon:
        print("Norm is less than epsilon, so the solution is correct")
    else:
        print("Norm is greater than epsilon, so the solution is incorrect")


def main():
    n, valori, ind_col, inceput_linii = extract_data("a_5.txt")
    print("n:", n)
    print("valori:", valori)
    print("ind_col:", ind_col)
    print("inceput_linii:", inceput_linii)


if __name__ == "__main__":
    main()
