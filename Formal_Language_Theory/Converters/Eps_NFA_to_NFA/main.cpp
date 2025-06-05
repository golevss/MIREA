#include <iostream>
#include <fstream>
#include <string>

#include <unordered_set>
#include <unordered_map>
#include <vector>

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

struct NFA
{
	int startState;
	std::unordered_set<int> acceptStates;
	std::vector<Transition> transitions;

	NFA() : startState(-1) {}
};

NFA convertEpsToNon(NFA nfa, int acceptState);
bool checkNonSingleEps(NFA nfa);
void visualizeNFA(const NFA& nfa, const char* pngName);

NFA convertEpsToNon(NFA nfa, int acceptState)
{
	NFA buffNFA;

	while (checkNonSingleEps(nfa))
	{
		for (int i = 0; i < nfa.transitions.size(); i++)
			if (nfa.transitions[i].symbol == '$')
				for (int j = 0; j < nfa.transitions.size(); j++)
					if (nfa.transitions[j].symbol == '$' && nfa.transitions[i].to == nfa.transitions[j].from && i != j && nfa.transitions[j].flag == false)
					{
						Transition buffTransition(nfa.transitions[i].from, nfa.transitions[j].to, '$');
						buffNFA.transitions.push_back(buffTransition);
						nfa.transitions[j].flag = true;
					}
		for (const auto elem : buffNFA.transitions)
			nfa.transitions.push_back(elem);
		buffNFA.transitions = {};
	}

	for (const auto& transition : nfa.transitions)
		if (transition.symbol == '$' && transition.to == acceptState)
			nfa.acceptStates.insert(transition.from);

	buffNFA.transitions = {};
	for (int i = 0; i < nfa.transitions.size(); i++)
	{
		Transition buffTransition(nfa.transitions[i].from, nfa.transitions[i].to, nfa.transitions[i].symbol);
		buffNFA.transitions.push_back(buffTransition);
		if (nfa.transitions[i].symbol == '$')
			for (int j = 0; j < nfa.transitions.size(); j++)
				if (nfa.transitions[j].symbol != '$' && nfa.transitions[i].to == nfa.transitions[j].from)
				{
					Transition buffTransition(nfa.transitions[i].from, nfa.transitions[j].to, nfa.transitions[j].symbol);
					buffNFA.transitions.push_back(buffTransition);
				}
	}
	nfa.transitions = buffNFA.transitions;

	buffNFA.transitions = {};
	for (int i = 0; i < nfa.transitions.size(); i++)
		if (nfa.transitions[i].symbol != '$')
		{
			Transition buffTransition(nfa.transitions[i].from, nfa.transitions[i].to, nfa.transitions[i].symbol);
			buffNFA.transitions.push_back(buffTransition);
		}
	nfa.transitions = buffNFA.transitions;

	buffNFA.transitions = {};
	for (int i = 0; i < nfa.transitions.size(); i++)
		for (int j = 0; j < nfa.transitions.size(); j++)
			if (nfa.transitions[i].from == nfa.startState || nfa.transitions[i].from == nfa.transitions[j].to)
			{
				Transition buffTransition(nfa.transitions[i].from, nfa.transitions[i].to, nfa.transitions[i].symbol);
				buffNFA.transitions.push_back(buffTransition);
				break;
			}
	nfa.transitions = buffNFA.transitions;

	for (const auto& state : nfa.acceptStates)
		for (int j = 0; j < nfa.transitions.size(); j++)
			if (nfa.transitions[j].to == state || nfa.startState == state)
			{
				buffNFA.acceptStates.insert(state);
			}
	nfa.acceptStates = buffNFA.acceptStates;

	return nfa;
}

bool checkNonSingleEps(NFA nfa)
{
	for (int i = 0; i < nfa.transitions.size(); i++)
		if (nfa.transitions[i].symbol == '$')
			for (int j = 0; j < nfa.transitions.size(); j++)
				if (nfa.transitions[j].symbol == '$' && nfa.transitions[i].to == nfa.transitions[j].from && i != j && nfa.transitions[j].flag == false)
					return true;
	return false;
}

void visualizeNFA(const NFA& nfa, const char* pngName)
{
	std::ofstream out("nfa.dot");
	if (!out)
	{
		std::cerr << "Error creating .dot file" << std::endl;
		return;
	}
	out << "digraph NFA {" << std::endl;
	out << "  start [shape=point];" << std::endl;
	out << "  start -> " << nfa.startState << ";" << std::endl;

	for (const auto& transition : nfa.transitions)
		out << "  " << transition.from << " -> " << transition.to << " [label=\"" << (transition.symbol) << "\"];" << std::endl;

	for (const auto& acceptState : nfa.acceptStates)
		out << "  " << acceptState << " [shape=doublecircle];" << std::endl;

	out << "}" << std::endl;
	out.close();

	system(pngName);
}

int main()
{
	NFA nonEpsNFA;

	int acceptState = 5;
	nonEpsNFA.acceptStates.insert(acceptState);
	nonEpsNFA.startState = 0;
	Transition buffTransition(0, 1, '$');
	nonEpsNFA.transitions.push_back(buffTransition);
	buffTransition.changeTransition(0, 2, '$');
	nonEpsNFA.transitions.push_back(buffTransition);
	buffTransition.changeTransition(1, 1, 'a');
	nonEpsNFA.transitions.push_back(buffTransition);
	buffTransition.changeTransition(2, 2, 'b');
	nonEpsNFA.transitions.push_back(buffTransition);
	buffTransition.changeTransition(1, 3, 'b');
	nonEpsNFA.transitions.push_back(buffTransition);
	buffTransition.changeTransition(2, 4, 'a');
	nonEpsNFA.transitions.push_back(buffTransition);
	buffTransition.changeTransition(4, 5, '$');
	nonEpsNFA.transitions.push_back(buffTransition);
	buffTransition.changeTransition(3, 5, '$');
	nonEpsNFA.transitions.push_back(buffTransition);

	const char* pngName_2 = "dot -Tpng nfa.dot -o pic_NFA1.png";
	visualizeNFA(nonEpsNFA, pngName_2);
	nonEpsNFA = convertEpsToNon(nonEpsNFA, acceptState);
	const char* pngName_3 = "dot -Tpng nfa.dot -o pic_NFA2.png";
	visualizeNFA(nonEpsNFA, pngName_3);

	std::cout << "Eps Graph saved in pic_NFA1.png" << std::endl;
	std::cout << "Non eps Graph saved in pic_NFA2.png" << std::endl;
}