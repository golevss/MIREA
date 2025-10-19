import numpy as np
import random

def createGraph(cNodes):    
    structure = {}
    step = 1
    for i in range (cNodes):
        structure[str(i + step)] = [] 

    for i in range (cNodes):
        for j in range (i + 1,cNodes):
            w = np.random.randint(1, 6)

            structure[str(i + step)].append((str(j + step), w))
            structure[str(j + step)].append((str(i + step), w))
    
    return structure, step

def aco_tsp(graph, startNode, num_ants=10, iterations=100, alpha=1):
    nodes = list(graph.keys())
    n = len(nodes)
    
    tau = {i: {j: np.random.uniform(0.1, 1.0) for j, _ in graph[i]} for i in graph}
    eta = {i: {j: 1 / w for j, w in graph[i]} for i in graph}

    best_length = float('inf')
    best_path = None

    for t in range(iterations):
        paths = []
        lengths = []

        for _ in range(num_ants):
            start = str(startNode)
            unvisited = set(nodes)
            unvisited.remove(start)
            path = [start]
            total_dist = 0
            current = start

            while unvisited:
                neighbors = [n for n, _ in graph[current] if n in unvisited]
                if not neighbors:
                    break

                probs = []
                denom = sum((tau[current][j] ** alpha) for j in neighbors)
                for j in neighbors:
                    p = (tau[current][j] ** alpha) / denom
                    probs.append(p)

                next_node = random.choices(neighbors, weights=probs, k=1)[0]
                dist = next(w for wj, w in graph[current] if wj == next_node)
                total_dist += dist
                path.append(next_node)
                unvisited.remove(next_node)
                current = next_node


            if len(path) == n:
                last, first = path[-1], path[0]
                dist = next(w for wj, w in graph[last] if wj == first)
                total_dist += dist
                path.append(first)

            # print(' -> '.join(path))
            # print(total_dist)

            paths.append(path)
            lengths.append(total_dist)

            if total_dist < best_length:
                best_length = total_dist
                best_path = path


        for k in range(num_ants):
            path = paths[k]
            length = lengths[k]
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                tau[a][b] += 1 / length
                tau[b][a] += 1 / length

    return best_path, best_length


if __name__ == '__main__':
    cNodes = 6
    structure, start = createGraph(cNodes)

    path, weight = aco_tsp(structure, startNode=start, num_ants = cNodes)
    print("Кратчайший путь:", ' -> '.join(path))
    print("Длина:", weight) 