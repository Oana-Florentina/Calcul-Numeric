import unittest
import math

from Tema_1.bonus import sin_S, cos_S
from Tema_1.exercitiul1 import find_u
from Tema_1.exercitiul2 import verify_operation_plus, verify_operation_multiply
from Tema_1.exercitiul3 import T_4, T_5, T_6, T_7, T_8, T_9, return_top


class TestFunctions(unittest.TestCase):
    def test_u(self):
        u = find_u()
        self.assertNotEqual(u+1, 1)

    def test_verify_operation_plus(self):
        result = verify_operation_plus()
        self.assertTrue(result, "The result of the addition operation should not be equal.")

    def test_verify_operation_multiply(self):
        result = verify_operation_multiply(0.4, 0.2, 0.3)
        self.assertTrue(result, "The result of the multiplication operation should not be equal.")

    def test_T_4(self):
        self.assertAlmostEqual(T_4(0.5), math.tan(0.5))

    def test_T_5(self):
        self.assertAlmostEqual(T_5(0.5), math.tan(0.5))

    def test_T_6(self):
        self.assertAlmostEqual(T_6(0.5), math.tan(0.5))

    def test_T_7(self):
        self.assertAlmostEqual(T_7(0.5), math.tan(0.5))

    def test_T_8(self):
        self.assertAlmostEqual(T_8(0.5), math.tan(0.5))

    def test_T_9(self):
        self.assertAlmostEqual(T_9(0.5), math.tan(0.5))

    def test_return_top(self):
        hierarchy = return_top()
        expected_hierarchy = ['T_9', 'T_8', 'T_7', 'T_6', 'T_5', 'T_4']
        self.assertEqual(hierarchy, expected_hierarchy)

    def test_sin_S(self):
        result = sin_S(T_4, math.pi / 4)
        self.assertAlmostEqual(result, math.sin(math.pi / 4))

    def test_cos_S(self):
        result = cos_S(T_4, math.pi / 4)
        self.assertAlmostEqual(result, math.cos(math.pi / 4))


if __name__ == '__main__':
    unittest.main()
