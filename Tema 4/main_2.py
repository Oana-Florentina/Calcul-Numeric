import re

import numpy as np

epsilon = 10 ** (-5)


def extract_data(file_path):
    pattern = r'(-?[\d.]+)\s*,\s*(\d+)\s*,\s*(\d+)'
    element_list = []
    try:
        with open(file_path, "r") as f:
            n = int(f.readline().strip())
            for line in f:
                matches = re.match(pattern, line.strip())
                if matches:
                    num_1 = float(matches.group(1))
                    num_2 = int(matches.group(2))
                    num_3 = int(matches.group(3))
                    element_list.append([num_1, num_2, num_3])
    except Exception as e:
        print(f"Error: {e}")
    return n, element_list


def create_vectors(n, element_list):
    values = []
    ind_col = []
    row_start = [0] * (n + 1)

    sorted_elements = sorted(element_list, key=lambda x: (x[1], x[2]))

    last_row = -1
    last_column = -1
    for i, (value, row, col) in enumerate(sorted_elements):
        if row == last_row and col == last_column:
            values[-1] += value
        else:
            values.append(value)
            ind_col.append(col)

        if row != last_row:
            row_start[row] = len(values) - 1
            last_row = row

        last_column = col

    row_start[n] = len(values)

    return values, ind_col, row_start


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


#
#
# def check_diagonal(n, values, ind_col, row_start):
#     for row in range(n):
#         diagonal_element_found = False
#         for idx in range(row_start[row], row_start[row + 1]):
#             if ind_col[idx] == row:
#                 diagonal_element_found = True
#                 if abs(values[idx]) < epsilon:
#                     print(f"Diagonal element from row {row} is 0")
#                     return
#                 break
#         if not diagonal_element_found:
#             print(f"Doesn't have a diagonal element in row {row}")
#             return
#
#     print("Matrix has diagonal elements")
#

def Gauss_Seidel(n, values, ind_col, row_start, b, k_max):
    k = 0
    x = [0 for _ in range(n + 1)]

    while True:
        old_x = np.copy(x)
        for i in range(n):
            sum_ = 0
            diag_val = None

            for j in range(row_start[i], row_start[i + 1]):
                if ind_col[j] == i:
                    diag_val = values[j]
                else:
                    sum_ += values[j] * x[ind_col[j]]

            if diag_val is None or abs(diag_val) < epsilon:
                raise ValueError(f"Diagonal element from row {i} is 0 or doesn't exist, determinant is 0")

            x[i] = (b[i] - sum_) / diag_val

        norm_error = np.linalg.norm(np.array(x) - np.array(old_x), ord=1)
        k += 1

        # print("norm_error:", norm_error)

        if k > k_max or norm_error < epsilon or norm_error > 10 ** 306:
            if k > k_max:
                print("Number of iterations is greater than k_max")

            if norm_error > 10 ** 90:
                print("Norm error is greater than 10^")

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


def norm_solution(n, values, ind_col, row_start, b, x):
    prod = [0 for _ in range(n)]
    for i in range(n):
        line_sum = 0
        for j in range(row_start[i], row_start[i + 1]):
            line_sum += values[j] * x[ind_col[j]]
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
    n, element_list = extract_data("a_4.txt")
    print("n:", n)
    values, ind_col, row_start = create_vectors(n, element_list)
    # print("values:", values)
    # print("ind_col:", ind_col)
    # print("row_start:", row_start)
    b = extract_b("b_4.txt")
    # b = [6, 7, 8, 9, 1]
    # check_diagonal(n, values, ind_col, row_start)
    k_max = 100000
    x = Gauss_Seidel(n, values, ind_col, row_start, b, k_max)
    print("x:", x)

    norm_solution(n, values, ind_col, row_start, b, x)


if __name__ == "__main__":
    main()