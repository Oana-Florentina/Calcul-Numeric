import re
import gradio as gr
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

def Gauss_Seidel(n, values, ind_col, row_start, b, k_max, norm_error_max):
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

        if k > k_max or norm_error < epsilon or norm_error > norm_error_max:
            if k > k_max:
                print("Number of iterations is greater than k_max")

            if norm_error > norm_error_max:
                print("Norm error is greater than norm_error_max")

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
    result = "||A*x_GS||_inf: {}".format(norm)
    print("||A*x_GS||_inf:", norm)

    if norm < epsilon:
        print("Norm is less than epsilon, so the solution is correct")
        result += "\nNorm is less than epsilon, so the solution is correct"
    else:
        print("Norm is greater than epsilon, so the solution is incorrect")
        result += "\nNorm is greater than epsilon, so the solution is incorrect"

    return result


def add_sparse_matrices(values_a, ind_col_a, row_start_a, values_b, ind_col_b, row_start_b, n):
    values_result = []
    ind_col_result = []
    row_start_result = [0]

    for row in range(n):
        a_index = row_start_a[row]
        b_index = row_start_b[row]
        a_end = row_start_a[row + 1]
        b_end = row_start_b[row + 1]

        current_row_elements = {}

        while a_index < a_end or b_index < b_end:
            if a_index < a_end:
                col_a = ind_col_a[a_index]
                val_a = values_a[a_index]
                if col_a in current_row_elements:
                    current_row_elements[col_a] += val_a
                else:
                    current_row_elements[col_a] = val_a
                a_index += 1

            if b_index < b_end:
                col_b = ind_col_b[b_index]
                val_b = values_b[b_index]
                if col_b in current_row_elements:
                    current_row_elements[col_b] += val_b
                else:
                    current_row_elements[col_b] = val_b
                b_index += 1

        for col, val in sorted(current_row_elements.items()):
            if val != 0:
                ind_col_result.append(col)
                values_result.append(val)

        row_start_result.append(len(values_result))

    return values_result, ind_col_result, row_start_result


def compare_sparse_matrices(values_a, ind_col_a, row_start_a, values_b, ind_col_b, row_start_b):
    if len(values_a) != len(values_b) or len(ind_col_a) != len(ind_col_b) or len(row_start_a) != len(row_start_b):
        print("Matrices are not equal len")
        return False

    for i in range(len(row_start_a)):
        if row_start_a[i] != row_start_b[i]:
            print("Matrices are not equal")
            return False

    for i in range(len(ind_col_a)):
        if ind_col_a[i] != ind_col_b[i]:
            print("Matrices are not equal")
            return False

    for i in range(len(values_a)):
        if abs(values_a[i] - values_b[i]) > epsilon:
            print("Matrices are not equal")

            return False

    print("Matrices are equal")
    return True


def process_files_gauss_seidel_norm_2(a_file, b_file, operations, k_max, norm_error_max):
    results = []

    if a_file and b_file:
        n, element_list = extract_data(a_file.name)
        values, ind_col, row_start = create_vectors(n, element_list)
        b = extract_b(b_file.name)

        x = Gauss_Seidel(n, values, ind_col, row_start, b, k_max, norm_error_max)
        n_s = norm_solution(n, values, ind_col, row_start, b, x)

        if "Gauss-Seidel" in operations:
            results.append("Gauss-Seidel Solution: {}".format(x))

        if "Norm" in operations:
            results.append("Norm calculation: {}".format(n_s))

    return "\n\n".join(results)


def process_files_sum_comparison_2(a_file, b_file, aplusb_file, operations):
    results = []

    if a_file and b_file:
        n, values_a = extract_data(a_file.name)
        n_, values_b = extract_data(b_file.name)
        if n != n_:
            results.append("Matrices have different dimensions")
            return "\n\n".join(results)

        values_a, ind_col_a, row_start_a = create_vectors(n, values_a)
        values_b, ind_col_b, row_start_b = create_vectors(n, values_b)

        if "Sum of Matrices" in operations:
            values_result, ind_col_result, row_start_result = add_sparse_matrices(values_a, ind_col_a, row_start_a,
                                                                                  values_b, ind_col_b, row_start_b, n)
            results.append("Sum of Matrices: values={}, ind_col={}, row_start={}".format(values_result, ind_col_result,
                                                                                         row_start_result))

        if aplusb_file and "Verify Sum" in operations:
            n__, values_ab = extract_data(aplusb_file.name)
            if n != n__:
                results.append("Matrices have different dimensions")
                return "\n\n".join(results)

            values_ab, ind_col_ab, row_start_ab = create_vectors(n, values_ab)
            are_equal = compare_sparse_matrices(values_ab, ind_col_ab, row_start_ab, values_result, ind_col_result,
                                                row_start_result)

            if are_equal:
                results.append("Matrices are equal")
            else:
                results.append("Matrices are not equal")

        return "\n\n".join(results)

    def main():
        n, element_list = extract_data("a_1.txt")
        print("n:", n)
        values, ind_col, row_start = create_vectors(n, element_list)
        # print("values:", values)
        # print("ind_col:", ind_col)
        # print("row_start:", row_start)
        b = extract_b("b_1.txt")
        # b = [6, 7, 8, 9, 1]
        # check_diagonal(n, values, ind_col, row_start)
        k_max = 100000
        norm_error_max = 10 ** 10
        x = Gauss_Seidel(n, values, ind_col, row_start, b, k_max, norm_error_max)
        # print("x:", x)

        norm_solution(n, values, ind_col, row_start, b, x)

        # bounus
        n, values_a = extract_data("a.txt")
        n_, values_b = extract_data("b.txt")
        if n != n_:
            print("Matrices have different dimensions")
            return

        values_a, ind_col_a, row_start_a = create_vectors(n, values_a)
        values_b, ind_col_b, row_start_b = create_vectors(n, values_b)

        values_result, ind_col_result, row_start_result = add_sparse_matrices(values_a, ind_col_a, row_start_a,
                                                                              values_b,
                                                                              ind_col_b, row_start_b, n)

        print("values_result:", values_result)
        print("ind_col_result:", ind_col_result)
        print("row_start_result:", row_start_result)

        n__, values_ab = extract_data("aplusb.txt")
        if n != n__:
            print("Matrices have different dimensions")
            return
        values_ab, ind_col_ab, row_start_ab = create_vectors(n, values_ab)
        print("values_ab:", values_ab)
        print("ind_col_ab:", ind_col_ab)
        print("row_start_ab:", row_start_ab)

        are_equal = compare_sparse_matrices(values_ab, ind_col_ab, row_start_ab, values_result, ind_col_result,
                                            row_start_result)
        print("Matrices are equal:", are_equal)

    # if __name__ == "__main__":
    # main()
