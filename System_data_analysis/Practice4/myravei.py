import numpy as np


def createGraph(cNodes):    
    structure = {}
    step = 1
    for i in range (cNodes):
        structure[str(i + step)] = [] 

    for i in range (cNodes):
        for j in range(i + 1, cNodes):
            w = np.random.randint(1, 10)

            structure[str(i + step)].append((str(j + step), w))
            structure[str(j + step)].append((str(i + step), w))
    
    return structure, step


def ant_colony_tsp(structure, n_ants=5, n_iterations=50, alpha=1.0, q=5.0, rho=0.5, Q=100.0, seed=123):

    rng = np.random.default_rng(seed)

    nodes = sorted(structure.keys(), key=lambda x: int(x))
    n = len(nodes)
    node_index = {node: idx for idx, node in enumerate(nodes)}

    dist = np.full((n, n), np.inf, dtype=float)
    for u in nodes:
        i = node_index[u]
        for v, w in structure[u]:
            j = node_index[v]
            dist[i, j] = w
            dist[j, i] = w 

    l = np.zeros_like(dist)
    finite_mask = np.isfinite(dist)
    l[finite_mask] = 1.0 / dist[finite_mask]

    tau = np.ones((n, n), dtype=float)

    best_path = None
    best_length = np.inf

    for it in range(n_iterations):
        all_paths = []
        all_lengths = []

        for ant in range(n_ants):
            start = 0
            current = start
            visited = {current}
            path = [current]

            while len(visited) < n:
                neighbors = [j for j in range(n) if j not in visited]

                tau_curr = tau[current, neighbors]
                l_curr = l[current, neighbors]

                weights = (tau_curr ** alpha) * (l_curr ** q)

                if weights.sum() == 0:
                    probs = np.ones_like(weights) / len(weights)
                else:
                    probs = weights / weights.sum()

                next_idx = rng.choice(len(neighbors), p=probs)
                next_vertex = neighbors[next_idx]

                path.append(next_vertex)
                visited.add(next_vertex)
                current = next_vertex

            path.append(start)

            length = 0.0
            for i in range(len(path) - 1):
                length += dist[path[i], path[i + 1]]

            all_paths.append(path)
            all_lengths.append(length)

            print(f"{path} | {length}")
            if length < best_length:
                best_length = length
                best_path = path
        print()
        tau *= (1.0 - rho)
        for path, length in zip(all_paths, all_lengths):
            if length == 0:
                continue
            delta = Q / length
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                tau[a, b] += delta
                tau[b, a] += delta

        # print(f"{best_path} | {best_length}")

    best_path_nodes = [nodes[i] for i in best_path]
    return best_path_nodes, best_length


if __name__ == "__main__":
    cNodes = 6
    structure, start = createGraph(cNodes)

    best_path, best_length = ant_colony_tsp(structure, n_ants=6, n_iterations=100)

    print("Лучший путь:", best_path)
    print("Длина:", best_length)
