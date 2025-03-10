import math


def main(n):
    if (n == 0):
        return -0.93
    elif (n == 1):
        return -0.84
    else:
        return (main(n - 2))**3 + math.asin(main(n-1))**2

print(main (2))