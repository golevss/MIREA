#include <iostream>
#include <vector>
#include <iomanip>
#include <limits>

struct Edge {
	int vertex; 
	int weight; 
	Edge(int v, int w) : vertex(v), weight(w) {}
};

struct Graph
{
	int numVertices;
	std::vector<std::vector<Edge>> graphList;
	std::vector<std::vector<int>> dist;
	std::vector<std::vector<int>> next;

	Graph(int vertices) {
		numVertices = vertices;

		graphList.resize(vertices + 1);
		dist.resize(vertices + 1, std::vector<int>(vertices + 1, std::numeric_limits<int>::max()));
		next.resize(vertices + 1, std::vector<int>(vertices + 1, std::numeric_limits<int>::min()));
		for (int i = 0; i <= numVertices; i++)
		{
			dist[i][i] = 0;
			next[i][i] = i;
		}
	}

	void re_size(int vertices)
	{
		graphList.clear();
		dist.clear();
		next.clear();

		numVertices = vertices;

		graphList.resize(vertices + 1);
		dist.resize(vertices + 1, std::vector<int>(vertices + 1, std::numeric_limits<int>::max()));
		next.resize(vertices + 1, std::vector<int>(vertices + 1, std::numeric_limits<int>::min()));

		for (int i = 0; i <= numVertices; i++)
		{
			dist[i][i] = 0;
			next[i][i] = i;
		}
	}
	
	void addEdge(int src, int dest, int weight) {
		graphList[src].emplace_back(dest, weight);
		//adjList[dest].emplace_back(src, weight);
		dist[src][dest] = weight;
		next[src][dest] = dest;
	}

	void print_tree(int vertex, std::vector<bool>& visited, int depth = 0) {
		visited[vertex] = true;

		std::cout << std::setw(depth * 4) << " " << "+--[" << vertex  << ']' << std::endl;

		for (const Edge& edge : graphList[vertex]) {
			if (!visited[edge.vertex]) {
				std::cout << std::setw((depth + 1) * 4) << " " << "| " << edge.weight << std::endl;
				print_tree(edge.vertex, visited, depth + 1);
			}
		}
	}

	void build_tree(int startVertex) {
		std::vector<bool> visited(numVertices + 1, false);
		print_tree(startVertex, visited);
	}

	void floyd()
	{
		for (int k = 1; k <= numVertices; k++) 
			for (int i = 1; i <= numVertices; i++) 
				for (int j = 1; j <= numVertices; j++) 
					if (dist[i][k]!= std::numeric_limits<int>::max() && dist[k][j] != std::numeric_limits<int>::max())
					{
						if (dist[i][j] > dist[i][k] + dist[k][j])
						{
							dist[i][j] = dist[i][k] + dist[k][j];
							next[i][j] = next[i][k];
						}
					}
	}

	int get_path(int src, int dest) {return dist[src][dest];}

	void find_path(int src, int dest)
	{
		if (next[src][dest] == std::numeric_limits<int>::min()) {
			std::cout << "Нет пути между вершинами " << src << " и " << dest << "." << std::endl;
			return;
		}

			std::cout << "Путь между вершинами " << src << " и " << dest << ": ";
			for (int at = src; at != dest; at = next[at][dest]) {
				std::cout << at << " ~ ";
			}
			std::cout << dest << std::endl;
		
	}
};

int main() {
	setlocale(LC_ALL, "RUS");
	
	/*
	* Graph g(6);
	g.addEdge(1, 2, 2);
	g.addEdge(1, 3, 5);
	g.addEdge(2, 5, 10);
	g.addEdge(2, 4, 6);
	g.addEdge(3, 5, 8);
	g.addEdge(3, 4, 9);
	g.addEdge(5, 6, 3);
	g.addEdge(4, 6, 4);
	*/
	Graph g(10);
	g.addEdge(1, 2, 3);
	g.addEdge(1, 3, 4);
	g.addEdge(1, 4, 2);
	g.addEdge(2, 6, 3);
	g.addEdge(3, 6, 6);
	g.addEdge(4, 6, 2);
	g.addEdge(4, 5, 5);
	g.addEdge(5, 7, 6);
	g.addEdge(5, 9, 12);
	g.addEdge(6, 5, 1);
	g.addEdge(6, 7, 8);
	g.addEdge(6, 8, 7);
	g.addEdge(7, 10, 4);
	g.addEdge(8, 10, 3);
	g.addEdge(9, 8, 6);
	g.addEdge(9, 10, 11);

	int cmd = 0;
	int cmd_2 = 0;

	int src = 0;
	int dest = 0;
	int weight = 0;

	while (true)
	{
		std::cout << "Выберите команду: "
			<< std::endl << "\t1. Ввод графа;"
			<< std::endl << "\t2. Вывод графа( результирующее дерево );"
			<< std::endl << "\t3. Нахождение кратчайшего пути;"
			<< std::endl << "\t4. Вывод кратчайшего пути"
			<< std::endl << "Команда: ";
		std::cin >> cmd;
		std::cout << std::endl;
		switch (cmd)
		{
		case 1:
			std::cout << "Введите количество вершин: ";
			std::cin >> cmd_2;
			g.re_size(cmd_2);
			std::cout << "Введите две вершины и вес ребра между ними, для выхода 0 0 0" << std::endl;
			while (true)
			{
				std::cin >> src; std::cin >> dest; std::cin >> weight;
				if (src + dest + weight == 0)
					break;
				g.addEdge(src, dest, weight);
			}
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		case 2:
			std::cout << "Введите вершину: ";
			std::cin >> cmd_2;
			std::cout << "Результирующее дерево для графа (с весами ребер):" << std::endl;
			g.build_tree(cmd_2);
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		case 3:
			std::cout << "Введите две вершины: ";
			std::cin >> src; std::cin >> dest;
			g.floyd();
			if (g.get_path(src, dest) == std::numeric_limits<int>::max()) {
				std::cout << "Нет пути между вершинами " << src << " и " << dest << "." << std::endl;
			}
			else {
				std::cout << "Кратчайший путь между вершинами " << src << " и " << dest << ": " << g.get_path(src, dest) << std::endl;
			}
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		case 4:
			std::cout << "Введите две вершины: ";
			std::cin >> src; std::cin >> dest;
			g.floyd();
			std::cout << std::endl;
			g.find_path(src, dest);
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		default:
			return 0;
		}
	}
}
