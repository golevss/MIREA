import numpy as np

class KohonenSOM:
    def __init__(self, n_inputs, grid_size=(3, 3), alpha=0.5, sigma=None):
        self.n_inputs = n_inputs
        self.grid_size = grid_size
        self.alpha = alpha
        self.sigma = sigma if sigma is not None else max(grid_size) / 2
        
        self.weights = np.random.rand(grid_size[0], grid_size[1], n_inputs)

        self.neuron_locations = np.array(
            [[i, j] for i in range(grid_size[0]) for j in range(grid_size[1])]
        )

    def _find_bmu(self, x):
        distances = np.linalg.norm(self.weights - x, axis=2)
        bmu_idx = np.unravel_index(np.argmin(distances), distances.shape)
        return bmu_idx

    def _neighborhood_function(self, bmu_idx, iteration, max_iter):
        decayed_sigma = self.sigma * np.exp(-iteration / (max_iter / np.log(self.sigma + 1e-8)))
        bmu_loc = np.array(bmu_idx)

        dist_sq = np.sum((self.neuron_locations - bmu_loc) ** 2, axis=1)
        h = np.exp(-dist_sq / (2 * decayed_sigma ** 2))
        return h.reshape(self.grid_size)

    def train(self, X, epochs=100):
        for epoch in range(epochs):
            alpha_t = self.alpha * np.exp(-epoch / epochs)
            
            for x in X:
                bmu_idx = self._find_bmu(x)
                h = self._neighborhood_function(bmu_idx, epoch, epochs)
                for i in range(self.grid_size[0]):
                    for j in range(self.grid_size[1]):
                        self.weights[i, j, :] += alpha_t * h[i, j] * (x - self.weights[i, j, :])

    def predict(self, x):
        return self._find_bmu(x)

if __name__ == "__main__":
    X = np.array([
        [0.2, 0.1],
        [0.1, 0.2],
        [0.9, 0.8],
        [0.9, 0.9]
    ])

    som = KohonenSOM(n_inputs=2, grid_size=(3, 3), alpha=0.6)
    som.train(X, epochs=50)

    print("\nРасположение нейронов-победителей:")
    for x in X:
        print(f"Вход {x} → нейрон {som.predict(x)}")
