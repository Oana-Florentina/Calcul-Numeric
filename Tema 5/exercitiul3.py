import numpy as np

def calculate_svd(A):
    U, S, VT = np.linalg.svd(A)
    return U, S, VT

def calculate_singular_values(A):
    _, singular_values, _ = calculate_svd(A)
    return singular_values

def calculate_rank(A):
    singular_values = calculate_singular_values(A)
    rank_A = np.sum(singular_values > 1e-10)  # Consideram valorile singulare nenule
    return rank_A

def calculate_condition_number(A):
    singular_values = calculate_singular_values(A)
    max_singular_value = np.max(singular_values)
    min_singular_value = np.min(singular_values[singular_values > 1e-10])
    condition_number = max_singular_value / min_singular_value
    return condition_number

def calculate_moore_penrose_pseudoinverse(A):
    U, S, VT = calculate_svd(A)
    pseudo_inverse = np.linalg.pinv(A)
    return pseudo_inverse

def calculate_least_squares_pseudoinverse(A):
    ATA_inverse = np.linalg.inv(np.dot(A.T, A))
    pseudo_inverse_least_squares = np.dot(ATA_inverse, A.T)
    return pseudo_inverse_least_squares

def calculate_norm(A1, A2):
    return np.linalg.norm(A1 - A2, ord=1)

def main():
    A = np.array([[2.5, 5, 5],
                  [2, 6, 6],
                  [2, 5, 6.5],
                  [1, 0, 2],
                  [1, 1, 3]])

    singular_values = calculate_singular_values(A)
    print("Valorile singulare ale matricei A:", singular_values)

    rank_A = calculate_rank(A)
    print("Rangul matricei A:", rank_A)

    condition_number = calculate_condition_number(A)
    print("Numărul de condiționare al matricei A:", condition_number)

    pseudo_inverse_moore_penrose = calculate_moore_penrose_pseudoinverse(A)
    print("Pseudoinversa Moore-Penrose a matricei A:\n", pseudo_inverse_moore_penrose)

    pseudo_inverse_least_squares = calculate_least_squares_pseudoinverse(A)
    print("Matricea pseudo-inversă în sensul celor mai mici pătrate a matricei A:\n", pseudo_inverse_least_squares)

    norm_difference = calculate_norm(pseudo_inverse_moore_penrose, pseudo_inverse_least_squares)
    print(
        "Norma diferenței (pseudoinversa Moore-Penrose, matricea pseudo-inversă..mai mici pătrate):",
        norm_difference)

if __name__ == "__main__":
    main()