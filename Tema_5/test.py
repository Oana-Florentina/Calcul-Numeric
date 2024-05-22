import unittest
import numpy as np
from exercitiul1 import *
from exercitiul2 import *
from exercitiul3 import *
from bonus import *


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.A = [[0, 0, 1],
             [0, 0, 1],
             [1, 1, 1]]
        self.A_init = np.copy(self.A)
        self.n = 3

    def test_ex1(self):
        A, U = jacobi(self.A)
        A_init = np.copy(self.A)
        eigenvalues = np.diag(A)
        norm = matrix_norm(np.dot(A_init, U) - np.dot(U, np.diag(eigenvalues)))
        self.assertTrue(norm < epsilon, "The result of jacobi is not as expected.")

    def test_ex2(self):
        A = generate_positive_definite_matrix(3)
        _, norm = process_this(A)
        self.assertTrue(norm < epsilon, "The result of jacobi as expected.")

    def test_ex3(self):
        A = np.array([[2.5, 5, 5],
                      [2, 6, 6],
                      [2, 5, 6.5],
                      [1, 0, 2],
                      [1, 1, 3]])

        pseudo_inverse_moore_penrose = calculate_moore_penrose_pseudoinverse(A)
        pseudo_inverse_least_squares = calculate_least_squares_pseudoinverse(A)

        norm_difference = calculate_norm(pseudo_inverse_moore_penrose, pseudo_inverse_least_squares)
        self.assertTrue(norm_difference < epsilon, "The result is not as expected.")

    def test_bonus(self):
        A = [0, 0, 0, 1, 1, 1]
        A_init = np.copy(A)
        calculate_p_q_bonus(A)
        A, U = jacobi2(A, self.n)
        norm = calculate_eigenvalues(A_init, U, self.n
                                     )
        print_matrix_from_vector(A, self.n)
        self.assertTrue(norm < epsilon, "The result is not as expected.")

if __name__ == '__main__':
    unittest.main()