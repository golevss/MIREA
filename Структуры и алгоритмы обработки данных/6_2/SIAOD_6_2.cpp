#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <unordered_set>

std::vector<std::string> split_sentence(const std::string& sentence);
std::string reverse_string(const std::string& str);
void find_antigrams(const std::vector<std::string>& words);

std::vector<int> prefix_function(const std::string& pattern);
std::vector<int> KMPsearch(const std::string& text, const std::string& pattern);
int max_prefix(const std::string& a, const std::string& b);

std::vector<std::string> split_sentence(const std::string& sentence)
{
	std::vector<std::string> words;
	std::string word;
	std::stringstream ss(sentence);

	while (std::getline(ss, word, ' '))
	{
		std::stringstream wordStream(word);
		std::string cleanWord;

		while (std::getline(wordStream, cleanWord, ','))
		{
			if (!cleanWord.empty())
			{
				words.push_back(cleanWord);
			}
		}
	}

	return words;
}

std::string reverse_string(const std::string& str)
{
	return std::string(str.rbegin(), str.rend());
}

void find_antigrams(const std::vector<std::string>& words)
{
	std::unordered_set<std::string> wordSet(words.begin(), words.end());
	std::unordered_set<std::string> wordsAnti;

	for (const std::string& word : words)
	{
		std::string reversedWord = reverse_string(word);

		if ((wordSet.find(reversedWord) != wordSet.end() && word != reversedWord) && (wordsAnti.find(word)) == wordsAnti.find(reversedWord))
		{
			wordsAnti.insert(word);
			wordsAnti.insert(reversedWord);
			std::cout << '\t' << word << " - " << reversedWord << " являются антиграммами." << std::endl;
			wordSet.erase(reversedWord);
		}
	}
}

std::vector<int> prefix_function(const std::string& pattern) {
	int m = pattern.length();
	std::vector<int> pi(m, 0);
	int k = 0;

	for (int i = 1; i < m; i++) {
		while (k > 0 && pattern[k] != pattern[i]) {
			k = pi[k - 1];
		}

		if (pattern[k] == pattern[i]) {
			k++;
		}
		pi[i] = k; 
	}
	return pi;
}

std::vector<int> KMPsearch(const std::string& text, const std::string& pattern)
{
	int n = text.length();
	int m = pattern.length();

	std::vector<int> pi = prefix_function(pattern);

	std::vector<int> matchPositions; 
	int j = 0; 
	for (int i = 0; i < n; i++) {
		while (j > 0 && text[i] != pattern[j])
		{
			j = pi[j - 1];
		}

		if (text[i] == pattern[j])
		{
			j++;
		}

		if (j == m)
		{
			matchPositions.push_back(i - m + 1); 
			j = pi[j - 1]; 
		}
	}

	return matchPositions; 
}

int max_prefix(const std::string& text, const std::string& pattern)
{
	std::vector<int> pi = prefix_function(pattern);
	int maxPrefixLength = 0;
	int j = 0; 

	
	for (int i = 0; i < text.length(); i++)
	{
		while (j > 0 && text[i] != pattern[j])
		{
			j = pi[j - 1]; 
		}
		if (text[i] == pattern[j] && i != pattern.length())
		{
			j++;
		}

		
		if (j > maxPrefixLength) {
			maxPrefixLength = j; 
		}
	}
	return maxPrefixLength; 
}


int main()
{
	setlocale(LC_ALL, "RUS");

	int cmd = 0;

	std::string sentence = "А нос упал в сон, кот побежал к току, куст пошел к туку, а мир обернулся в рим и лад обратился в дал";
	std::vector<std::string> words;

	std::string pattern = "abcabd";
	std::string text = "bcabagyhkadcabccbgabddabsadasfasfabcсd";
	int result = 0;

	while (true)
	{
		std::cout << "Выберите задание:"
			<< std::endl << "\t1. Дано предложение, слова в котором разделены пробелами и запятыми.\n\tРаспечатать те слова, которые являются обращениями других слов в этом предложении."
			<< std::endl << "\t2. Даны две строки a и b. Требуется найти максимальную длину префикса строки a,\n\tкоторый входит как подстрока в строку b.При этом считать, что пустая строка является подстрокой любой строки.\n\tРеализация алгоритмом Кнута - Мориса - Пратта."
			<< std::endl << "Команда: ";
		std::cin >> cmd;
		switch (cmd)
		{
		case 1:
			std::cout << "Изначальная строка: " << sentence << std::endl << std::endl;
			words = split_sentence(sentence);
			std::cout << "Антиграммы:" << std::endl;
			find_antigrams(words);
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		case 2:
			std::cout << "\ttext: " << text << std::endl;
			std::cout << "\tpattern: " << pattern << std::endl;
			result = max_prefix(text, pattern);
			std::cout << "\tМаксимальная длина префикса , которая входит в текст: " << result << std::endl << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		default:
			break;
		}
	}
	return 0;
}