import numpy as np


def f(x, y):
    return (1.5 - x + x*y)**2 + (2.25 - x + x*(y**2))**2 + (2.625 - x + x*(y**3))**2

class Bee():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.f = 0

    def calc(self):
        self.f = f(self.x, self.y)
        return self.f

    def calc_x_area(self, inaccuracy):
        return self.x - inaccuracy, self.x + inaccuracy

    def calc_y_area(self, inaccuracy):
        return self.y - inaccuracy, self.y + inaccuracy 


class Colony():
    def __init__(self):
        self.scouts = 20
        self.best = 7
        self.worst = 2
        self.best_area = 5
        self.worst_area = 1
        self.inaccuracy = 1

    def bee_atack(self, iter, minX, maxX, minY, maxY):
        beez = []
        for i in range (iter):
            bee = Bee()
            bee.x = np.random.uniform(minX, maxX)
            bee.y = np.random.uniform(minY, maxY)

            bee.x = np.clip(bee.x, -4.5, 4.5)
            bee.y = np.clip(bee.y, -4.5, 4.5)
            
            bee.calc()

            beez.append(bee)
        beez.sort(key=lambda b: b.f)

        return beez

    def find_best(self, iter):
        beez = self.bee_atack(self.scouts, -4.5, 4.5, -4.5, 4.5)
        beez = beez[:self.best_area + self.worst_area]

        cur_beez = []
        for i in range(iter):
            for bee in range (self.best_area):
                minX, maxX = beez[bee].calc_x_area(self.inaccuracy)
                minY, maxY = beez[bee].calc_y_area(self.inaccuracy)
                cur_beez += self.bee_atack(self.best, minX, maxX, minY, maxY)

            for bee in range (self.worst_area):
                minX, maxX = beez[self.best_area + bee].calc_x_area(self.inaccuracy)
                minY, maxY = beez[self.best_area + bee].calc_y_area(self.inaccuracy)
                cur_beez += self.bee_atack(self.worst, minX, maxX, minY, maxY)

            cur_beez.sort(key=lambda b: b.f)
            cur_beez = cur_beez[:self.best_area + self.worst_area]
        
        return cur_beez[0]


if __name__ == '__main__':
    print("Эталон: f(3, 0.5) = 0")

    c = Colony()
    iter = 1000

    best_bee = c.find_best(iter)
    print(f"Результат x = {best_bee.x:.5f} y = {best_bee.y:.5f} f = {best_bee.f:.5f}")
