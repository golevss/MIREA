#include <iostream>
#include <string>
#include <queue>
#include <vector>
#include <tuple>
#include <unordered_map>
#include <algorithm>
#include <fstream>


std::vector<std::tuple<int, int, char>> lz77_compress(const std::string& input)
{
	std::vector<std::tuple<int, int, char>> output;
	int i = 0;

	while (i < input.length())
	{
		int match_length = 0;
		int match_position = 0;

		for (int j = 0; j < i; j++)
		{
			int length = 0;
			while (i + length < input.length() && input[j + length] == input[i + length] && (j + length) < i)
				length++;

			if (length > match_length)
			{
				match_length = length;
				match_position = i - j; 
			}
		}
		char next_char = (i + match_length < input.length()) ? input[i + match_length] : '\0';
		output.emplace_back(match_position, match_length, next_char);
		i += match_length + 1;
	}

	return output;
}

void print_compressed_77(const std::vector<std::tuple<int, int, char>>& compressed)
{
	std::cout << "Data:" << std::endl;
	for (int i = 0; i < compressed.size(); i++) 
		std::cout << "(" << std::get<0>(compressed[i]) << ", " << std::get<1>(compressed[i]) << ", " << std::get<2>(compressed[i]) << ")" << std::endl;
}

std::string lz77_decompress(const std::vector<std::tuple<int, int, char>>& compressed)
{
	std::string output;

	for (int i = 0; i < compressed.size(); i++)
	{
		int start = output.length() - std::get<0>(compressed[i]);

		for (int j = 0; j < std::get<1>(compressed[i]); j++)
			output += output[start + j];

		if (std::get<2>(compressed[i]) != '\0') 
			output += std::get<2>(compressed[i]);
	}

	return output;
}
//===============================================================================================
//===============================================================================================
//===============================================================================================
std::vector<std::tuple<int, char>> lz78_compress(const std::string& input)
{
	std::vector<std::tuple<int, char>> output;
	std::unordered_map<std::string, int> dictionary;
	std::string current;
	int index = 1;

	for (char c : input)
	{
		current += c;
		if (dictionary.find(current) == dictionary.end()) 
		{
			int prev_index = (current.length() > 1) ? dictionary[current.substr(0, current.length() - 1)] : 0;
			output.emplace_back(prev_index, c);
			dictionary[current] = index++;
			current.clear();
		}
	}

	if (!current.empty())
	{
		int prev_index = (current.length() > 1) ? dictionary[current.substr(0, current.length() - 1)] : 0;
		output.emplace_back(prev_index, current[0]);
	}

	return output;
}

void print_compressed_78(const std::vector<std::tuple<int, char>>& compressed)
{
	std::cout << "Data:" << std::endl;
	for (int i = 0; i < compressed.size(); i++)
		std::cout << "(" << std::get<0>(compressed[i]) << ", '" << std::get<1>(compressed[i]) << "')" << std::endl;
}

std::string lz78_decompress(const std::vector<std::tuple<int, char>>& compressed)
{
	std::string output = "";
	std::unordered_map<int,std::string> dictionary;
	int index = 1;

	for (int i = 0; i < compressed.size(); i++)
	{

		if (std::get<0>(compressed[i]) == 0)
		{
			dictionary[index] = std::get<1>(compressed[i]);
		}
		else
		{
			output += dictionary[std::get<0>(compressed[i])];
			dictionary[index] = dictionary[std::get<0>(compressed[i])] + std::get<1>(compressed[i]);
		}
		output += std::get<1>(compressed[i]);
		index++;
	}

	return output;
}
//===============================================================================================
//===============================================================================================
//===============================================================================================
struct Symbol {
	char character;
	int frequency;

	Symbol(char c, int f) : character(c), frequency(f) {}
};

bool compare(const Symbol& a, const Symbol& b) {
	return a.frequency > b.frequency;
}

void shannon_fano_encode(std::vector<Symbol>& symbols, std::unordered_map<char, std::string>& codes, std::string prefix = "") {
	if (symbols.size() == 1)
	{
		codes[symbols[0].character] = prefix;
		return;
	}

	int total_frequency = 0;
	for (const auto& s : symbols) 
		total_frequency += s.frequency;

	int cumulative_frequency = 0;
	int split_index = 0;
	
	for (int i = 0; i < symbols.size(); i++)
	{
		cumulative_frequency += symbols[i].frequency;
		if (cumulative_frequency >= total_frequency / 2)
		{
			split_index = i;
			break;
		}
	}

	std::vector<Symbol> symbolsL(symbols.begin(), symbols.begin() + split_index + 1);
	std::vector<Symbol> symbolsR(symbols.begin() + split_index + 1, symbols.end());
	shannon_fano_encode(symbolsL, codes, prefix + "0");
	shannon_fano_encode(symbolsR, codes, prefix + "1");
}

std::string encode_string(const std::string& input, const std::unordered_map<char, std::string>& codes) {
	std::string encoded = "";
	for (char c : input)
		encoded += codes.at(c);
	return encoded;
}

