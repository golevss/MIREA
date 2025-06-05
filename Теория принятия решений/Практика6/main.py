import numpy as np
from scipy.optimize import linprog
from sympy import symbols, Eq, solve

a_primal = np.array([
    [2, 1, 0.5, 4],
    [1, 5, 3, 0],
    [3, 0, 6, 1]
])
b_primal = np.array([3400, 1200, 3000])
c_primal = np.array([7.5, 3, 6, 12])

A_dual = a_primal.T
y1, y2, y3 = symbols('y1 y2 y3')
Eqs = []
for i in range(4):
    Eqs.append(Eq(A_dual[i][0]*y1 + A_dual[i][1]*y2 + A_dual[i][2]*y3, c_primal[i]))

B_inv = np.array([
    [0.25, -0.05, 0.004],
    [0.02, 0.2, -0.09],
    [-0.04, 0.008, 0.17]
])
# Первая теорема
# =======================================
print(f"Первая теорема двойственности:")
res_primal = linprog(
    -c_primal,
    A_ub=a_primal,
    b_ub=b_primal,
    bounds=[(0, None)] * 4,
    method='highs'
)
x_opt = res_primal.x
y_opt = -res_primal.ineqlin.marginals

g = b_primal[0] * (y_opt[0]) + b_primal[1] * (y_opt[1]) + b_primal[2] * (y_opt[2])

print(f"y1 = {round(-res_primal.ineqlin.marginals[0],2)}, y2 = {round(-res_primal.ineqlin.marginals[1],2)}, y3 = {round(-res_primal.ineqlin.marginals[2],2)}")
print(f"g_min = {round(g,2)}")
print(f"Совпадение с решением прямой задачи {np.isclose(round(g,0), 11851)}")


# Вторая теорема
# =======================================
print(f"\nВторая теорема двойственности:")
lims = 0
for line in a_primal:
    check = [line[i] * x_opt[i] for i in range(4)]
    check = sum(check) > b_primal[lims]
    lims += 1

    if check:
        print(f"Невыполение условия")
        exit(0)
print(f"Ограничения прямой задачи выполняются")

fin_eqs = []
for i in range(4):
    if x_opt[i] > 0:
        fin_eqs.append(Eqs[i])
print(f"Ограничения двойственной задачи выполняются")

solutions = solve((fin_eqs), (y1, y2, y3))
g_min = b_primal[0] * (solutions[y1]) + b_primal[1] * (solutions[y2]) + b_primal[2] * (solutions[y3])

print(f"y1 = {round(solutions[y1],2)}, y2 = {round(solutions[y2],2)}, y3 = {round(solutions[y3],2)}")
print(f"g_min = {round(g_min,2)}")


# Третья теорема
# =======================================
print(f"\nТретья теорема двойственности:")

def calculate_limits(B_inv, b):
    limits = []
    for col in range(B_inv.shape[1]):
        column = B_inv[:, col]
        
        pos_mask = column > 0
        if any(pos_mask):
            delta_lower = min(b[pos_mask]/column[pos_mask])
        else:
            delta_lower = np.inf
            
        neg_mask = column < 0
        if any(neg_mask):
            delta_upper = min(b[neg_mask]/abs(column[neg_mask]))
        else:
            delta_upper = np.inf
            
        limits.append((b[col] - delta_lower, b[col] + delta_upper))
    return limits

def calculate_max_Z(y_opt, limits, Z_original):
    delta_Z = 0
    for i in range(len(y_opt)):
        if y_opt[i] > 1e-6:
            delta_b = limits[i][1] - b_primal[i]
            delta_Z += y_opt[i] * delta_b
    return Z_original + delta_Z

resource_limits = calculate_limits(B_inv, b_primal)
Z_max = calculate_max_Z(y_opt, resource_limits, g_min)

print("\nИнтервалы устойчивости ресурсов:")
i = 3
for (lower, upper) in resource_limits:
    print(f"Ресурс {i}: ({lower:.2f}, {upper:.2f})")
    i -= 1    

print("\nВценим влияние изменения объема ресурсов")
for i in range(len(b_primal)):
    if y_opt[i] > 1e-6:
        print(f"При b_{i+1}={resource_limits[i][1]:.2f}: Z={y_opt[i]*(resource_limits[i][1]-b_primal[i]):.2f}")
print(f"\nМаксимальное значение целевой функции: {Z_max:.2f}")

