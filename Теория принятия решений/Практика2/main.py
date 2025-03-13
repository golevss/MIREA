import pandas as pd

alts = pd.DataFrame([
    {"name": "TIE Fighter", "credits": 10, "speed": 30, "hyper": 10, "weapons": 10, "shields": 5},
    {"name": "TZ-24", "credits": 10, "speed": 25, "hyper": 10, "weapons": 30, "shields": 10},
    {"name": "S-100", "credits": 10, "speed": 20, "hyper": 10, "weapons": 20, "shields": 25},
    {"name": "F-T2", "credits": 20, "speed": 30, "hyper": 20, "weapons": 20, "shields": 5},
    {"name": "CR90", "credits": 10, "speed": 10, "hyper": 10, "weapons": 10, "shields": 15},
    {"name": "IL-5", "credits": 10, "speed": 15, "hyper": 20, "weapons": 10, "shields": 5},
    {"name": "FT-6", "credits": 30, "speed": 5, "hyper": 30, "weapons": 10, "shields": 5},
    {"name": "FT-8", "credits": 30, "speed": 5, "hyper": 30, "weapons": 20, "shields": 10},
    {"name": "S-13", "credits": 30, "speed": 10, "hyper": 30, "weapons": 10, "shields": 5},
    {"name": "S-SC4", "credits": 30, "speed": 15, "hyper": 20, "weapons": 20, "shields": 15},
])

min_crit = [1, 3]
plus_crit = [2, 4, 5]

N = len(alts)
pref_table = pd.DataFrame()

def compare(s1, s2):
    P = 0
    N = 0
    for crit in min_crit:
        P += s1.iloc[crit] if s1.iloc[crit] < s2.iloc[crit] else 0
        N += s2.iloc[crit] if s1.iloc[crit] > s2.iloc[crit] else 0

    for crit in plus_crit:
        P += s1.iloc[crit] if s1.iloc[crit] > s2.iloc[crit] else 0
        N += s2.iloc[crit] if s1.iloc[crit] < s2.iloc[crit] else 0
        
    if (N == 0):
        return "inf"
    if P/N > 1:
        return str(P) + "/" + str(N)
    else:
        return "-"

for i in range(N):
    for j in range(N):
        if i == j:
            pref_table.loc[i,j] = "x"
        else:
            pref_table.loc[i,j] = compare(alts.loc[i], alts.loc[j])
print("Матрицы предпочтений")
print(pref_table)

N = len(alts)
pref_table = pd.DataFrame()

def compare(s1, s2):
    P = 0
    N = 0
    for crit in min_crit:
        P += s1.iloc[crit] if s1.iloc[crit] < s2.iloc[crit] else 0
        N += s2.iloc[crit] if s1.iloc[crit] > s2.iloc[crit] else 0

    for crit in plus_crit:
        P += s1.iloc[crit] if s1.iloc[crit] > s2.iloc[crit] else 0
        N += s2.iloc[crit] if s1.iloc[crit] < s2.iloc[crit] else 0
        
    if (N == 0):
        return "inf"
    if P/N > 1.3:
        return str(P) + "/" + str(N)
    else:
        return "-"

for i in range(N):
    for j in range(N):
        if i == j:
            pref_table.loc[i,j] = "x"
        else:
            pref_table.loc[i,j] = compare(alts.loc[i], alts.loc[j])

print("\nМатрицы предпочтений с порогом 1.3")
print(pref_table)