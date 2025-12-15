import numpy as np

def f(x, y):
    return (1.5 - x + x*y)**2 + (2.25 - x + x*(y**2))**2 + (2.625 - x + x*(y**3))**2


def genetic_minimize_beale(
        pop_size=50,
        n_generations=300,
        x_bounds=(-4.5, 4.5),
        y_bounds=(-4.5, 4.5),
        pc=0.8,
        pm=0.1,
        mutation_sigma=0.1,
        tournament_size=3,
        seed=123
    ):
    rng = np.random.default_rng(seed)

    pop = np.empty((pop_size, 2))
    pop[:, 0] = rng.uniform(x_bounds[0], x_bounds[1], size=pop_size)  # x
    pop[:, 1] = rng.uniform(y_bounds[0], y_bounds[1], size=pop_size)  # y

    def fitness(ind):
        x, y = ind
        value = f(x, y)
        return 1.0 / (1.0 + value)

    def evaluate_population(pop):
        return np.array([fitness(ind) for ind in pop])

    def tournament_select(pop, fit):
        idx = rng.integers(0, len(pop), size=tournament_size)
        best_i = idx[np.argmax(fit[idx])]
        return pop[best_i].copy()

    def crossover(parent1, parent2):
        if rng.random() < pc:
            alpha = rng.random()
            child1 = alpha * parent1 + (1 - alpha) * parent2
            child2 = alpha * parent2 + (1 - alpha) * parent1
        else:
            child1, child2 = parent1.copy(), parent2.copy()
        return child1, child2

    def mutate(ind):
        for i in range(len(ind)):
            if rng.random() < pm:
                ind[i] += rng.normal(0.0, mutation_sigma)
        ind[0] = np.clip(ind[0], x_bounds[0], x_bounds[1])
        ind[1] = np.clip(ind[1], y_bounds[0], y_bounds[1])
        return ind

    best_ind = None
    best_fit = -np.inf

    for gen in range(n_generations):
        fit = evaluate_population(pop)

        gen_best_i = np.argmax(fit)
        if fit[gen_best_i] > best_fit:
            best_fit = fit[gen_best_i]
            best_ind = pop[gen_best_i].copy()

        print(f"f = {f(best_ind[0], best_ind[1]):.6f} в точке {best_ind}")

        new_pop = []

        while len(new_pop) < pop_size:
            p1 = tournament_select(pop, fit)
            p2 = tournament_select(pop, fit)

            c1, c2 = crossover(p1, p2)

            c1 = mutate(c1)
            c2 = mutate(c2)

            new_pop.append(c1)
            if len(new_pop) < pop_size:
                new_pop.append(c2)

        pop = np.array(new_pop)

    best_x, best_y = best_ind
    best_value = f(best_x, best_y)
    return best_x, best_y, best_value


if __name__ == "__main__":
    x_opt, y_opt, f_opt = genetic_minimize_beale()
    print(f"Результат x = {x_opt:.5f} y = {y_opt:.5f} f = {f_opt:.8f}")
