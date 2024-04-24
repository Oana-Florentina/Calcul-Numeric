import math

from .exercitiul3 import list_of_functions


def sin_S(T_x, a):
    # return T_x(a) / math.sqrt(1 + (T_x(a) ** 2))
    return (1 - T_x((2 * a - math.pi) / 4) ** 2) / (1 + T_x((2 * a - math.pi) / 4) ** 2)


def cos_S(T_x, a):
    # return 1 / math.sqrt(1 + (T_x(a) ** 2))
    return (1 - (T_x(a / 2)) ** 2) / (1 + (T_x(a / 2)) ** 2)


def approximations(f, a):
    Result = ""
    for function in list_of_functions:
        Result += "n = " + function.__name__[2] + " " + str(f(function, a)) + "\n"
        # print(f"n = {function.__name__[2]} ", f(function, a))
    return Result


def return_app_sin():
    return approximations(sin_S, math.pi / 4)


def return_app_cos():
    return approximations(cos_S, math.pi / 4)


print("Sinus:")
approximations(sin_S, math.pi / 4)
print("Cosinus:")
approximations(cos_S, math.pi / 4)
