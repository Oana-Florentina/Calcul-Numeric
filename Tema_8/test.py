import unittest
from main import *

epsilon = 10 ** (-5)
class MyTestCase(unittest.TestCase):
    def test_algorithm_with_approximate_gradient(self):
        x, y = 2, 3
        learning_rate = 10 ** (-3)

        max_k = 300000
        max_p = 8
        result = algorithm(function_1, approximate_gradient, x, y, learning_rate, max_k, max_p, 1, 10 ** 10)

        # Assert if the result contains "converged" indicating successful convergence
        self.assertIn("converged", result.lower())

    def test_algorithm_with_analytic_gradient(self):
        x, y = 2, 3  # Example initial values
        learning_rate = 10 ** (-3)

        max_k = 300000
        max_p = 8
        result = algorithm(function_4, analytic_gradient, x, y, learning_rate, max_k, max_p, 2, 10 ** 10)
        # Assert if the result contains "converged" indicating successful convergence
        self.assertIn("diverge", result.lower())

if __name__ == '__main__':
    unittest.main()
