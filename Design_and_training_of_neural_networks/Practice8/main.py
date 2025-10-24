import numpy as np

# --- Свёртка ---
class ConvLayer:
    def __init__(self, num_filters, kernel_size):
        self.num_filters = num_filters
        self.kernel_size = kernel_size
        self.filters = np.random.randn(num_filters, kernel_size, kernel_size) / (kernel_size * kernel_size)
    
    def _region(self, image):
        h, w = image.shape
        for i in range(h - self.kernel_size + 1):
            for j in range(w - self.kernel_size + 1):
                region = image[i:i+self.kernel_size, j:j+self.kernel_size]
                yield region, i, j

    def forward(self, image):
        self.last_input = image
        h, w = image.shape
        output = np.zeros((self.num_filters, h - self.kernel_size + 1, w - self.kernel_size + 1))
        for region, i, j in self._region(image):
            output[:, i, j] = np.sum(region * self.filters, axis=(1, 2))
        return output

    def backward(self, d_L_d_out, learn_rate):
        d_L_d_filters = np.zeros(self.filters.shape)
        for region, i, j in self._region(self.last_input):
            for f in range(self.num_filters):
                d_L_d_filters[f] += d_L_d_out[f, i, j] * region
        self.filters -= learn_rate * d_L_d_filters
        return None

# --- Активация ---
class ReLU:
    def forward(self, x):
        self.last_input = x
        return np.maximum(0, x)
    
    def backward(self, d_L_d_out):
        d_L_d_input = d_L_d_out.copy()
        d_L_d_input[self.last_input <= 0] = 0
        return d_L_d_input

# --- Чистка ---
class MaxPool:
    def __init__(self, size):
        self.size = size

    def _region(self, image):
        h, w = image.shape
        for i in range(0, h, self.size):
            for j in range(0, w, self.size):
                region = image[i:i+self.size, j:j+self.size]
                yield region, i, j

    def forward(self, image):
        self.last_input = image
        n_filters, h, w = image.shape
        output = np.zeros((n_filters, h // self.size, w // self.size))
        for f in range(n_filters):
            for region, i, j in self._region(image[f]):
                output[f, i//self.size, j//self.size] = np.max(region)
        return output

    def backward(self, d_L_d_out):
        d_L_d_input = np.zeros(self.last_input.shape)
        n_filters, h, w = self.last_input.shape
        for f in range(n_filters):
            for region, i, j in self._region(self.last_input[f]):
                h_out, w_out = i // self.size, j // self.size
                max_val = np.max(region)
                for i2 in range(self.size):
                    for j2 in range(self.size):
                        if region[i2, j2] == max_val:
                            d_L_d_input[f, i+i2, j+j2] = d_L_d_out[f, h_out, w_out]
        return d_L_d_input

# --- Вектор ---
class FullyConnected:
    def __init__(self, input_len, output_len):
        self.weights = np.random.randn(output_len, input_len) / input_len
        self.biases = np.zeros((output_len, 1))

    def forward(self, input_data):
        self.last_input_shape = input_data.shape
        input_data = input_data.flatten().reshape(-1, 1)
        self.last_input = input_data
        return np.dot(self.weights, input_data) + self.biases

    def backward(self, d_L_d_out, learn_rate):
        d_L_d_w = np.dot(d_L_d_out, self.last_input.T)
        d_L_d_b = d_L_d_out
        d_L_d_input = np.dot(self.weights.T, d_L_d_out)
        self.weights -= learn_rate * d_L_d_w
        self.biases -= learn_rate * d_L_d_b
        return d_L_d_input.reshape(self.last_input_shape)

# --- Выход ---
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def deriv_sigmoid(y):
    return y * (1 - y)

class SimpleCNN:
    def __init__(self):
        self.conv = ConvLayer(2, 3)
        self.relu = ReLU()
        self.pool = MaxPool(2)
        self.fc = FullyConnected(8, 1)

    def forward(self, image):
        out = self.conv.forward(image)
        out = self.relu.forward(out)
        out = self.pool.forward(out)
        out = self.fc.forward(out)
        return sigmoid(out)

    def train(self, X, D, epochs=100, lr=0.01):
        for epoch in range(epochs):
            total_loss = 0
            for img, target in zip(X, D):
                out = self.forward(img)
                loss = (target - out) ** 2
                total_loss += np.sum(loss)

                grad = -2 * (target - out) * deriv_sigmoid(out)
                grad = self.fc.backward(grad, lr)
                grad = self.pool.backward(grad)
                grad = self.relu.backward(grad)
                self.conv.backward(grad, lr)


    def predict(self, image):
        y = self.forward(image)
        return 1 if y >= 0.5 else 0

if __name__ == "__main__":
    vertical = np.array([
        [0,1,0,1,0,1],
        [0,1,0,1,0,1],
        [0,1,0,1,0,1],
        [0,1,0,1,0,1],
        [0,1,0,1,0,1],
        [0,1,0,1,0,1],
    ])

    horizontal = np.array([
        [0,0,0,0,0,0],
        [1,1,1,1,1,1],
        [0,0,0,0,0,0],
        [1,1,1,1,1,1],
        [0,0,0,0,0,0],
        [1,1,1,1,1,1],
    ])

    X = [vertical, horizontal]
    D = [np.array([[1]]), np.array([[0]])]

    cnn = SimpleCNN()
    cnn.train(X, D, epochs=100, lr=0.01)

    print("\nРезультаты для вертикального и горизонтального изображения:")
    for img, label in zip(X, D):
        print(f"Ожидаемый: {label[0][0]}, Предсказание: {cnn.predict(img)}")
