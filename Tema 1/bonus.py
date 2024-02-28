import math

from exercitiul3 import list_of_functions


def sin_S(T_x, a):
    return T_x(a) / math.sqrt(1 + (T_x(a) ** 2))


def cos_S(T_x, a):
    return 1 / math.sqrt(1 + (T_x(a) ** 2))


def approximations(f, a):
    for function in list_of_functions:
        print(f"n = {function.__name__[2]} ", f(function, a))


print("Sinus:")
approximations(sin_S, 30)
print("Cosinus:")
approximations(cos_S, 30)
