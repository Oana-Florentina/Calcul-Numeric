from exercitiul1 import find_u
from decimal import Decimal, getcontext


def verify_operation_plus():

    x = 1.0
    u = find_u()
    y = u / 10
    z = u / 10
    result1 = (x + y) + z
    result2 = x + (y + z)
    print("Rezultatul 1:", result1)
    print("Rezultatul 2:", result2)
    return result1 != result2


print(verify_operation_plus())


def verify_operation_multiply(x, y, z):
    return (x * y) * z != x * (y * z)

print(verify_operation_multiply(0.4, 0.2, 0.3))
