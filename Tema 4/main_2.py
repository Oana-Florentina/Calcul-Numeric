import re
import sys

import numpy as np

epsilon = 10 ** (-5)


def extract_data(file_path):
    pattern = r'(-?[\d.]+)\s*,\s*(\d+)\s*,\s*(\d+)'
    element_list = []
    try:
        with open(file_path, "r") as f:
            n = int(f.readline().strip())
            for line in f:
                matches = re.match(pattern, line.strip())
                if matches:
                    num_1 = float(matches.group(1))
                    num_2 = int(matches.group(2))
                    num_3 = int(matches.group(3))
                    element_list.append((num_2, num_3, num_1))
    except Exception as e:
        print(f"Errordc: {e}")
    return n, element_list

def create_vectors(n, element_list):
    element_list.sort()
    values = []
    ind_col = []
    row_start = [0] * (n + 1)

    current_row = 0
    for line, column, value in element_list:
        values.append(value)
        ind_col.append(column)
        for row in range(current_row, line):
            row_start[row + 1] = len(values)
        current_row = line

    row_start[-1] = len(values)

    return values, ind_col, row_start


def main():
    n, element_list = extract_data("a_1.txt")
    values, ind_col, row_start = create_vectors(n, element_list)
    # print("values:", values)
    print("ind_col:", ind_col)
    print("row_start:", row_start)


if __name__ == "__main__":
    main()