import numpy as np

class ElmanRNN:
    def __init__(self, n_inputs, n_hidden, n_outputs, alpha=0.1):
        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_outputs = n_outputs
        self.alpha = alpha

        self.U = np.random.uniform(-0.5, 0.5, (n_hidden, n_inputs))
        self.W = np.random.uniform(-0.5, 0.5, (n_hidden, n_hidden))
        self.V = np.random.uniform(-0.5, 0.5, (n_outputs, n_hidden))
        
        self.bh = np.zeros((n_hidden, 1))
        self.by = np.zeros((n_outputs, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def dsigmoid(self, y):
        return y * (1 - y)

    def tanh(self, x):
        return np.tanh(x)

    def dtanh(self, y):
        return 1 - y ** 2

    def forward(self, X):
        T = len(X)
        self.h, self.y = {}, {}
        self.h[-1] = np.zeros((self.n_hidden, 1))
        for t in range(T):
            x_t = X[t].reshape(-1, 1)
            self.h[t] = self.tanh(np.dot(self.U, x_t) + np.dot(self.W, self.h[t-1]) + self.bh)
            self.y[t] = self.sigmoid(np.dot(self.V, self.h[t]) + self.by)
        return self.y, self.h

    def backward(self, X, D):
        T = len(X)
        dU = np.zeros_like(self.U)
        dW = np.zeros_like(self.W)
        dV = np.zeros_like(self.V)
        dbh = np.zeros_like(self.bh)
        dby = np.zeros_like(self.by)
        dh_next = np.zeros((self.n_hidden, 1))

        for t in reversed(range(T)):
            x_t = X[t].reshape(-1, 1)
            d = D[t].reshape(-1, 1)
            dy = (self.y[t] - d) * self.dsigmoid(self.y[t])
            dV += np.dot(dy, self.h[t].T)
            dby += dy

            dh = np.dot(self.V.T, dy) + dh_next
            dh_raw = dh * self.dtanh(self.h[t])
            dbh += dh_raw
            dU += np.dot(dh_raw, x_t.T)
            dW += np.dot(dh_raw, self.h[t-1].T)
            dh_next = np.dot(self.W.T, dh_raw)

        for param, dparam in zip([self.U, self.W, self.V, self.bh, self.by],
                                 [dU, dW, dV, dbh, dby]):
            param -= self.alpha * dparam

    def train(self, X, D, epochs=1000):
        for epoch in range(epochs):
            self.forward(X)
            self.backward(X, D)
            if epoch % 100 == 0:
                loss = np.mean([(D[t] - self.y[t])**2 for t in range(len(X))])

    def predict(self, X):
        y_pred, _ = self.forward(X)
        outputs = [1 if y[0] >= 0.5 else 0 for y in [v.flatten() for v in y_pred.values()]]
        return outputs

if __name__ == "__main__":
    X = [np.array([0]), np.array([1]), np.array([0]), np.array([1])]
    D = [np.array([0]), np.array([1]), np.array([0]), np.array([1])]

    rnn = ElmanRNN(n_inputs=1, n_hidden=3, n_outputs=1, alpha=0.05)
    rnn.train(X, D, epochs=1000)

    print("\nРезультаты:")
    Y = rnn.predict(X)
    for i, x in enumerate(X):
        print(f"Вход={x[0]}, Выход={Y[i]}")
