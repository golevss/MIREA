import pandas as pd
import numpy as np


all_crit = pd.DataFrame([
    {"K1": 1,"K2": 1/7,"K3": 3,"K4": 2,"K5": 2},
    {"K1": 7,"K2": 1,"K3": 3,"K4": 5,"K5": 5},
    {"K1": 1/3,"K2": 1/3,"K3": 1,"K4": 1,"K5": 1},
    {"K1": 1/2,"K2": 1/5,"K3": 1,"K4": 1,"K5": 3},
    {"K1": 1/2,"K2": 1/5,"K3": 1,"K4": 1/3,"K5": 1},
])  

crit1 = pd.DataFrame([
    {"A1": 1,"A2": 3,"A3": 3,"A4": 5,"A5": 5},
    {"A1": 1/3,"A2": 1,"A3": 3,"A4": 5,"A5": 5},
    {"A1": 1/3,"A2": 1/3,"A3": 1,"A4": 5,"A5": 3},
    {"A1": 1/5,"A2": 1/5,"A3": 1/5,"A4": 1,"A5": 1},
    {"A1": 1/5,"A2": 1/5,"A3": 1/3,"A4": 1,"A5": 1},
])

crit2 = pd.DataFrame([
    {"A1": 1,"A2": 1/3,"A3": 1/3,"A4": 1/5,"A5": 1/3},
    {"A1": 3,"A2": 1,"A3": 1/3,"A4": 1/3,"A5": 1/5},
    {"A1": 3,"A2": 3,"A3": 1,"A4": 1,"A5": 1},
    {"A1": 5,"A2": 3,"A3": 1,"A4": 1,"A5": 1},
    {"A1": 3,"A2": 5,"A3": 1,"A4": 1,"A5": 1},
])

crit3 = pd.DataFrame([
    {"A1": 1,"A2": 1,"A3": 3,"A4": 5,"A5": 5},
    {"A1": 1,"A2": 1,"A3": 1,"A4": 5,"A5": 5},
    {"A1": 1/3,"A2": 1,"A3": 1,"A4": 3,"A5": 3},
    {"A1": 1/5,"A2": 1/5,"A3": 1/3,"A4": 1,"A5": 1},
    {"A1": 1/5,"A2": 1/5,"A3": 1/3,"A4": 1,"A5": 1},
])

crit4 = pd.DataFrame([
    {"A1": 1,"A2": 3,"A3": 1,"A4": 1,"A5": 1},
    {"A1": 1/3,"A2": 1,"A3": 1/3,"A4": 1/3,"A5": 1/3},
    {"A1": 1,"A2": 1/3,"A3": 1,"A4": 1,"A5": 1},
    {"A1": 1,"A2": 1/3,"A3": 1,"A4": 1,"A5": 1},
    {"A1": 1,"A2": 1/3,"A3": 1,"A4": 1,"A5": 1},
])

crit5 = pd.DataFrame([
    {"A1": 1,"A2": 5,"A3": 5,"A4": 3,"A5": 3},
    {"A1": 1/5,"A2": 1,"A3": 3,"A4": 5,"A5": 5},
    {"A1": 1/5,"A2": 1/3,"A3": 1,"A4": 3,"A5": 3},
    {"A1": 1/3,"A2": 1/5,"A3": 1/3,"A4": 1,"A5": 1},
    {"A1": 1/3,"A2": 1/5,"A3": 1/3,"A4": 1,"A5": 1},
])

tabs = [crit1,crit2,crit3,crit4,crit5]

def vec_prior(tab):
    w = []
    v1 = (tab.iloc[0].prod() ** (1/5)).round(3)
    v2 = (tab.iloc[1].prod() ** (1/5)).round(3)
    v3 = (tab.iloc[2].prod() ** (1/5)).round(3)
    v4 = (tab.iloc[3].prod() ** (1/5)).round(3)
    v5 = (tab.iloc[4].prod() ** (1/5)).round(3)
    v_all = v1 + v2 + v3 + v4 + v5
    w.append((v1 / v_all).round(3))
    w.append((v2 / v_all).round(3))
    w.append((v3 / v_all).round(3))
    w.append((v4 / v_all).round(3))
    w.append((v5 / v_all).round(3))
    return w

def check(tab, vec):
    p1 = tab["A1"].sum() * vec[0]
    p2 = tab["A2"].sum() * vec[1]
    p3 = tab["A3"].sum() * vec[2]
    p4 = tab["A4"].sum() * vec[3]
    p5 = tab["A5"].sum() * vec[4]
    lamb = p1 + p2 + p3 + p4 +p5
    print(lamb)
    return (((lamb - 5)/(5 - 1)) / 1.12) <= 0.1

alts_vec = []
crit_vec = []

vec = vec_prior(all_crit)
print("Вектор приоритетов", [float(x) for x in vec])
[crit_vec.append(float(x)) for x in vec]

for i, tab in enumerate(tabs, 1):
    alt = []
    vec = vec_prior(tab)
    print("Вектор приоритетов", [float(x) for x in vec])
    print(check(tab,vec))
    [alt.append(float(x)) for x in vec]
    alts_vec.append(alt)

best_alt_vec = []
print()
for i in range (5):
    W = 0
    for j in range (5):
        W += crit_vec[j] * alts_vec[j][i]
    print(f"Приоритет альтернативы №{i + 1} : {round(W,3)}")
    best_alt_vec.append(round(W,3))
print(f"\nЛучшая альтернатива : №{np.argmax(best_alt_vec) + 1}")