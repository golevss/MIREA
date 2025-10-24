import numpy as np

class RBFNetwork:
    def __init__(self, n_inputs, n_hidden, n_outputs, alpha=0.1):
        self.alpha = alpha

        self.centers = np.random.rand(n_hidden, n_inputs) 
        self.sigma = np.ones(n_hidden)
        self.W = np.random.randn(n_hidden, n_outputs)
        self.b = np.random.randn(1, n_outputs)

    def _gaussian(self, x, c, s):
        return np.exp(-np.linalg.norm(x - c) ** 2 / (2 * s ** 2))

    def _rbf_layer(self, X):
        G = np.zeros((X.shape[0], self.centers.shape[0]))
        for i, x in enumerate(X):
            for j, c in enumerate(self.centers):
                G[i, j] = self._gaussian(x, c, self.sigma[j])
        return G

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, X):
        G = self._rbf_layer(X)
        output_linear = np.dot(G, self.W) + self.b
        output = self._sigmoid(output_linear)
        return output, G

    def train(self, X, D, epochs=200):
        random_idx = np.random.choice(X.shape[0], self.centers.shape[0], replace=False)
        self.centers = X[random_idx]

        d_max = np.max([np.linalg.norm(c1 - c2) for c1 in self.centers for c2 in self.centers])
        self.sigma[:] = d_max / np.sqrt(2 * self.centers.shape[0])

        for epoch in range(epochs):
            Y, G = self.forward(X)
            error = D - Y
            loss = np.mean(np.square(error))
            self.W += self.alpha * np.dot(G.T, error)
            self.b += self.alpha * np.sum(error, axis=0, keepdims=True)

    def predict(self, X):
        Y, _ = self.forward(X)
        return (Y >= 0.5).astype(int)

if __name__ == "__main__":
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    D = np.array([[0], [1], [1], [0]])

    rbf = RBFNetwork(n_inputs=2, n_hidden=4, n_outputs=1, alpha=0.5)
    rbf.train(X, D, epochs=200)

    print("\nРезультаты после обучения:")
    for x in X:
        y = rbf.predict(x.reshape(1, -1))
        print(f"Вход={x}, Выход={y[0][0]}")
