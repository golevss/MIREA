import numpy as np

def print_table(table, basis, columns, iteration):
    print(f"\n{'='*50}\nИтерация {iteration}\n{'='*50}")
    header = ["base"] + columns
    rows = []

    for i in range(len(table)-1):
        row = [basis[i]] + [f"{val:.2f}" if abs(val) >= 0.01 else "0.00" for val in table[i]]
        rows.append(row)
    rows.append(["f"] + [f"{val:.2f}" for val in table[-1]])
    
    for row in [header] + rows:
        print("{: >8} | {: >8} | {: >8} | {: >8} | {: >8} | {: >8} | {: >8} | {: >8} | {: >12}".format(*row))

def simplex_method():
    num_vars = 4
    num_slack = 3
    columns = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'A']
    basis = ['x5', 'x6', 'x7']
    iteration = 0

    table = np.array([
        [2, 1, 0.5, 4, 1, 0, 0, 3400],
        [1, 5, 3, 0, 0, 1, 0, 1200],
        [3, 0, 6, 1, 0, 0, 1, 3000],
        [-7.5, -3, -6, -12, 0, 0, 0, 0]
    ], dtype=float)

    print_table(table, basis, columns, 0)

    while True:
        z_row = table[-1, :-1]
        if all(z_row >= 0):
            break
        entering_col = np.argmin(z_row)
        print(f"\nВводимая в базис переменная: {columns[entering_col]}")

        ratios = []
        for row in table[:-1]:
            if row[entering_col] > 0:
                ratios.append(row[-1] / row[entering_col])
            else:
                ratios.append(np.inf)
        exiting_row = np.argmin(ratios)
        print(f"Выводимая из базиса переменная: {basis[exiting_row]}")

        
        pivot = table[exiting_row, entering_col]
        print(pivot)
        table[exiting_row] = table[exiting_row] / pivot
        for i in range(len(table)):
            if i != exiting_row:
                factor = table[i, entering_col]
                table[i] -= factor * table[exiting_row]

        basis[exiting_row] = columns[entering_col]

        print_table(table, basis, columns, iteration)
        iteration += 1

    for var, val in zip(basis, table[:-1, -1]):
        print(f"{var}: {val:.2f}")
    print(f"Максимальная прибыль: {table[-1, -1]:.2f} ден. ед.")

simplex_method()