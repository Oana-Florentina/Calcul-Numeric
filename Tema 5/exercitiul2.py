import numpy as np
import scipy.linalg as cholesky


def main():
    epsilon = 10 ** (-5)

    # Generăm o matrice pozitiv definită
    A = generate_positive_definite_matrix(3)

    k = 0
    print("K:", k)
    print("A:", A)

    try:
        # Verificăm dacă matricea este pozitiv definită
        if not is_positive_definite(A):
            raise ValueError("Matricea nu este pozitiv definită.")

        # Calculăm factorizarea Cholesky
        L = cholesky.cholesky(A)
        print(L)

        # Calculăm factorizarea Cholesky
        while np.linalg.norm(A - L @ L.T) > epsilon:
            k += 1
            A = L @ L.T
            L = cholesky.cholesky(A)
            print("A:", A)
            print()
            print("K:", k)
    except np.linalg.LinAlgError as e:
        print("A apărut o eroare în timpul calculului factorizării Cholesky:", e)
        return
    except ValueError as e:
        print(e)
        return

    print()
    norma = np.linalg.norm(A - L @ L.T)
    print("Norma:", norma)

    print()


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