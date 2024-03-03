
import math
import random
import numpy as np
def calculate_p_q(A):
    n = len(A)
    p = 0
    q = 0
    max = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[i][j]) > max:
                max = abs(A[i][j])
                p = i
                q = j
    return p, q

def is_not_diagonal(A):
    n = len(A)
    for i in range(n):
        for j in range(n):
            if i != j and A[i][j] != 0:
                return True
    return False


# Algoritmul Jacobi

k_max =100
def jacobi(A, epsilon):
  k = 0
  U = np.identity(len(A))
  p, q = calculate_p_q(A)
  n = len(A)
  alpha = (A[p][p] - A[q][q]) / (2 * A[p][q])
  if alpha >= 0:
    t = -alpha + math.sqrt(1 + alpha ** 2)
  else:
    t = -alpha - math.sqrt(1 + alpha ** 2)
  c = 1 / math.sqrt(1 + t ** 2)
  s = t / math.sqrt(1 + t ** 2)
  while k <= k_max and is_not_diagonal(A):
      for j in range (1, n):
          if j != p and j != q:
                A[p][j] = c * A[p][j] + s * A[q][j]
                A[q][j] = -s * A[j][p] + c * A[q][j]
                A[j][p] = A[p][j]
                A[p][p] = A[p][p] + t * A[p][q]
                A[q][q] = A[q][q] - t * A[p][q]
                A[p][q] = 0


def generate_symmetric_matrix(n):
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            A[i][j] = random.randint(1, 10)
            A[j][i] = A[i][j]
    return A


def main():
    n = 5
    epsilon = 10 ** (-9)
    A_init = generate_symmetric_matrix(n)
    print("Initial A:", A_init)




if __name__ == "__main__":
    main()




