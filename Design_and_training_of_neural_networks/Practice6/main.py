import numpy as np

class CounterPropagationNetwork:
    def __init__(self, n_inputs, n_hidden, n_outputs, alpha=0.5, beta=0.3):
        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_outputs = n_outputs

        self.alpha = alpha
        self.beta = beta

        self.W_kohonen = np.random.rand(n_hidden, n_inputs)
        self.W_kohonen = self.W_kohonen / np.linalg.norm(self.W_kohonen, axis=1, keepdims=True)

        self.W_grossberg = np.random.rand(n_hidden, n_outputs)

    def normalize(self, x):
        norm = np.linalg.norm(x)
        return x / norm if norm != 0 else x

    def kohonen_winner(self, x):
        activations = np.dot(self.W_kohonen, x)
        return np.argmax(activations)

    def train(self, X, D, epochs=100):
        for epoch in range(epochs):
            for x, d in zip(X, D):
                x = self.normalize(x)

                winner = self.kohonen_winner(x)
                self.W_kohonen[winner] += self.alpha * (x - self.W_kohonen[winner])
                self.W_kohonen[winner] /= np.linalg.norm(self.W_kohonen[winner]) 

                self.W_grossberg[winner] += self.beta * (d - self.W_grossberg[winner])

    def predict(self, x):
        x = self.normalize(x)
        winner = self.kohonen_winner(x)
        y = self.W_grossberg[winner]
        return np.where(y >= 0.5, 1, 0)

if __name__ == "__main__":
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    D = np.array([
        [0],
        [1],
        [1],
        [0]
    ])

    net = CounterPropagationNetwork(n_inputs=2, n_hidden=4, n_outputs=1, alpha=0.4, beta=0.3)
    net.train(X, D, epochs=100)

    print("\nРезультаты:")
    for x in X:
        print(f"Вход {x} → Выход {net.predict(x)}")
