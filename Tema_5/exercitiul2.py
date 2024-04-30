import numpy as np
import scipy.linalg as cholesky


def process_this(A):
    epsilon = 10 ** (-5)

    k = 0
    result = ""
    result+= "K: " + str(k) + "\n"
    result+= "A: " + str(A) + "\n"
    k_max = 10000
    try:
        if not is_positive_definite(A):
            raise ValueError("Matricea nu este pozitiv definită.")

        L = cholesky.cholesky(A)
        result += "L: " + str(L) + "\n"

        while np.linalg.norm(A - L @ L.T) > epsilon or k > k_max:
            k += 1
            A = L @ L.T
            L = cholesky.cholesky(A)
            result += "A: " + str(A) + "\n"
            print()
            result += "K: " + str(k) + "\n"
    except np.linalg.LinAlgError as e:
        print("A apărut o eroare în timpul calculului factorizării Cholesky:", e)
        return
    except ValueError as e:
        print(e)
        return

    print()
    norma = np.linalg.norm(A - L @ L.T)
    return result, norma



def main():
    A = generate_positive_definite_matrix(3)
    process_this(A)


def generate_positive_definite_matrix(n):
    A = np.random.rand(n, n)
    A = 0.5 * (A + A.T)
    A += np.eye(n) * n
    positive_definite_matrix = np.dot(A, A.T)
    return positive_definite_matrix


def is_positive_definite(A):
    return np.all(np.linalg.eigvals(A) > 0)


if __name__ == "__main__":
    main()

# matricea este simetrica, diagonala, pozitiv definita