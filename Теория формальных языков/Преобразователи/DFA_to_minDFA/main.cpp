#include <iostream>
#include <sstream>

#include <vector>
#include <set>
#include <algorithm>

struct Transition
{
	int from;
	int to;
	char symbol;
	bool flag = false;

	Transition(int f, int t, char s) : from(f), to(t), symbol(s) {}
	void changeTransition(int f, int t, char s)
	{
		this->from = f;
		this->to = t;
		this->symbol = s;
	}
};

struct sDFA
{
	int startState;
	std::set<int> states;
	std::set<int> acceptStates;
	std::vector<Transition> transitions;

	sDFA() : startState(-1) {}
};

void mainFunc(sDFA FA);
bool areTransitionsEqual(int state1, int state2, const sDFA& dfa);
bool areTransitionsEqualInClusters(int state1, int state2, std::vector<std::vector<int>> clusters, const sDFA& dfa);
void delEmptyClasters(std::vector <std::vector<int>>& clusters);

std::vector <std::vector<int>> splitMainCluster(sDFA FA);
std::vector <std::vector<int>> processClusters(std::vector<std::vector<int>>& clusters, const sDFA& dfa);
std::vector<std::vector<int>> mergeSingleElementClusters(std::vector<std::vector<int>> clusters, const sDFA& dfa);

void readDFA(sDFA& dfa);
void printDFA(sDFA dfa);
void printMinDFA(std::vector <std::vector<int>> clusters);

void mainFunc(sDFA FA)
{
	printDFA(FA);
	std::vector <std::vector<int>> clusters = {};
	clusters = splitMainCluster(FA);
	delEmptyClasters(clusters);
	clusters = processClusters(clusters, FA);
	delEmptyClasters(clusters);
	clusters = mergeSingleElementClusters(clusters, FA);
	delEmptyClasters(clusters);
	printMinDFA(clusters);
}

std::vector <std::vector<int>> splitMainCluster(sDFA FA)
{
	std::vector <std::vector<int>> clusters;
	clusters.resize(2);

	for (const auto state : FA.states)
		if (FA.acceptStates.find(state) != FA.acceptStates.end())
			clusters[1].push_back(state);
		else
			clusters[0].push_back(state);

	return clusters;
}

bool areTransitionsEqual(int state1, int state2, const sDFA& dfa)
{
	int pubCounter = 0;
	int counter = 0;
	for (const auto& transition1 : dfa.transitions)
		if (transition1.from == state1)
			for (const auto& transition2 : dfa.transitions)
				if (transition2.from == state2)
					if (transition1.symbol == transition2.symbol)
					{
						if (transition1.to == transition2.to)
							counter++;
						pubCounter++;
					}

	return pubCounter == counter;
}

std::vector <std::vector<int>> processClusters(std::vector<std::vector<int>>& clusters, const sDFA& dfa)
{
	std::vector<std::vector<int>> buffClusters;
	std::vector<int> firstBuffClusters;
	auto& firstCluster = clusters[0];

	for (auto it = firstCluster.begin(); it != firstCluster.end();)
	{
		int elem = *it;
		std::vector<int> buffCluster = { elem };

		for (auto jt = firstCluster.begin(); jt != firstCluster.end();)
		{
			if (elem != *jt && areTransitionsEqual(elem, *jt, dfa))
			{
				buffCluster.push_back(*jt);
				jt = firstCluster.erase(jt);
			}
			else
			{
				jt++;
			}
		}
		buffClusters.push_back(buffCluster);
		it = firstCluster.erase(it);
	}

	for (const auto buffCluster : buffClusters)
		clusters.push_back(buffCluster);

	return clusters;
}

bool areTransitionsEqualInClusters(int state1, int state2, std::vector<std::vector<int>> clusters, const sDFA& dfa)
{
	int pubCounter = 0;
	int counter = 0;
	for (const auto& transition1 : dfa.transitions)
		if (transition1.from == state1)
			for (const auto& transition2 : dfa.transitions)
				if (transition2.from == state2)
					if (transition1.symbol == transition2.symbol)
					{
						for (size_t i = 1; i < clusters.size(); ++i)
							if (std::find(clusters[i].begin(), clusters[i].end(), transition1.to) != clusters[i].end() && std::find(clusters[i].begin(), clusters[i].end(), transition2.to) != clusters[i].end())
								counter++;
						pubCounter++;
					}

	return pubCounter == counter;
}

