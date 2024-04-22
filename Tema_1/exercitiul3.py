import random
import math
from queue import PriorityQueue


def T_4(a: float) -> float:
    return (105 * a - 10 * (a ** 3)) / (105 - 45 * (a ** 2) + a ** 4)


def T_5(a: float) -> float:
    return (945 * a - 105 * (a ** 3) + a ** 5) / (945 - 420 * (a ** 2) + 15 * (a ** 4))


def T_6(a: float) -> float:
    return (10395 * a - 1260 * (a ** 3) + 21 * (a ** 5)) / (10395 - 4725 * (a ** 2) + 210 * (a ** 4) - a ** 6)


def T_7(a: float) -> float:
    return (135135 * a - 17325 * (a ** 3) + 378 * (a ** 5) - a ** 7) / (
            135135 - 62370 * (a ** 2) + 3150 * (a ** 4) - 28 * (a ** 6))


def T_8(a: float) -> float:
    return (2027025 * a - 270270 * (a ** 3) + 6930 * (a ** 5) - 36 * (a ** 7)) / (
            2027025 - 945945 * (a ** 2) + 51975 * (a ** 4) - 630 * (a ** 6) + a ** 8)


def T_9(a: float) -> float:
    return (34459425 * a - 4729725 * (a ** 3) + 135135 * (a ** 5) - 990 * (a ** 7) + a ** 9) / (
            34459425 - 16216200 * (a ** 2) + 945945 * (a ** 4) - 13860 * (a ** 6) + 45 * (a ** 8))
def error_function(T_x, a):
    v_exact = math.tan(a)
    return abs(T_x(a) - v_exact)


list_of_functions = [T_4, T_5, T_6, T_7, T_8, T_9]

frequency = {"T_4": 0,
             "T_5": 0,
             "T_6": 0,
             "T_7": 0,
             "T_8": 0,
             "T_9": 0
              }


def best_functions():
    lower_bound = -math.pi / 2
    upper_bound = math.pi / 2
    for _ in range(1000):
        pq = PriorityQueue()
        random_number = random.uniform(lower_bound, upper_bound)
        for function in list_of_functions:
            pq.put((error_function(function, random_number), f"{function.__name__}"))

        # print("-----------------")
        while not pq.empty():
            priority, item = pq.get()
            global frequency
            frequency[item] += priority


def return_top():
        return hierarchy
# pt fiecare x, aplic t4..6, calculez eroarea pt fiecare si returnez top3

if __name__ == "__main__":
    best_functions()
    hierarchy = sorted(frequency, key=frequency.get)
    print(frequency)
    print(hierarchy)