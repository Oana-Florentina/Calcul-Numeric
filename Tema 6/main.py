import numpy as np


def progressive_newton_interpolation(x_list, y, x):
    n = len(y) - 1
    h = (x_list[-1] - x_list[0]) / n
    t = (x - x_list[0]) / h
    s = t
    L_n = y[0]

    for i in range(1, n + 1):
        for j in range(n, i - 1, -1):
            y[j] = y[j] - y[j - 1]

        if i > 1:
            s *= (t - i + 1) / i

        L_n += y[i] * s

    return L_n


def function_1(x):
    return x ** 4 - 12 * x ** 3 + 30 * x ** 2 + 12


def least_squares_method(n, m, x_, x, y):
    print("x= ", x)
    print("h= ", h)

    B = np.zeros((m + 1, m + 1))
    for i in range(m + 1):
        for j in range(m + 1):
            B[i, j] = sum(x[k] ** (i + j) for k in range(n + 1))
    print("B= ", B)

    f = np.zeros(m + 1)
    for i in range(m + 1):
        f[i] = sum(y[k] * x[k] ** i for k in range(n + 1))
    print("f= ", f)

    a = np.linalg.solve(B, f)
    print("a= ", a)

    print("Without Horner P(x)= ", sum(a[i] * x_ ** i for i in range(m + 1)))

    return a


def horner_method(c, x_):
    d = c[len(c) - 1]
    for i in range(len(c) - 2, -1, -1):
        d = d * x_ + c[i]
    return d


if __name__ == "__main__":
    print("Progressive Newton interpolation")
    x_list = [0, 1, 2, 3, 4, 5]
    fx_list = [50, 47, -2, -121, -310, -545]
    x = 1.5
    y_ = 30.3125
    # x_list = [0, 2, 4, 6]
    # fx_list = [1, -3, 49, 253]
    # x=1

    result = progressive_newton_interpolation(x_list, fx_list, x)
    print("L_n(x) =", result)
    print("|L_x- f(x)| =", abs(result - y_))

    a = 0
    b = 5
    n = 5
    m = 1
    x_ = 1.5
    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    y = [function_1(x[i]) for i in range(n + 1)]
    c = least_squares_method(n, m, x_, x, y)
    result = horner_method(c, x_)

    print("With Horner P(x)= ", result)

    print("|P(x)- f(x)| =", abs(result - function_1(x_)))

    difference = sum(abs(horner_method(c, x_el) - function_1(x_el)) for x_el in x)
    print("Sum of differences= ", difference)