std::string decode_string(const std::string& input, const std::unordered_map<char, std::string>& codes) {
	std::string decoded = "";
	std::string current = "";
	for (int i = 0; i <input.size();i++)
	{
		current += input[i];
		for (const auto& el : codes)
		{
			if (el.second == current)
			{
				decoded += el.first;
				current.clear();
			}
		}
	}
	return decoded;
}

std::string start_shannon(std::string& input)
{
	std::unordered_map<char, int> frequency_map;
	for (char c : input)
		frequency_map[c]++;
	
	std::vector<Symbol> symbols;
	for (const auto& pair : frequency_map)
		symbols.emplace_back(pair.first, pair.second);

	sort(symbols.begin(), symbols.end(), compare);
	std::unordered_map<char, std::string> codes;

	shannon_fano_encode(symbols, codes);
	//std::cout << "Коды символов:" << std::endl;
	//for (const auto& pair : codes)
	//	std::cout << "'" << pair.first << "' -> " << pair.second << std::endl;

	//std::cout << "Закодированная строка: " << encode_string(input, codes) << std::endl;
	return encode_string(input, codes);
}
//===============================================================================================
//===============================================================================================
//===============================================================================================

struct Node
{
	char character;
	int frequency;
	Node* left;
	Node* right;

	Node(char c, int f) : character(c), frequency(f), left(nullptr), right(nullptr) {}
};

// Сравнитель для приоритетной очереди
struct Compare
{
	bool operator()(Node* left, Node* right)
	{
		return left->frequency > right->frequency;
	}
};

void generate_сodes(Node* root, const std::string& code, std::unordered_map<char, std::string>& codes)
{
	if (!root) return;

	if (!root->left && !root->right) 
		codes[root->character] = code;

	generate_сodes(root->left, code + "0", codes);
	generate_сodes(root->right, code + "1", codes);
}

std::string huffman_encode(const std::string& input)
{
	std::unordered_map<char, int> frequency;
	for (char c : input) 
		frequency[c]++;

	std::priority_queue<Node*, std::vector<Node*>, Compare> minHeap;

	for (const auto& pair : frequency) 
		minHeap.push(new Node(pair.first, pair.second));

	while (minHeap.size() > 1)
	{
		Node* left = minHeap.top();
		minHeap.pop();
		Node* right = minHeap.top();
		minHeap.pop();

		Node* newNode = new Node('\0', left->frequency + right->frequency);
		newNode->left = left;
		newNode->right = right;

		minHeap.push(newNode);
	}

	Node* root = minHeap.top();

	std::unordered_map<char, std::string> codes;
	generate_сodes(root, "", codes);

	std::string encodedString = "";
	for (char c : input) 
		encodedString += codes[c];

	return encodedString;
}
//===============================================================================================
//===============================================================================================
//===============================================================================================

double comporator(const std::string& originalString, const std::string& encodedString) {
	// Размер исходных данных в битах (каждый символ занимает 8 бит)
	int originalSize = originalString.size() * 8;

	// Размер сжатых данных в битах (длина закодированной строки)
	int compressedSize = encodedString.size();

	// Вычисление процента сжатия
	double compressionRatio = ((double)compressedSize / originalSize);

	return compressionRatio;
}
int main()
{
	setlocale(LC_ALL, "RUS");

	int cmd = 0;

	std::string input77 = "000110111011101010111110101110001001";
	std::vector<std::tuple<int, int, char>> compressed77 = lz77_compress(input77);

	std::string input78 = "sarsalsarsanlasanl";
	std::vector<std::tuple<int, char>> compressed78 = lz78_compress(input78);

	std::string input = "Мой котёнок очень странный, Он не хочет есть сметану, К молоку не прикасался И от рыбки отказался.";
	std::string input1 = "Голев Семён Сергеевич";
	std::string input2 = "";
	std::string record;
	std::string output;

	std::ifstream inputFile("data.txt");
	while (inputFile >> record)
	{
		input2 += record + ' ';
	}
	inputFile.close();

	while (true)
	{
		std::cout << "Commands: " << std::endl << "\t1. LZ77" << std::endl << "\t2. LZ78" << std::endl << "\t3. Шеннон" << std::endl << "\t4. Хаффман" << std::endl;
		std::cin >> cmd;
		switch (cmd)
		{
		case 1:
			print_compressed_77(compressed77);
			std::cout << "input:  " << input77 << std::endl;
			std::cout << "output: " << lz77_decompress(compressed77) << std::endl;
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		case 2:
			print_compressed_78(compressed78);
			std::cout << "input:  " << input78 << std::endl;
			std::cout << "output: " << lz78_decompress(compressed78) << std::endl;
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		case 3:
			output = start_shannon(input2);
			std::cout<<comporator(input2, output)<<std::endl;
			std::cout << "input size:  " << input2.size() << std::endl;
			std::cout << "output size: " << output.size() << std::endl;
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		case 4:
			output = huffman_encode(input1);
			std::cout << comporator(input1,output) << std::endl;
			std::cout << "input size:  " << input1 << std::endl;
			std::cout << "output size: " << output << std::endl;
			std::cout << std::endl;
			system("pause");
			std::cout << std::endl;
			break;
		default:
			return 0;
		}
	}
	return 0;
}