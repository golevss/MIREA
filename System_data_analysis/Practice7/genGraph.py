import numpy as np


def createGraph(cNodes):    
    structure = {}
    step = 1
    for i in range(cNodes):
        structure[str(i + step)] = [] 

    for i in range(cNodes):
        for j in range(i + 1, cNodes):
            w = np.random.randint(1, 6)

            structure[str(i + step)].append((str(j + step), w))
            structure[str(j + step)].append((str(i + step), w))
    
    return structure, step


def genetic_tsp(structure, pop_size=80, n_generations=300,tournament_size=5, pc=0.9, pm=0.2, seed=132):
    
    rng = np.random.default_rng(seed)

    nodes = sorted(structure.keys(), key=lambda x: int(x))
    n = len(nodes)
    node_index = {node: idx for idx, node in enumerate(nodes)}

    dist = np.zeros((n, n), dtype=float)
    for u in nodes:
        i = node_index[u]
        for v, w in structure[u]:
            j = node_index[v]
            dist[i, j] = w
            dist[j, i] = w

    def tour_length(perm):
        length = 0.0
        for i in range(n - 1):
            length += dist[perm[i], perm[i + 1]]
        length += dist[perm[-1], perm[0]]
        return length

    def fitness(perm):
        L = tour_length(perm)
        return 1.0 / L

    population = []
    for _ in range(pop_size):
        perm = np.arange(n)
        rng.shuffle(perm)
        population.append(perm)

    def tournament_select(pop, fit_values):
        idx = rng.integers(0, len(pop), size=tournament_size)
        best_i = idx[np.argmax(fit_values[idx])]
        return pop[best_i].copy()

    def order_crossover(p1, p2):
        if rng.random() >= pc:
            return p1.copy(), p2.copy()

        a, b = sorted(rng.integers(0, n, size=2))
        c1 = np.full(n, -1, dtype=int)
        c1[a:b] = p1[a:b]
        p2_seq = [g for g in p2 if g not in c1]
        idx = 0
        for i in range(n):
            if c1[i] == -1:
                c1[i] = p2_seq[idx]
                idx += 1

        c2 = np.full(n, -1, dtype=int)
        c2[a:b] = p2[a:b]
        p1_seq = [g for g in p1 if g not in c2]
        idx = 0
        for i in range(n):
            if c2[i] == -1:
                c2[i] = p1_seq[idx]
                idx += 1

        return c1, c2

    def mutate(perm):
        if rng.random() < pm:
            i, j = rng.integers(0, n, size=2)
            perm[i], perm[j] = perm[j], perm[i]
        return perm

    best_perm = None
    best_fit = -np.inf

    for gen in range(n_generations):
        fits = np.array([fitness(ind) for ind in population])

        gen_best_i = np.argmax(fits)
        if fits[gen_best_i] > best_fit:
            best_fit = fits[gen_best_i]
            best_perm = population[gen_best_i].copy()
        
        print(best_perm)


        new_population = []
        while len(new_population) < pop_size:
            p1 = tournament_select(population, fits)
            p2 = tournament_select(population, fits)

            c1, c2 = order_crossover(p1, p2)

            c1 = mutate(c1)
            c2 = mutate(c2)

            new_population.append(c1)
            if len(new_population) < pop_size:
                new_population.append(c2)

        population = new_population

    best_tour_indices = best_perm
    best_tour_nodes = [nodes[i] for i in best_tour_indices]
    best_length = tour_length(best_perm)

    best_tour_nodes.append(best_tour_nodes[0])

    return best_tour_nodes, best_length


if __name__ == "__main__":
    cNodes = 6
    structure, start = createGraph(cNodes)

    best_tour, best_len = genetic_tsp(structure, pop_size=80, n_generations=300)

    print("Лучший путь:", best_tour)
    print("Длина:", best_len)
