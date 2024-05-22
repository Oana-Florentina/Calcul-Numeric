import unittest
import numpy as np
from exercitiul import *

class TestFunctions(unittest.TestCase):

    def test_inverse_with_qr(self):
        n = 3
        s = [3, 2, 1]
        A = [[0, 0, 4], [1, 2, 3], [0, 1, 2]]
        A_init = np.copy(A)
        b = calculate_vector(A, n, s)
        Q, R, b = QR(A, n, b)
        inverse_qr = inverse_with_qr(Q, R)
        inverse_library = np.linalg.inv(A_init)
        self.assertTrue(np.allclose(inverse_qr, inverse_library), "The result of inverse_with_qr is not as expected.")

    def test_calculate_svd(self):
        A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        U, S, VT = calculate_svd(A)
        self.assertEqual(U.shape, (3, 3))
        self.assertEqual(S.shape, (3,))
        self.assertEqual(VT.shape, (3, 3))

    def test_QR(self):
        n = 3
        s = [3, 2, 1]
        A = [[0, 0, 4], [1, 2, 3], [0, 1, 2]]
        b = calculate_vector(A, n, s)
        b_init = np.copy(b)
        Q, R, _ = QR(A, n, b)
        X_house = solve_system(R, n, np.dot(Q.T, b_init))
        x_QR = find_x_qr_with_lib(A, n, b)
        self.assertTrue(np.allclose(x_QR, s), "The result of find_x_qr_with_lib is not as expected.")
        self.assertTrue(np.allclose(X_house, s), "The result of solve_system is not as expected.")

    def test_norms(self):
        n = 3
        s = [3, 2, 1]
        A = [[0, 0, 4], [1, 2, 3], [0, 1, 2]]
        A_init = np.copy(A)
        b = calculate_vector(A, n, s)
        b_init = np.copy(b)
        Q, R, _ = QR(A, n, b)
        X_house = solve_system(R, n, np.dot(Q.T, b_init))
        x_QR = find_x_qr_with_lib(A, n, b)

        # norm between A_init * X_house and b_init
        prod = np.dot(np.array(A_init), np.array(X_house))
        self. assertAlmostEqual(np.linalg.norm(prod - np.array(b_init)), 0)

        # norm between A_init * x_QR and b_init
        prod = np.dot(np.array(A_init), np.array(x_QR))
        self. assertAlmostEqual(np.linalg.norm(prod - np.array(b_init)), 0)

   

if __name__ == '__main__':
    unittest.main()