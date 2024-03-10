import numpy as np
import re

epsilon = 10 ** (-5)


def extract_data(file_path):
    pattern = r'(-?[\d.]+)\s*,\s*(\d+)\s*,\s*(\d+)'
    try:
        f = open(file_path, "r")
        n = int(f.readline().strip())
        sparse_matrix = [[] for _ in range(n)]
        for line in f:
            # print(line)
            matches = re.match(pattern, line.strip())
            if matches:
                num_1 = float(matches.group(1))  # elementul
                num_2 = int(matches.group(2))  # linia
                num_3 = int(matches.group(3))  # coloana

                if num_1 == 0:
                    print("Matrix has a 0 element but maybe there are other elements in the same line")
                    return None

                dup = False
                for index, tuple_ in enumerate(sparse_matrix[num_2]):
                    column = tuple_[1]
                    if column == num_3:
                        print("Matrix has multiple elements in the same position")
                        sparse_matrix[num_2][index][0] += num_1
                        dup = True


                if not dup:
                    sparse_matrix[num_2].append([num_1, num_3]) # moddd

        return sparse_matrix, n

    except:
        print("Error while reading the file 1")


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
    A, n = extract_data("a_5.txt")
    x = [0 for _ in range(n)]
    b = extract_b("b_5.txt")
    print(len(A))
    print(len(b))
    k_max = 30000
    # A = [[(2.5, 2), (102.5, 0)], [(3.5, 0), (0.33, 4), (1.05, 2), (104.88, 1)], [(100, 2)], [(1.3, 1), (101.3, 3)],
    #      [(1.5, 3), (0.73, 0), (102.23, 4)]]
    # x = [1.0, 2.0, 3.0, 4.0, 5.0]
    # b = [6.0, 7.0, 8.0, 9.0, 1.0]
    # n = 5
    x = Gauss_Seidel(A, b, x, n, k_max)
    norm_solution(A, x, b, n)


if __name__ == "__main__":
    main()
