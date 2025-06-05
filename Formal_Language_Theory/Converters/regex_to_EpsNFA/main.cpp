#include <iostream>
#include <fstream>
#include <string>

#include <vector>
#include <stack>

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

struct StartNFA
{
	int startState;
	int acceptState;
	std::vector<Transition> transitions;

	StartNFA() : startState(-1), acceptState(-1) {}
};

StartNFA createNFAForSymbol(char symbol, int& stateCount);
StartNFA concatenateNFA(const StartNFA& nfa1, const StartNFA& nfa2);
StartNFA alternatNFA(const StartNFA& nfa1, const StartNFA& nfa2, int& stateCount);
StartNFA kleeneStarNFA(const StartNFA& nfa, int& stateCount);
StartNFA buildNFA(const std::string& regex, int& stateCount, size_t& pos);
void visualizeEpsNFA(const StartNFA& nfa, const char* pngName);

StartNFA createNFAForSymbol(char symbol, int& stateCount)
{
	StartNFA nfa;
	nfa.startState = stateCount++;
	nfa.acceptState = stateCount++;
	nfa.transitions.push_back(Transition(nfa.startState, nfa.acceptState, symbol));
	return nfa;
}

StartNFA concatenateNFA(const StartNFA& nfa1, const StartNFA& nfa2)
{
	StartNFA nfa;
	nfa.startState = nfa1.startState;
	nfa.acceptState = nfa2.acceptState;

	nfa.transitions = nfa1.transitions;
	nfa.transitions.insert(nfa.transitions.end(), nfa2.transitions.begin(), nfa2.transitions.end());
	nfa.transitions.push_back(Transition(nfa1.acceptState, nfa2.startState, '$'));

	return nfa;
}

StartNFA alternatNFA(const StartNFA& nfa1, const StartNFA& nfa2, int& stateCount)
{
	StartNFA nfa;
	nfa.startState = stateCount++;
	nfa.acceptState = stateCount++;

	nfa.transitions.push_back(Transition(nfa.startState, nfa1.startState, '$'));
	nfa.transitions.push_back(Transition(nfa.startState, nfa2.startState, '$'));

	nfa.transitions.insert(nfa.transitions.end(), nfa1.transitions.begin(), nfa1.transitions.end());
	nfa.transitions.insert(nfa.transitions.end(), nfa2.transitions.begin(), nfa2.transitions.end());

	nfa.transitions.push_back(Transition(nfa1.acceptState, nfa.acceptState, '$'));
	nfa.transitions.push_back(Transition(nfa2.acceptState, nfa.acceptState, '$'));

	return nfa;
}

StartNFA kleeneStarNFA(const StartNFA& nfa, int& stateCount)
{
	StartNFA resultNFA;
	resultNFA.startState = stateCount++;
	resultNFA.acceptState = stateCount++;

	resultNFA.transitions.push_back(Transition(resultNFA.startState, nfa.startState, '$'));
	resultNFA.transitions.push_back(Transition(resultNFA.startState, resultNFA.acceptState, '$'));

	resultNFA.transitions.insert(resultNFA.transitions.end(), nfa.transitions.begin(), nfa.transitions.end());

	resultNFA.transitions.push_back(Transition(nfa.acceptState, nfa.startState, '$'));
	resultNFA.transitions.push_back(Transition(nfa.acceptState, resultNFA.acceptState, '$'));

	return resultNFA;
}

StartNFA buildNFA(const std::string& regex, int& stateCount, size_t& pos)
{
	std::stack<StartNFA> nfaStack;

	while (pos < regex.size())
	{
		char current = regex[pos];

		if (isalnum(current))
		{
			nfaStack.push(createNFAForSymbol(current, stateCount));
		}
		else if (current == '|')
		{
			pos++;
			StartNFA rightNFA = buildNFA(regex, stateCount, pos);
			StartNFA leftNFA = nfaStack.top(); nfaStack.pop();
			nfaStack.push(alternatNFA(leftNFA, rightNFA, stateCount));
			continue;
		}
		else if (current == '.')
		{
			pos++;
			StartNFA rightNFA = buildNFA(regex, stateCount, pos);
			StartNFA leftNFA = nfaStack.top(); nfaStack.pop();
			nfaStack.push(concatenateNFA(leftNFA, rightNFA));
			continue;
		}
		else if (current == '*')
		{
			pos++;
			StartNFA innerNFA = nfaStack.top(); nfaStack.pop();
			nfaStack.push(kleeneStarNFA(innerNFA, stateCount));
			continue;
		}
		pos++;
	}

	return nfaStack.top();
}

void visualizeEpsNFA(const StartNFA& nfa, const char* pngName)
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

	out << "  " << nfa.acceptState << " [shape=doublecircle];" << std::endl;
	out << "}" << std::endl;
	out.close();

	system(pngName);
}

int main()
{
	setlocale(LC_ALL, "RUS");

	std::string regex = "a*.c.a.a|b";

	int stateCount = 0;
	size_t pos = 0;
	StartNFA EpsilonNFA = buildNFA(regex, stateCount, pos);
	const char* pngName_1 = "dot -Tpng nfa.dot -o pic_EpsNFA.png";
	visualizeEpsNFA(EpsilonNFA, pngName_1);
}