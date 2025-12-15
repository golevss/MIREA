import numpy as np
import datetime

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

        self.step = 0.1

    def calc(self):
        self.f = f(self.x, self.y)
        return self.f
    
    def make_local_jump(self, max_jump):
        self.xi, self.yi,  self.fi = self.x, self.y, self.f
        best_xi, best_yi, best_fi = self.xi, self.yi, self.fi

        jumps_left = max_jump

        while jumps_left > 0:
            trial_x = np.random.uniform(self.xi - self.step, self.xi + self.step)
            trial_y = np.random.uniform(self.yi - self.step, self.yi + self.step)

            trial_x = np.clip(trial_x, -4.5, 4.5)
            trial_y = np.clip(trial_y, -4.5, 4.5)

            trial_f = f(trial_x, trial_y)

            if trial_f < best_fi:
                best_xi, best_yi, best_fi = trial_x, trial_y, trial_f
                jumps_left = max_jump
            else:
                jumps_left -= 1

        self.xi, self.yi, self.fi = best_xi, best_yi, best_fi
        return self.fi

    def make_global_jump(self, c_x, c_y):
        self.x = self.x + np.random.uniform(1, 2) * (c_x - self.x)
        self.y = self.y + np.random.uniform(1, 2) * (c_y - self.y)

        self.x = np.clip(self.x, -4.5, 4.5)
        self.y = np.clip(self.y, -4.5, 4.5)

        self.calc()
    
    def update(self):
        self.x, self.y, self.f = self.xi, self.yi, self.fi


class Troop:
    def __init__(self):
        self.n_monkeys = 15
        self.max_local_jumps = 20

    def monkey_init(self, minZ, maxZ):
        monkeyz = []
        for _ in range(self.n_monkeys):
            m = Monkey()
            m.x = np.random.uniform(minZ, maxZ)
            m.y = np.random.uniform(minZ, maxZ)
            m.calc()
            
            monkeyz.append(m)
        return monkeyz

    def find_best(self, iter):
        monkeyz = self.monkey_init(-4.5, 4.5)

        for i in range(iter):
            c_x = np.mean([m.x for m in monkeyz])
            c_y = np.mean([m.y for m in monkeyz])

            for monk in monkeyz:
                if monk.make_local_jump(self.max_local_jumps) < monk.f:
                    monk.update()
                else:
                    monk.make_global_jump(c_x, c_y)
                    c_x = np.mean([m.x for m in monkeyz])
                    c_y = np.mean([m.y for m in monkeyz])

        monkeyz.sort(key=lambda b: b.f)
        return monkeyz[0]


if __name__ == '__main__':
    print("Эталон: f(3, 0.5) = 0")

    troop = Troop()
    iter = 100
    start = datetime.datetime.now()
    best_monkey = troop.find_best(iter)
    end = datetime.datetime.now()
    print(end - start)
    print(f"Результат x = {best_monkey.x:.5f} y = {best_monkey.y:.5f} f = {best_monkey.f:.8f}")
