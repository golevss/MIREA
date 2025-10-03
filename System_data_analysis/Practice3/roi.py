import numpy as np

def f(x, y):
    return (1.5 - x + x*y)**2 + (2.25 - x + x*(y**2))**2 + (2.625 - x + x*(y**3))**2

class Particle():
    def __init__(self):
        self.xi = []
        self.yi = []
        self.func = []
        self.Vxi = []
        self.Vyi = []
    
    def find_best(self):
        minf = min(self.func)
        for i in range(len(self.func)):
            if minf == self.func[i]:
                return self.xi[i], self.yi[i]


class Roi():
    def __init__(self):
        self.parts = []
        self.glob_best = ()
        self.iteration = 0
        
        self.c1, self.c2 = 2, 2
        self.r1, self.r2 = np.random.uniform(0, 1), np.random.uniform(0, 1)

    def create(self, count, minZ, maxZ):
        for _ in range (count):
            part = Particle()
            
            part.xi.append(np.random.uniform(minZ, maxZ))
            part.yi.append(np.random.uniform(minZ, maxZ))
            part.func.append(f(part.xi[0],part.yi[0]))

            part.Vxi.append(np.random.uniform(minZ, maxZ))
            part.Vyi.append(np.random.uniform(minZ, maxZ))
           
            self.parts.append(part)
        minf = min(obj.func for obj in self.parts)
        for obj in self.parts:
            self.glob_best = (obj.xi[0], obj.yi[0], obj.func[0]) if minf == obj.func else self.glob_best

    def new_v(self, n, xb, yb):
        return (
            self.parts[n].Vxi[self.iteration] 
            + self.c1 * self.r1 * (xb - self.parts[n].xi[self.iteration])
            + self.c2 * self.r2 * (self.glob_best[0] - self.parts[n].xi[self.iteration])
        ),(
            self.parts[n].Vyi[self.iteration] 
            + self.c1 * self.r1 * (yb - self.parts[n].yi[self.iteration])
            + self.c2 * self.r2 * (self.glob_best[1] - self.parts[n].yi[self.iteration])
        )
    
    def make_iter(self, N):
        for i in range(N):
            xb, yb = self.parts[i].find_best()
            Vx, Vy = self.new_v(i, xb, yb)
            
            self.parts[i].Vxi.append(Vx)
            self.parts[i].Vyi.append(Vy)
            
            self.parts[i].xi.append(self.parts[i].xi[self.iteration] + Vx)
            self.parts[i].yi.append(self.parts[i].yi[self.iteration] + Vy)
            self.parts[i].func.append(f(self.parts[i].xi[self.iteration] + Vx, self.parts[i].yi[self.iteration] + Vy))
        
        minf = min(min(obj.func) for obj in self.parts)
        for obj in self.parts:
            for i in range (len(obj.func)):
                self.glob_best = (obj.xi[i], obj.yi[i], obj.func[i]) if minf == obj.func[i] else self.glob_best
        
        self.iteration += 1

    def print(self):
        for obj in self.parts:
            print(f'x = {obj.xi[self.iteration]}  y = {obj.yi[self.iteration]}  f(x,y) = {obj.func[self.iteration]}')


if __name__ == '__main__':
    obj = Roi() 
    N = 5
    max_iter = 50

    obj.create(N, -4.5, 4.5)
    
    print("==Начальные позиции роя==")
    obj.print()
    print(obj.glob_best)

    while obj.iteration != max_iter:
        obj.make_iter(N)

    print("\n==Конечные позиции роя==")
    obj.print()
    print(obj.glob_best)