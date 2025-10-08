import numpy as np

def f(x, y):
    return (1.5 - x + x*y)**2 + (2.25 - x + x*(y**2))**2 + (2.625 - x + x*(y**3))**2

def otzhig(T = 1,Tmin = 1e-100, alpha = np.random.uniform(0.1, 1)):
    xb = np.random.uniform(-4.5, 4.5)
    yb = np.random.uniform(-4.5, 4.5)

    while (T > Tmin):
        xi = np.random.uniform(-4.5, 4.5)
        yi = np.random.uniform(-4.5, 4.5)
        
        funci = f(xi,yi)
        funcb = f(xb,yb)
        
        if (funci - funcb <= 0):
            xb = xi
            yb = yi
        else:
            if (np.exp(-(funci - funcb) / T) > np.random.uniform(0, 1)):
                xb = xi
                yb = yi
        
        T *= alpha

    return xb, yb

def otzhigKoshi(T = 1,Tmin = 1e-1000, k=1):
    xb = np.random.uniform(-4.5, 4.5)
    yb = np.random.uniform(-4.5, 4.5)

    while (T > Tmin):
        xi = np.random.uniform(-4.5, 4.5)
        yi = np.random.uniform(-4.5, 4.5)
        
        funci = f(xi,yi)
        funcb = f(xb,yb)
        
        if (funci - funcb <= 0):
            xb = xi
            yb = yi
        else:
            if (np.exp(-(funci - funcb) / T) > np.random.uniform(0, 1)):
                xb = xi
                yb = yi
        
        T /= k
        k+=0.5

    return xb, yb

print("Эталон: f(3,0.5) = 0")
xb, yb = otzhig()
print("Отжиг")
print(xb, yb)
print(f(xb, yb))

print("Отжиг Коши")
xb, yb = otzhigKoshi()
print(xb, yb)
print(f(xb, yb))