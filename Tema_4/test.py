import unittest
from io import StringIO

from Tema_6.main import progressive_newton_interpolation
from main import *

class MyTestCase(unittest.TestCase):
    def test_check_diagonal(self):
        A = [
            [(2, 2), (102.5, 0)],
            [(3.5, 0), (0.33, 3), (1.05, 1), (104.88, 0)],
            [(100, 2)],
            [(1.3, 0), (101.3, 3)],
            [(1.5, 1), (0.73, 3), (102.23, 4)]
        ]
        n = 5
        result = check_diagonal(A, n)
        self.assertTrue(result)
    def test_calculate_norm_error(self):
        x = [1, 2, 3]
        old_x = [4, 5, 6]
        result = calculate_norm_error(x, old_x)
        expected_result = 9
        self.assertEqual(result, expected_result)
    def test_verify_matrix_is_empty(self):
        A = [[] for _ in range(5)]
        result = verify_matrix_is_empty(A)
        expected_result = "Matrix has the same elements. AB == A + B"
        self.assertEqual(result, expected_result)

    def test_norm(self):
        k_max = 30000
        norm_error_max = 10 ** 60
        A = [[(2.5, 2), (102.5, 0)], [(3.5, 0), (0.33, 4), (1.05, 2), (104.88, 1)], [(100, 2)], [(1.3, 1), (101.3, 3)],
             [(1.5, 3), (0.73, 0), (102.23, 4)]]
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        b = [6.0, 7.0, 8.0, 9.0, 1.0]
        n = 5
        x = Gauss_Seidel(A, b, x, n, k_max, norm_error_max)
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
        self.assertTrue(norm < epsilon, "The result is not as expected.")


if __name__ == '__main__':
    unittest.main()
