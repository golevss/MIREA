import pandas as pd

alts = pd.DataFrame([
    {"name": "TIE Fighter", "credits": 20000, "speed": 5000, "hyper": 3.0, "weapons": 2, "shields": 100},
    {"name": "TZ-24", "credits": 22000, "speed": 4900, "hyper": 3.2, "weapons": 4, "shields": 120},
    {"name": "S-100", "credits": 21000, "speed": 4800, "hyper": 3.1, "weapons": 3, "shields": 150},
    {"name": "F-T2", "credits": 30000, "speed": 5100, "hyper": 4.0, "weapons": 3, "shields": 110},
    {"name": "CR90", "credits": 25000, "speed": 4600, "hyper": 3.5, "weapons": 2, "shields": 130},
    {"name": "IL-5", "credits": 26000, "speed": 4700, "hyper": 3.7, "weapons": 2, "shields": 100},
    {"name": "FT-6", "credits": 35000, "speed": 4400, "hyper": 4.5, "weapons": 2, "shields": 110},
    {"name": "FT-8", "credits": 34000, "speed": 4500, "hyper": 4.3, "weapons": 3, "shields": 115},
    {"name": "S-13", "credits": 33000, "speed": 4600, "hyper": 4.1, "weapons": 2, "shields": 105},
    {"name": "S-SC4", "credits": 32000, "speed": 4700, "hyper": 3.9, "weapons": 3, "shields": 125},
])

min_crit = ["credits", "hyper"]
plus_crit = ["speed", "weapons", "shields"]


def dom(a, b):
    if sum(a[min_crit].values == b[min_crit].values) + sum(a[plus_crit].values == b[plus_crit].values):
        return False
    crits = sum(a[min_crit].values <= b[min_crit].values) + sum(a[plus_crit].values >= b[plus_crit].values)

    return crits == len(min_crit) + len(plus_crit)

def pareto(alts):
    pareto = []
    for i in range (len(alts)):
        for j in range (i+ 1,len(alts)):
            if dom(alts.iloc[i], alts.iloc[j]):
                pareto.append(alts.iloc[i])
                break   
    
    return pd.DataFrame(pareto)

opt_alt = pareto(alts)

print("\nОптимальное множество:")
print(opt_alt["name"].to_list())

fil_opt_alt = opt_alt[
    (opt_alt["credits"] <= 22000) &
    (opt_alt["speed"] >= 4800) &
    (opt_alt["hyper"] >= 3.0) &
    (opt_alt["weapons"] >= 3) &
    (opt_alt["shields"] > 100)
]

print("\nУказание верхних/нижних границ критериев:")
print(fil_opt_alt["name"].to_list())

fil_opt_alt = opt_alt[
    (opt_alt["credits"] <= 25000) &
    (opt_alt["hyper"] >= 3.2) &
    (opt_alt["weapons"] > 2) &
    (opt_alt["shields"] >= 120)
]

fil_opt_alt = fil_opt_alt.sort_values(by="speed", ascending=False)

print("\nСубоптимизация:")
print(fil_opt_alt["name"].to_list())

criteria_priority = ["speed", "weapons", "shields", "credits", "hyper"]

filtered_opt_alt = alts.sort_values(by=criteria_priority, ascending=[False, False, False, True, True])

print("\nЛексикографическая оптимизация:")
print(filtered_opt_alt["name"].to_list()[0])