import numpy as np

class BackpropagationNN:
    def __init__(self, n_inputs, n_hidden, n_outputs, init_scale=0.5, alpha=0.5):
        self.alpha = alpha  
        
        self.W1 = np.random.uniform(-init_scale, init_scale, (n_inputs, n_hidden))
        self.b1 = np.random.uniform(-init_scale, init_scale, (1, n_hidden))
        
        self.W2 = np.random.uniform(-init_scale, init_scale, (n_hidden, n_outputs))
        self.b2 = np.random.uniform(-init_scale, init_scale, (1, n_outputs))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, y):
        return y * (1 - y)

    def forward(self, X):
        self.hidden_input = np.dot(X, self.W1) + self.b1
        self.hidden_output = self.sigmoid(self.hidden_input)

        self.final_input = np.dot(self.hidden_output, self.W2) + self.b2
        self.final_output = self.sigmoid(self.final_input)

        return self.final_output

    def backward(self, X, D):
        error = D - self.final_output
        delta_output = error * self.sigmoid_derivative(self.final_output)

        delta_hidden = delta_output.dot(self.W2.T) * self.sigmoid_derivative(self.hidden_output)

        self.W2 += self.alpha * self.hidden_output.T.dot(delta_output)
        self.b2 += self.alpha * np.sum(delta_output, axis=0, keepdims=True)

        self.W1 += self.alpha * X.T.dot(delta_hidden)
        self.b1 += self.alpha * np.sum(delta_hidden, axis=0, keepdims=True)

        return np.mean(np.square(error))

    def train(self, X, D, epochs=1000):
        for epoch in range(epochs):
            self.forward(X)
            loss = self.backward(X, D)

    def predict(self, X):
        return self.forward(X)

if __name__ == "__main__":
    X = np.array([[0,0],
                [0,1],
                [1,0],
                [1,1]])
    D = np.array([[0],[1],[1],[0]])

    neuron = BackpropagationNN(n_inputs=2, n_hidden=2, n_outputs=1, alpha=0.5)
    neuron.train(X, D, epochs=5000)

    print("Результаты после обучения:")
    for i, x in enumerate(X):
        print(f"Вход={x}, Выход={neuron.predict(x.reshape(1,-1)).round(0)}")
    
