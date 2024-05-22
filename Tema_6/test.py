import unittest

from main import *

epsilon = 1e-5
class MyTestCase(unittest.TestCase):
    def test_progressive_newton_interpolation(self):
        x_list = [0, 1, 2, 3, 4, 5]
        fx_list = [50, 47, -2, -121, -310, -545]
        x = 1.5
        result = progressive_newton_interpolation(x_list, fx_list, x)
        expected_result = 30.3125
        self.assertAlmostEqual(result, expected_result)

    def test_difference(self):
        a = 0
        b = 5
        n = 5
        m = 5
        x_ = 1.5
        h = (b - a) / n
        x = [a + i * h for i in range(n + 1)]
        y = [function_1(x[i]) for i in range(n + 1)]
        c = least_squares_method(n, m, x_, x, y)

        difference = sum(abs(horner_method(c, x_el) - function_1(x_el)) for x_el in x)
        self.assertTrue(difference < epsilon, "The result is not as expected.")

    def test_result(self):
        a = 0
        b = 5
        n = 5
        m = 5
        x_ = 1.5
        h = (b - a) / n
        x = [a + i * h for i in range(n + 1)]
        y = [function_1(x[i]) for i in range(n + 1)]
        c = least_squares_method(n, m, x_, x, y)
        result = horner_method(c, x_)
        difference = abs(result - function_1(x_))
        self.assertTrue(difference < epsilon, "The result is not as expected.")

    def test_horner_method(self):
        c = [5, -3, 2, -1]
        x_ = 2.5
        result_without_horner = sum(c[i] * x_ ** i for i in range(len(c)))
        result_with_horner = horner_method(c, x_)
        self.assertAlmostEqual(result_without_horner, result_with_horner)

if __name__ == '__main__':
    unittest.main()
