import unittest
from main import *

epsilon = 10 ** (-5)
class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.functions = [function_1, function_2, function_3, function_4]
        self.analytic_gradients = {
            function_1: function_1_analytic_gradient,
            function_2: function_2_analytic_gradient,
            function_3: function_3_analytic_gradient,
            function_4: function_4_analytic_gradient
        }
        self.approximate_gradients = {
            function_1: function_1,
            function_2: function_2,
            function_3: function_3,
            function_4: function_4
        }
    def test_algorithm_with_approximate_gradient(self):
        x, y = 1, 2
        learning_rate = 10 ** (-3)
        max_k = 300000
        max_p = 8
        result = algorithm(function_1, approximate_gradient, x, y, learning_rate, max_k, max_p, 1, 10 ** 10)
        result2 = algorithm(function_2, approximate_gradient, x, y, learning_rate, max_k, max_p, 1, 10 ** 10)
        result3 = algorithm(function_3, approximate_gradient, x, y, learning_rate, max_k, max_p, 1, 10 ** 10)
        result4 = algorithm(function_4, approximate_gradient, x, y, learning_rate, max_k, max_p, 1, 10 ** 10)
        # Assert if the result contains "converged" indicating successful convergence
        self.assertIn("converged", result.lower())
        self.assertIn("converged", result2.lower())
        self.assertIn("diverge", result3.lower())
        self.assertIn("diverge", result4.lower())

    def test_algorithm_with_analytic_gradient(self):
        x, y = 2, 3  # Example initial values
        learning_rate = 10 ** (-3)
        max_k = 300000
        max_p = 8
        result = algorithm(function_3, analytic_gradient, x, y, learning_rate, max_k, max_p, 1, 10 ** 10)
        result2 = algorithm(function_4, analytic_gradient, x, y, learning_rate, max_k, max_p, 2, 10 ** 10)
        result3 = algorithm(function_1, analytic_gradient, x, y, learning_rate, max_k, max_p, 1, 10 ** 10)
        result4 = algorithm(function_2, analytic_gradient, x, y, learning_rate, max_k, max_p, 1, 10 ** 10)
        # Assert if the result contains "converged" indicating successful convergence
        self.assertIn("diverge", result.lower())
        self.assertIn("diverge", result2.lower())
        self.assertIn("converged", result3.lower())
        self.assertIn("converged", result4.lower())


if __name__ == '__main__':
    unittest.main()
