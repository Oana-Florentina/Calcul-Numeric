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


def function_2(x):
    return -23 * x ** 2 + 20 * x + 50


def least_squares_method(f, a, b, n, m, x_):
    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    print("x= ", x)
    print("h= ", h)
    # y = [f(x[i]) for i in range(n + 1)]
    y = [50, 47, -2, -121, -310, -545]

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
    print("With Horner P(x)= ", d)


if __name__ == "__main__":
    print("Progressive Newton interpolation")
    x_list = [0, 1, 2, 3, 4, 5]
    fx_list = [50, 47, -2, -121, -310, -545]
    x = 1.5

    # x_list = [0, 2, 4, 6]
    # fx_list = [1, -3, 49, 253]
    # x=1

    print("L_n(x) =", progressive_newton_interpolation(x_list, fx_list, x))

    # a = 1
    # b = 5
    # n = 4
    # m = 4
    # x_ = 3
    # c = least_squares_method(function_1, a, b, n, m, x_)
    # horner_method(c, x_)

    a = 0
    b = 5
    n = 5
    m = 2
    x_ = 1.5
    c = least_squares_method(function_2, a, b, n, m, x_)
    horner_method(c, x_)
