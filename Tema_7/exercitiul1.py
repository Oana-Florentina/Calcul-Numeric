from random import random
import random
import numpy as np

epsilon = 10 ** (-3)


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
        if abs(x_2 - sol[i]) < 0.1:
            return False
    return True


def save_solution(sol, name_file):
    with open(name_file, "w") as file:
        file.write(str(sol))


def calculate_derivate_polinom(coef, n):
    derivata = [0] * (n - 1)
    for i in range(0, n - 1):
        derivata[i] = coef[i] * (n - i - 1)
    return derivata


def bonus(coef, R, n):
    x1, _, _ = choose_x1_x2_x3(R)
    derivata_coef = calculate_derivate_polinom(coef, n)

    y = x1 - (P(coef, x1, n) / P(derivata_coef, x1, n - 1))

    x2 = x1 - (((P(coef, x1, n) ** 2) + P(coef, y, n) ** 2) / (
                P(derivata_coef, x1, n - 1) * (P(coef, x1, n) - P(coef, y, n))))
    while np.linalg.norm(x1 - x2) > epsilon:
        x1 = x2
        if P(derivata_coef, x1, n - 1) < epsilon:
            return bonus(coef, R, n)
        y = x1 - (P(coef, x1, n) / P(derivata_coef, x1, n - 1))
        if (P(derivata_coef, x1, n - 1) * (P(coef, x1, n) - P(coef, y, n))) < epsilon:
            return bonus(coef, R, n)
        x2 = x1 - (((P(coef, x1, n) ** 2) + P(coef, y, n) ** 2) / (
                    P(derivata_coef, x1, n - 1) * (P(coef, x1, n) - P(coef, y, n))))
    return x2

def helper_function(a, n, R):
    sol = []
    x_2 = Muller(a, n, R)
    sol.append(x_2)
    i = 1
    while i < 30 * n:
        x_2 = Muller(a, n, R)
        if check_solution(x_2, sol, epsilon):
            sol.append(x_2)
        i += 1
    return sol
def main():
    n = 5
    a = [42.0, -55.0, -42.0, 49.0, -6.0]
    # a = gen_pol(n)
    print("a:", a)
    R = Calculate_Roots(a, n)
    sol = helper_function(a, n, R)


    print("sol:", sol)
    save_solution(sol, "sol.txt")
    print("roots:", -R, R)
    print("---------bonussssssss-------")
    bonus_sol = helper_bonus([1, -6, 11, -6], 12, 4)
    print ("bonus_sol:", bonus_sol)

def helper_bonus(coef, R, n):
    bonus_sol = []

    print("derivata:", calculate_derivate_polinom(coef, n))
    i = 0
    while i < 3000:
        x_2 = bonus(coef, R, n)
        if check_solution(x_2, bonus_sol, epsilon):
            bonus_sol.append(x_2)
        i += 1
    return bonus_sol
if __name__ == "__main__":
    main()
