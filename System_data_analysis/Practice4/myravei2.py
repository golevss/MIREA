import numpy as np
import random
import datetime

class AntAlg:
    def __init__(self, distances: np.ndarray, n_ants, n_iterations, alpha, beta, rho, q):
        self.distances = distances
        self.n = len(distances)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q

        self.pheromone = np.ones((self.n, self.n)) / self.n

        self.best_path = None
        self.best_length = float('inf')

    def _initialize_ants(self):
        return [random.sample(range(self.n), 1) for _ in range(self.n_ants)]

    def _select_next_city(self, ant_path, allowed_cities):
        current_city = ant_path[-1]

        probabilities = []
        total = 0

        for city in allowed_cities:
            if self.distances[current_city][city] > 0:
                pheromone = self.pheromone[current_city][city] ** self.alpha
                heuristic = (1.0 / self.distances[current_city][city]) ** self.beta
                prob = pheromone * heuristic
                probabilities.append((city, prob))
                total += prob

        if total > 0:
            probabilities = [(city, prob / total) for city, prob in probabilities]

            r = random.random()
            cumulative = 0
            for city, prob in probabilities:
                cumulative += prob
                if r <= cumulative:
                    return city

        return random.choice(allowed_cities)

    def _construct_solution(self, ant_path):
        all_cities = list(range(self.n))

        allowed_cities = [city for city in all_cities if city not in ant_path]

        while allowed_cities:
            next_city = self._select_next_city(ant_path, allowed_cities)
            ant_path.append(next_city)
            allowed_cities.remove(next_city)

        return ant_path

    def _calculate_path_length(self, path):
        length = 0
        for i in range(len(path)):
            j = (i + 1) % len(path)
            length += self.distances[path[i]][path[j]]
        return length

    def _update_pheromones(self, all_paths, all_lengths):
        self.pheromone *= (1 - self.rho)

        for path, length in zip(all_paths, all_lengths):
            for i in range(len(path)):
                j = (i + 1) % len(path)
                self.pheromone[path[i]][path[j]] += self.q / length
                self.pheromone[path[j]][path[i]] += self.q / length

    def run(self):
        s = 50
        for iteration in range(self.n_iterations):
            all_paths = []
            all_lengths = []
            s += 1
            for ant in range(self.n_ants):
                ant_path = [1]

                ant_path = self._construct_solution(ant_path)

                path_length = self._calculate_path_length(ant_path)

                
                print(ant_path + [1], path_length)

                all_paths.append(ant_path)
                all_lengths.append(path_length)

                if path_length < self.best_length:
                    self.best_length = path_length
                    self.best_path = ant_path.copy()

            print()

            self._update_pheromones(all_paths, all_lengths)

        return self.best_path, self.best_length


if __name__ == "__main__":
    distances = np.array([
        [0, 10, 15, 20, 25],
        [10, 0, 35, 25, 30],
        [15, 35, 0, 30, 10],
        [20, 25, 30, 0, 15],
        [25, 30, 10, 15, 0]
    ])

    start = datetime.datetime.now()
    aa = AntAlg(distances, 6, 50, 1, 2, 0.5, 100)

    best_path, best_length = aa.run()
    end = datetime.datetime.now()
    print(f"Лучшая длина маршрута: {best_length:.2f}")
    print(f"Лучший маршрут: {best_path + [1]}") 
    print(end - start)