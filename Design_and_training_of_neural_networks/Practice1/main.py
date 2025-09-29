import numpy as np

class Rosenblatt:
    def __init__(self, n_inputs, init_scale=0.05):
        self.w = np.random.uniform(0, init_scale, size=n_inputs)
        self.T = np.random.uniform(0, init_scale)

    def activation(self, x):
        net = np.dot(self.w, x) - self.T
        return 1 if net >= 0 else -1
    
    def modification(self, x, etal):
        self.w = self.w + x * etal
        self.T = self.T - etal

    def train(self, X, D):
        n_samples = X.shape[0]

        for i in range(n_samples):
            x = X[i]
            etal = D[i]
            y = self.activation(x)
            print(f"{i}: x={x}\tЭталон={etal}, Результат={y}")
            while y != etal:
                self.modification(x, etal)
                print(f"\tНовые значения -> w={self.w}, T={self.T}")
                
                y = self.activation(x)
                print(f"{i}: x={x}\tЭталон={etal}, Результат={y}")


if __name__ == "__main__":
    X = np.array([[-1, -1],
                  [-1,  1],
                  [ 1, -1],
                  [ 1,  1]])
    D = np.array([-1, -1, -1, 1])

    neuron = Rosenblatt(n_inputs=2)
    print(f"Вес w = {neuron.w}, порог T = {neuron.T}")

    neuron.train(X, D)
    print(f"Вес w = {neuron.w}, порог T = {neuron.T}")