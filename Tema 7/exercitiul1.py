from random import random
import random
import numpy as np

epsilon = 10 ** (-4)


# Muller
def choose_x1_x2_x3(R):
    return random.uniform(-R, R), random.uniform(-R, R), random.uniform(-R, R)


def gen_pol(n):
    coefficients = [random.uniform(-10, 10) for _ in range(n)]
    while coefficients[0] == 0:
        coefficients[0] = random.uniform(-10, 10)
    return coefficients


def P(a, v, n):
    b = a[0]
    for i in range(1, n):
        b = b * v + a[i]
    return b


def sign(x):
    if x <= 0:
        return -1
    return 1


def Muller(coef, n, R):
    x_0, x_1, x_2 = choose_x1_x2_x3(R)
    k = 2
    deltax = epsilon + 1
    while True:
        h0 = x_1 - x_0
        h1 = x_2 - x_1
        delta0 = (P(coef, x_1, n) - P(coef, x_0, n)) / h0
        delta1 = (P(coef, x_2, n) - P(coef, x_1, n)) / h1
        a = (delta1 - delta0) / (h1 + h0)
        b = a * h1 + delta1
        c = P(coef, x_2, n)
        if (b * b - 4 * a * c) < 0:
            break

        if abs(b + sign(b) * np.sqrt(b * b - 4 * a * c)) < epsilon:
            break
        deltax = (2.0 * c) / abs(b + sign(b) * np.sqrt(b * b - 4 * a * c))
        x_3 = x_2 - deltax
        k += 1
        x_0 = x_1
        x_1 = x_2
        x_2 = x_3
        if abs(deltax) < epsilon or k > 10000 or abs(deltax) > 10 ** 8:
            break
    if (abs(deltax) < epsilon):
        print("x_2:", x_2)
        #  print("convergenta")

        return x_2

    else:
        # print("divergenta")

        return Muller(coef, n, R)


def Calculate_Roots(coef, n):
    A = -999
    for i in range(n):
        if abs(coef[i]) > A:
            A = abs(coef[i])
    R = abs(coef[0] + A) / coef[0]
    return R


def check_solution(x_2, sol, epsilon):
    for i in range(len(sol)):
        if abs(x_2 - sol[i]) < epsilon:
            return False
    return True


def save_solution(sol):
    with open("solution_test.txt", "w") as file:
        file.write(str(sol))


def main():
    n = 4
    a = [1, -6, 11, -6]
    a = gen_pol(n)
    print("a:", a)
    R = Calculate_Roots(a, n)

    sol = []
    x_2 = Muller(a, n, R)
    sol.append(x_2)
    i = 1
    while i < 15 * n:
        x_2 = Muller(a, n, R)
        if check_solution(x_2, sol, epsilon):
            sol.append(x_2)
        i += 1

    print("sol:", sol)
    save_solution(sol)
    print("roots:", -R, R)


if __name__ == "__main__":
    main()
