import numpy as np

class Delta:
    def __init__(self, n_inputs, init_scale=0.05):
        self.w = np.random.uniform(0, init_scale, size=n_inputs)
        self.T = np.random.uniform(0, init_scale)
        self.eta = 1
        self.err = 0

    def activation(self, x):
        S = np.dot(x, self.w)
        return -1 if S > self.T else 1

    def modification(self, x, e):
        self.w = self.w + self.eta * x * e
        self.T = self.T + self.eta * e

    def predict(self, X):
        S = X.dot(self.w)
        return np.where(S > self.T, 1, -1)

    def train(self, X, D):
        for step in range(1, 100):
            total_error = 0
            for i in range(X.shape[0]):
                x = X[i]
                d = D[i]
                y = self.activation(x)

                e = d - y
                total_error += e
                self.modification(x, e)
                # print(f"{step} – {i}: Error={e}, w={self.w}, T={self.T}")
            # print(f"{step}: avg_error={avg_error}")
            if total_error < self.err:
                # print(f"Training stopped at step {step}")
                break
            


if __name__ == "__main__":
    X = np.array([[-1, -1],
                  [-1,  1],
                  [ 1, -1],
                  [ 1,  1]])
    D = np.array([-1, -1, -1, 1])

    neuron = Delta(n_inputs=2)
    print(f"Вес w = {neuron.w}, порог T = {neuron.T}")

    neuron.train(X, D)
    print(f"Вес w = {neuron.w}, порог T = {neuron.T}")

    y_pred = neuron.predict(X)
    print("Эталон:", D)
    print("Выходы:", y_pred)
