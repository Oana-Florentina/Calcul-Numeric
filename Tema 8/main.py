import math
import random

import numpy as np

h = 10 ** (-6)
epsilon = 10 ** (-8)


def function_1(x, y):
    return x ** 2 + y ** 2 - 2 * x - 4 * y - 1


def function_1_analytic_gradient(x, y):
    return 2 * x - 2, 2 * y - 4


def function_2(x, y):
    return 3 * x ** 2 - 12 * x + 2 * y ** 2 + 16 * y - 10


def function_2_analytic_gradient(x, y):
    return 6 * x - 12, 4 * y + 16


def function_3(x, y):
    return x ** 2 - 4 * x * y + 5 * y ** 2 - 4 * y + 3


def function_3_analytic_gradient(x, y):
    return 2 * x - 4 * y, (-4) * x + 10 * y - 4


def function_4(x, y):
    return x * y ** 2 - 2 * x * y ** 2 + 3 * x * y + 4


def function_4_analytic_gradient(x, y):
    return 2 * x * y - 2 * y ** 2 + 3 * y, x ** 2 - 4 * x * y + 3 * x


analytic_gradient_dictionary = {function_1: function_1_analytic_gradient,
                                function_2: function_2_analytic_gradient,
                                function_3: function_3_analytic_gradient,
                                function_4: function_4_analytic_gradient}


def analytic_gradient(f, x, y):
    return analytic_gradient_dictionary[f](x, y)


def approximate_gradient(f, x, y):
    G_1 = 3 * f(x, y) - 4 * f(x - h, y) + f(x - 2 * h, y)
    G_1 /= 2 * h

    G_2 = 3 * f(x, y) - 4 * f(x, y - h) + f(x, y - 2 * h)
    G_2 /= 2 * h

    return G_1, G_2


def calculate_norm_2(G_1, G_2):
    return G_1 ** 2 + G_2 ** 2


def condition_learning_rate(operation_1, operation_2, learning_rate, norm, p):
    if p >= 8:
        return False

    # f(x - G_1, y - G_2) > f(x, y) - learning_rate * 0.5 * calculate_norm_2(G_1, G_2)
    return operation_1 > operation_2 - learning_rate * 0.5 * norm


def find_learning_rate_1(learning_rate):
    return learning_rate / 1


def find_learning_rate_2(f, x, y, G_1, G_2):
    # f(x-G_1, y-G_2)
    operation_1 = f(x - G_1, y - G_2)
    # f(x, y)
    operation_2 = f(x, y)
    norm = np.linalg.norm([G_1, G_2], ord=2) ** 2

    learning_rate = 1
    p = 1
    beta = 0.8
    while condition_learning_rate(operation_1, operation_2, learning_rate, norm, p):
        learning_rate *= beta
        p += 1

    return learning_rate


def divergence_condition(k, learning_rate, G_1, G_2):
    norm = np.linalg.norm([G_1, G_2], ord=2)

    product = learning_rate * norm
    if k > 300000 or product < epsilon or product > 10 ** 10:
        return product, True
    return product, False


def choose_values(start, end):
    x, y = random.uniform(start, end), random.uniform(start, end)
    print(f"Initial point: ({x}, {y})")
    return x, y


def algorithm(f, gradient_function, x, y):
    k = 0
    learning_rate = 10 ** (-1)
    while True:
        G_1, G_2 = gradient_function(f, x, y)
        # print(f"{gradient_function.__name__}: ", G_1, G_2)

        learning_rate = find_learning_rate_2(f, x, y, G_1, G_2)
        # learning_rate = find_learning_rate_1(learning_rate)
        # print("Learning rate:", learning_rate)

        x -= learning_rate * G_1
        y -= learning_rate * G_2
        k += 1

        product, divergence = divergence_condition(k, learning_rate, G_1, G_2)
        if divergence:
            # print("Divergence condition met")
            print("Number of iterations:", k)
            break

    if product <= epsilon:
        print("converged")
        print("x:", x)
        print("y:", y)
    else:
        print("Divergence condition met")


if __name__ == "__main__":
    x, y = choose_values(-10, 10)
    learning_rate = 10 ** (-1)
    epsilon = 10 ** (-8)
    max_k = 30000
    max_p = 8
    print("Approximate gradient:")
    algorithm(function_3, approximate_gradient, x, y)
    print()

    print("Analytic gradient:")
    algorithm(function_3, analytic_gradient, x, y)
    print()
