def main(X):
    X = list(X)

    Xi = [chi**2 + 7*chi for chi in X if (chi <= -64 or 55 < chi)]

    Phi = [chi * xi for chi in X for xi in Xi if chi < xi]

    Z = [abs(xi) + xi for xi in Xi if xi >= 76]

    sum1 = sum(phi % 2 for phi in Phi)

    cartesian_product = {(phi, zeta) for phi in Phi for zeta in Z}
    sum2 = sum(phi + (ord(zeta) % 3 if isinstance(zeta, str) else zeta % 3)
               for phi, zeta in cartesian_product)

    psi = sum1 - sum2
    return psi

print(main({35, -93, 11, -85, -75, -74, -40, -6, 92, -67})) 
print(main({-38, 8, -49, -48, -9, -74, 22, 58, -69, 60})) 