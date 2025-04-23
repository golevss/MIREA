def main(x):
    rules = {
        "node": "x[1]",
        "branches": {
            "SCAML": {
            "node": "x[2]",
            "branches": {
                "FREGE": 0,
                "HAXE": 1,
                "GENIE": {
                "node": "x[0]",
                "branches": {
                    "1961": 2,
                    "1975": 3,
                    "2019": 4
                }
                }
            }
            },
            "DYLAN": {
            "node": "x[3]",
            "branches": {
                "1996": {
                "node": "x[0]",
                "branches": {
                    "1961": 5,
                    "1975": 6,
                    "2019": 7
                }
                },
                "1995": {
                "node": "x[2]",
                "branches": {
                    "FREGE": 8,
                    "HAXE": 9,
                    "GENIE": 10
                }
                },
                "2015": 11
            }
            },
            "SAS": {
            "node": "x[3]",
            "branches": {
                "1996": {
                "node": "x[0]",
                "branches": {
                    "1961": 5,
                    "1975": 6,
                    "2019": 7
                }
                },
                "1995": {
                "node": "x[2]",
                "branches": {
                    "FREGE": 8,
                    "HAXE": 9,
                    "GENIE": 10
                }
                },
                "2015": 11
            }
            },
            "QMAKE": {
            "node": "x[4]",
            "branches": {
                "BLADE": 13,
                "C": 14
            }
            }
        }
    }
    
print(main([2019, 'SCAML', 'FREGE', 2015, 'BLADE']))
# Ожидаемо: ≈ 1.83e-01
