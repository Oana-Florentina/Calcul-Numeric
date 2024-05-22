import unittest
import numpy as np
from copy import deepcopy

epsilon = 10 ** (-5)

from main import (
    validation_matrix,
    LU_decomposition,
    determinant,
    forward_substitution,
    backward_substitution,
    verify_euclidian_norm,
    solve_equation,
    LU_decomposition_2,
    generate_matrix,
    generate_vector_s
)

class TestMatrixOperations(unittest.TestCase):

    def setUp(self):
        self.A_init = [[2.5, 2, 2], [5, 6, 5], [5, 6, 6.5]]
        self.b = [2, 2, 2]
        self.n = len(self.A_init)

    def test_validation_matrix(self):
        self.assertTrue(validation_matrix(self.A_init))
        self.assertFalse(validation_matrix([[1, 2], [3]]))  # Non-square matrix

    def test_LU_decomposition(self):
        A = deepcopy(self.A_init)
        result = LU_decomposition(A, self.A_init, self.n)
        self.assertNotEqual(result, "Matrix cannot be decomposed")
        self.assertNotEqual(result, "Matrix is not valid")

    def test_determinant(self):
        A = deepcopy(self.A_init)
        LU_decomposition(A, self.A_init, self.n)
        det = determinant(A)
        expected_det = np.linalg.det(np.array(self.A_init))
        self.assertAlmostEqual(det, expected_det, places=5)

    def test_forward_substitution(self):
        A = deepcopy(self.A_init)
        LU_decomposition(A, self.A_init, self.n)
        y = forward_substitution(A, self.n, self.b)
        self.assertNotEqual(y, "Matrix is not valid")

    def test_backward_substitution(self):
        A = deepcopy(self.A_init)
        LU_decomposition(A, self.A_init, self.n)
        y = forward_substitution(A, self.n, self.b)
        x = backward_substitution(A, self.n, y)
        self.assertNotEqual(x, "Matrix is not valid")

    def test_verify_euclidian_norm(self):
        A = deepcopy(self.A_init)
        LU_decomposition(A, self.A_init, self.n)
        y = forward_substitution(A, self.n, self.b)
        x = backward_substitution(A, self.n, y)
        verify_euclidian_norm(self.A_init, x, self.b)
        norm = np.linalg.norm(np.dot(np.array(self.A_init), np.array(x)) - np.array(self.b))
        self.assertLessEqual(norm, 10 ** (-8))

    def test_solve_equation(self):
        A = deepcopy(self.A_init)
        LU_decomposition(A, self.A_init, self.n)
        y = forward_substitution(A, self.n, self.b)
        x = backward_substitution(A, self.n, y)
        result = solve_equation(self.A_init, self.b, x)
        self.assertIn("x_lib:", result)

    def test_LU_decomposition_2(self):
        L, U = LU_decomposition_2(self.A_init, self.n)
        self.assertIsInstance(L, list)
        self.assertIsInstance(U, list)

    def test_generate_matrix(self):
        matrix = generate_matrix(self.n)
        self.assertEqual(len(matrix), self.n)
        self.assertEqual(len(matrix[0]), self.n)

    def test_generate_vector_s(self):
        vector = generate_vector_s(self.n)
        self.assertEqual(len(vector), self.n)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
