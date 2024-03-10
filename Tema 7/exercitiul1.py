from random import random
import random
import numpy as np

epsilon = 10 ** (-5)


# Muller
def choose_x1_x2_x3():
    return random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)


def gen_pol(n):
    coefficients = [random.uniform(-10, 10) for _ in range(n)]
    while coefficients[0] == 0:
        coefficients[0] = random.uniform(-10, 10)
    return coefficients


def P(a, v, n):
    # with Horner's method
    b = a[0]
    for i in range(1, n):
        b = b * v + a[i]
    return b


def Muller(coef, n):
    x_0, x_1, x_2 = choose_x1_x2_x3()
    k = 2
    while True:
        h0 = x_1 - x_0
        h1 = x_2 - x_1
        delta0 = (P(coef, x_1, n) - P(coef, x_0, n)) / h0
        delta1 = (P(coef, x_2, n) - P(coef, x_1, n)) / h1
        a = (delta1 - delta0) / h1 + h0
        b = a * h1 + delta1
        c = P(coef, x_2, n)
        if b * b - 4 * a * c < 0:
            return
        if max(abs(b + np.sqrt(b * b - 4 * a * c)), (b - np.sqrt(b * b - 4 * a * c))) < epsilon:
            return
        deltax = 2 * c / max(b + np.sqrt(b * b - 4 * a * c), b - np.sqrt(b * b - 4 * a * c))
        x_3 = x_2 - deltax
        k += 1
        x_0 = x_1
        x_1 = x_2
        x_2 = x_3
        if abs(deltax) > epsilon and k < 1000 and abs(deltax) < 10 ** 8:
            break

    if (abs(deltax) < epsilon):
        print("x:", x_2)
        print("convergenta")
        print("norm_error:", deltax)
    else:
        print("divergenta")
        print("norm_error:", deltax)


def main():
    n = 3
    a = gen_pol(n)
    x = Muller(a, n)
    while x == -1:
        a = gen_pol(n)
        x = Muller(a, n)



if __name__ == "__main__":
    main()