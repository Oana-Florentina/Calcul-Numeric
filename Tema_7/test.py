import unittest

from exercitiul1 import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.n = 5
        self.a = [42.0, -55.0, -42.0, 49.0, -6.0]
    def test_choose_x1_x2_x3(self):
        R = Calculate_Roots(self.a, self.n)
        x1, x2, x3 = choose_x1_x2_x3(R)
        self.assertTrue(-R <= x1 <= R)
        self.assertTrue(-R <= x2 <= R)
        self.assertTrue(-R <= x3 <= R)

    def test_Muller(self):
        coef = [1, -6, 11, -6]
        n = len(coef)
        R = Calculate_Roots(coef, n)
        x_2 = Muller(coef, n, R)
        result = P(coef, x_2, n)
        self.assertTrue(result < epsilon, "The result is not as expected.")

    def test_bonus(self):
        coef = [1, -6, 11, -6]
        n = len(coef)
        R = Calculate_Roots(coef, n)
        bonus_sol = helper_bonus(coef, R, n)
        for root in bonus_sol:
            result = P(coef, root, n)
            self.assertTrue(result < epsilon, "The result is not as expected.")



if __name__ == '__main__':
    unittest.main()
