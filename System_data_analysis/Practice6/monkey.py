import numpy as np


def f(x, y):
    return (1.5 - x + x*y)**2 + (2.25 - x + x*(y**2))**2 + (2.625 - x + x*(y**3))**2


class Monkey:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.f = 0

        self.xi = 0
        self.yi = 0
        self.fi = 0

        self.jumps = 0
        self.step = 0.1

    def calc(self):
        self.f = f(self.x, self.y)
        return self.f
    
    def make_local_jump(self, max_jump):
        self.xi = self.x
        self.yi = self.y
        self.fi = self.f

        self.jumps = 0
        while self.jumps != max_jump:
            self.xi = np.random.uniform(self.xi - self.step, self.xi + self.step)
            self.yi = np.random.uniform(self.yi - self.step, self.yi + self.step)
            
            self.xi = np.clip(self.xi, -4.5, 4.5)
            self.yi = np.clip(self.yi, -4.5, 4.5)

            self.jumps += 1
        
        self.fi = f(self.xi, self.yi)
        return self.fi
    
    def make_global_jump(self, c_x, c_y):
            self.x = self.x + np.random.uniform(1, 2) * (c_x - self.x)
            self.y = self.y + np.random.uniform(1, 2) * (c_y - self.y)

            self.x = np.clip(self.x, -4.5, 4.5)
            self.y = np.clip(self.y, -4.5, 4.5)

            self.calc()
    
    def update(self):
        self.x = self.xi
        self.y = self.yi
        self.f = self.fi


class Troop:
    def __init__(self):
        self.monkeys = 10
        self.jumps = 5

        self.c_x = 0
        self.c_y = 0

    def monkey_init(self, minZ, maxZ):
        monkeyz = []
        for i in range (self.monkeys):
            monk = Monkey()
            monk.x = np.random.uniform(minZ, maxZ)
            monk.y = np.random.uniform(minZ, maxZ)
            monk.calc()

            monkeyz.append(monk)
        
        return monkeyz


    def find_best(self, iter):
        monkeyz = self.monkey_init(-4.5, 4.5)

        for i in range(iter):
            self.c_x = sum(m.x for m in monkeyz) / len(monkeyz)
            self.c_y = sum(m.y for m in monkeyz) / len(monkeyz)
            
            for monk in monkeyz:
                if monk.make_local_jump(self.jumps) < monk.f:
                    monk.update()
                else:
                    monk.make_global_jump(self.c_x, self.c_y)

        monkeyz.sort(key=lambda b: b.f)
        return monkeyz[0]




if __name__ == '__main__':
    print("Эталон: f(3, 0.5) = 0")

    troop = Troop()
    iter = 1000
    best_monk = troop.find_best(iter)
    print(f"Результат x = {best_monk.x} y = {best_monk.y} f = {best_monk.f}")