std::vector<std::vector<int>> mergeSingleElementClusters(std::vector<std::vector<int>> clusters, const sDFA& dfa)
{

	for (size_t i = 1; i < clusters.size(); ++i)
	{
		if (clusters[i].size() != 1) continue;
		int elem1 = clusters[i][0];

		for (size_t j = i + 1; j < clusters.size(); ++j)
		{
			if (clusters[j].size() != 1) continue;
			int elem2 = clusters[j][0];

			if (areTransitionsEqualInClusters(elem1, elem2, clusters, dfa))
			{
				clusters[i].push_back(elem2);
				clusters.erase(clusters.begin() + j);
				j--;
			}
		}
	}

	return clusters;
}

void delEmptyClasters(std::vector <std::vector<int>>& clusters)
{
	for (int i = 0; i < clusters.size(); i++)
		if (clusters[i].empty())
			clusters.erase(clusters.begin() + i);
}

void printDFA(sDFA dfa)
{
	std::cout << "\t====== ДКА =====" << std::endl;
	std::cout << "Начальное состояние [ " << dfa.startState << " ]" << std::endl << std::endl;

	std::cout << "Конечные состояния  [ ";
	if (dfa.acceptStates.size() > 1)
		for (const auto elem : dfa.acceptStates)
			std::cout << elem << "; ";
	else
		for (const auto elem : dfa.acceptStates)
			std::cout << elem << " ";
	std::cout << "]" << std::endl << std::endl;

	std::cout << "Состояния ";
	for (const auto elem : dfa.states)
		std::cout << "{ " << elem << " } ";

	std::cout << std::endl << std::endl << "Переходы: " << std::endl;
	for (const auto elem : dfa.transitions)
		std::cout << elem.from << " --'" << elem.symbol << "'-> " << elem.to << std::endl;

	std::cout << std::endl << std::endl;
}

void printMinDFA(std::vector <std::vector<int>> clusters)
{

	std::cout << "\t==== minДКА ====" << std::endl;
	std::cout << "Начальное состояние [ ";
	for (const auto elem : clusters[1])
		std::cout << elem << ' ';
	std::cout << "]" << std::endl << std::endl;

	std::cout << "Конечное состояние  [ ";
	for (const auto elem : clusters[0])
		std::cout << elem << ' ';
	std::cout << "]" << std::endl << std::endl;

	std::cout << "Состояния ";
	for (const auto elems : clusters)
	{
		std::cout << "{ ";
		for (const auto elem : elems)
			std::cout << elem << ' ';
		std::cout << "} ";
	}
	std::cout << std::endl;
}

void readDFA(sDFA& dfa)
{
	std::string input;

	std::cout << "Введите все состояния (например, 1 2 3 4):" << std::endl;
	std::getline(std::cin, input);
	std::istringstream statesStream(input);
	int state;
	while (statesStream >> state)
		dfa.states.insert(state);

	std::cout << "Введите переходы (например, (1,1,'1') (1,1,'0')):" << std::endl;
	std::getline(std::cin, input);
	std::istringstream transitionsStream(input);
	std::string transition;

	while (std::getline(transitionsStream, transition, ')'))
	{
		if (transition.empty()) continue;

		size_t pos = transition.find('(');
		if (pos != std::string::npos)
			transition = transition.substr(pos + 1);

		int from, to;
		char symbol;
		char comma;

		std::istringstream transStream(transition);
		transStream >> from >> comma >> to >> comma >> symbol;

		dfa.transitions.emplace_back(from, to, symbol);
	}

	std::cout << "Введите начальное состояние:" << std::endl;
	std::cin >> dfa.startState;

	std::cout << "Введите конечные состояния (например, 2 3 4):" << std::endl;
	int acceptState;
	while (std::cin >> acceptState)
	{
		dfa.acceptStates.insert(acceptState);
		if (std::cin.peek() == '\n') break;
	}
}

int main()
{
	setlocale(LC_ALL, "RUS");
	sDFA main;
	readDFA(main);
	mainFunc(main);
}

