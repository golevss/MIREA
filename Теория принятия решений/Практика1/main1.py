alts = [
    {"name": "TIE Fighter", "credits": 20000, "speed": 5000, "hyper": 3.0, "weapons": 2, "shields": 100},
    {"name": "TZ-24",       "credits": 22000, "speed": 4900, "hyper": 3.2, "weapons": 4, "shields": 120},
    {"name": "S-100",       "credits": 21000, "speed": 4800, "hyper": 3.1, "weapons": 3, "shields": 150},
    {"name": "F-T2",        "credits": 30000, "speed": 5100, "hyper": 4.0, "weapons": 3, "shields": 110},
    {"name": "CR90",        "credits": 25000, "speed": 4600, "hyper": 3.5, "weapons": 2, "shields": 130},
    {"name": "IL-5",        "credits": 26000, "speed": 4700, "hyper": 3.7, "weapons": 2, "shields": 100},
    {"name": "FT-6",        "credits": 35000, "speed": 4400, "hyper": 4.5, "weapons": 2, "shields": 110},
    {"name": "FT-8",        "credits": 34000, "speed": 4500, "hyper": 4.3, "weapons": 3, "shields": 115},
    {"name": "S-13",        "credits": 33000, "speed": 4600, "hyper": 4.1, "weapons": 2, "shields": 105},
    {"name": "S-SC4",       "credits": 32000, "speed": 4700, "hyper": 3.9, "weapons": 3, "shields": 125},
]

min_crit = ["credits", "hyper"]
plus_crit = ["speed", "weapons", "shields"]

def dom(a, b):
    crits = 0

    for crit in min_crit:
        if a[crit] <= b[crit]:
            crits += 1

    for crit in plus_crit:
        if a[crit] >= b[crit]:
            crits += 1

    return crits == 5

def pareto(alts):
    pareto = []
    for i in range (len(alts)):
        for j in range (i+ 1,len(alts)):
            if dom(alts[i], alts[j]):
                pareto.append(alts[i])
                break
    
    return pareto

opt_alt = pareto(alts)

for alt in opt_alt:
    print(alt["name"])
