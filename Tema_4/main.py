import numpy as np
import re
import gradio as gr

epsilon = 10 ** (-10)


def extract_data(file_path, sparse_matrix=None, compare_matrix=None, sign_=1):
    pattern = r'(-?[\d.]+)\s*,\s*(\d+)\s*,\s*(\d+)'
    try:
        f = open(file_path, "r")
        n = int(f.readline().strip())
        if sparse_matrix is None:
            sparse_matrix = [[] for _ in range(n)]

        for line in f:

            matches = re.match(pattern, line.strip())
            if matches:
                num_1 = float(matches.group(1))  # elementul
                num_2 = int(matches.group(2))  # linia
                num_3 = int(matches.group(3))  # coloana

                dup = False
                for index, tuple_ in enumerate(sparse_matrix[num_2]):
                    column = tuple_[1]
                    if column == num_3:
                        # print("Matrix has multiple elements in the same position")
                        sparse_matrix[num_2][index][0] += sign_ * num_1
                        # stergem elementul daca suma este 0
                        # epsilooon
                        if sparse_matrix[num_2][index][0] < epsilon:
                            del sparse_matrix[num_2][index]

                        dup = True

                if not dup:
                    sparse_matrix[num_2].append([num_1, num_3])  # moddd

                    if compare_matrix is not None:
                        print("Matrix has different elements. AB != A + B")
                        return

        return sparse_matrix, n

    except:
        print("Error while reading the file 1")


def check_diagonal(A, n):
    for i in range(n):
        diagonal_element_found = False
        for entry in A[i]:
            if entry[1] == i:
                diagonal_element_found = True
                break
        if not diagonal_element_found:
            print("Elementul de pe diagonala la linia", i, "nu este specificat în fișierul de intrare.")
            return False
    print("Toate elementele de pe diagonala sunt specificate în fișierul de intrare.")
    return True


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


def Gauss_Seidel(A, b, x, n, k_max, norm_error_max):
    k = 0
    old_x = []
    norm_error = 0
    while True:
        old_x = np.copy(x)
        for i in range(n):
            line = A[i]
            sum_ = 0
            diag = None
            for tuple_ in line:
                if tuple_[1] != i:
                    sum_ += tuple_[0] * x[tuple_[1]]
                else:
                    diag = tuple_[0]

            if diag is None or abs(diag) < epsilon:
                raise ValueError(f"Diagonal element from row {i} is 0 or doesn't exist, determinant is 0")

            x[i] = (b[i] - sum_) / diag

        norm_error = np.linalg.norm(np.array(x) - np.array(old_x), ord=1)
        k += 1

        # print("norm_error:", norm_error)

        if k > k_max or norm_error < epsilon or norm_error > norm_error_max:
            if k > k_max:
                print("Number of iterations is greater than k_max")

            if norm_error > 10 ** 40:
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
    result = "||A*x_GS||_inf: {}".format(norm)
    if norm < epsilon:
        print("Norm is less than epsilon, so the solution is correct")
        result += "\nNorm is less than epsilon, so the solution is correct"
    else:
        print("Norm is greater than epsilon, so the solution is incorrect")
        result += "\nNorm is greater than epsilon, so the solution is incorrect"

    return result


def verify_matrix_is_empty(sparse_matrix):
    for line in sparse_matrix:
        if len(line) > 0:
            print("Matrix has different elements. AB != A + B")
            return "Matrix has different elements. AB != A + B"

    print("Matrix has the same elements. AB == A + B")
    return "Matrix has the same elements. AB == A + B"

def process_files_gauss_seidel_norm(a_file, b_file, operations, k_max, norm_error_max):
    print("Processing files")
    results = []

    if a_file and b_file:
        A, n = extract_data(a_file.name)
        x = [0 for _ in range(n)]
        b = extract_b(b_file.name)
        x = Gauss_Seidel(A, b, x, n, k_max, norm_error_max)
        n_s = norm_solution(A, x, b, n)

        if "Gauss-Seidel" in operations:
            results.append("Gauss-Seidel Solution: {}".format(x))

        if "Norm" in operations:
            results.append("Norm calculation: {}".format(n_s))

    return "\n\n".join(results)


def process_files_sum_comparison(a_file, b_file, aplusb_file, operations):
    results = []

    if a_file and b_file:
        A_, n_ = extract_data(a_file.name)
        AB_, n__ = extract_data(b_file.name, A_)

        if "Sum of Matrices" in operations:
            results.append("Sum of Matrices: {}".format(AB_))

        if aplusb_file and "Verify Sum" in operations:
            result, n = extract_data(aplusb_file.name, AB_, 1, -1)
            result = verify_matrix_is_empty(result)
            results.append("Verification Result: {}".format(result))

    return "\n\n".join(results)



def main():
    A, n = extract_data("a_1.txt")
    x = [0 for _ in range(n)]
    b = extract_b("b_1.txt")
    print(len(A))
    print(len(b))
    k_max = 30000
    norm_error_max = 10 ** 60
    A = [[(2.5, 2), (102.5, 0)], [(3.5, 0), (0.33, 4), (1.05, 2), (104.88, 1)], [(100, 2)], [(1.3, 1), (101.3, 3)],
         [(1.5, 3), (0.73, 0), (102.23, 4)]]
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    b = [6.0, 7.0, 8.0, 9.0, 1.0]
    n = 5
    x = Gauss_Seidel(A, b, x, n, k_max, norm_error_max)
    norm_solution(A, x, b, n)

    # bonus
    A_, n_ = extract_data("a.txt")
    AB_, n__ = extract_data("b.txt", A_)
    print("Matrix A+B")
    print(AB_)

    if n_ != n__:
        print("Matrices have different sizes")
        return

    result, n = extract_data("aplusb.txt", AB_, 1, -1)
    print("Matrix after comparison")
    print(result)
    verify_matrix_is_empty(result)

# if __name__ == "__main__":
# main()
