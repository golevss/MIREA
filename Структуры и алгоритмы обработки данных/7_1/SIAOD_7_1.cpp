#include <iostream>
#include <vector>
#include <iomanip>

struct binTree{

	struct Node {
		int data;
		Node* left;
		Node* right;

		Node(int value) : data(value), left(nullptr), right(nullptr) {}
	};

	Node* root;
	float globSum = 0;
	float globSize = 0;
	bool insFlag = true;

	binTree() : root(nullptr) {}
	binTree(int a)
	{
		root = nullptr;
		insert(5);
		insert(3);
		insert(7);
		insert(2);
		insert(4);
		insert(6);
		insert(9);
	}

	void insert(int value)                  { root = insert(root, value); }
	Node* search(int value)                 { return search(root, value); }
	void remove(Node* node,int value)       { remove_pr(node, value); }
	void display_line()     { display_line(root); }
	void display()          { display(root); }
	float average()         { average(root); return globSum / globSize; }
	int node_count()        { average(root); return globSize; }
	int max_el()            { return max_el(root); }

private:

	Node* insert(Node* node, int value)
	{
		if (node == nullptr)
		{
			return new Node(value);
		}
		if (search(node,value))
		{
			std::cout << "Повторная вставка" << std::endl;
			return root;
		}
		if (value < node->data)
		{
			node->left = insert(node->left, value);
		}
		else {
			node->right = insert(node->right, value);
		}
		return node;
	}

	Node* search(Node* node, int value)
	{
		if (node == nullptr || node->data == value)
		{
			return node; 
		}
		if (value < node->data) {
			return search(node->left, value); 
		}
		else {
			return search(node->right, value); 
		}
	}

	void remove_pr(Node* node, int value)
	{
		if (node != nullptr)
		{
			if (node->data != value)
				insert(node->data);
			remove_pr(node->left, value);
			remove_pr(node->right, value);
		}
	}

	void display_line(Node* root)
	{
		if (root != nullptr)
		{
			display_line(root->left);
			std::cout << root->data << " ";
			display_line(root->right);
		}
	}

	void display(Node* node, int space = 0, int level = 0)
	{
		int count = 5; 
		if (node == nullptr) return; 

		space += count;

		display(node->right, space, level + 1);

		std::cout << std::endl;
		for (int i = count; i < space; i++) {
			std::cout << " ";
		}
		std::cout << node->data << "\n";

		display(node->left, space, level + 1);
	}

	void average(Node* node)
	{
		globSum = 0;
		globSum += node->data;
		globSize = 1;
		traversal(node);
	}

	void traversal(Node* node)
	{
		if (node == nullptr) return;
		if (node->left != nullptr)
		{
			globSum += (node->left->data);
			globSize++;
		}
		if (node->right != nullptr)
		{
			globSum += (node->right->data);
			globSize++;
		}
		traversal(node->left);
		traversal(node->right);
	}
	int max_el(Node* node)
	{
		if (node->right != nullptr)
			return max_el(node->right);
		else
			return node->data;
	}
};

struct BTree {
	struct BTreeNode {
		std::vector<int> keys;
		std::vector<BTreeNode*> children;
		int t;
		bool isLeaf;

		BTreeNode(int _t, bool _isLeaf) {
			t = _t;
			isLeaf = _isLeaf;
			keys.reserve(2 * t - 1);
			children.reserve(2 * t);
		}
	};
	int maxEl = 0;
	int minEl = 1000000;
	BTreeNode* root;
	int t;

	BTree(int _t)
	{
		root = nullptr;
		t = _t;

		insert(10);
		insert(20);
		insert(5);
		insert(6);
		insert(12);
		insert(30);
		insert(7);
		insert(17);
		insert(1);
		insert(3);
	}

	void insert(int key)
	{
		if (search(root,key))
		{
			std::cout << "Повторная вставка" << std::endl;
			return;
		}
		if (root == nullptr)
		{
			root = new BTreeNode(t, true);
			root->keys.push_back(key);
		}
		else
		{
			if (root->keys.size() == 2 * t - 1)
			{
				BTreeNode* newRoot = new BTreeNode(t, false);
				newRoot->children.push_back(root);
				split_child(newRoot, 0, root);
				root = newRoot;
			}
			insert_non_full(root, key);
		}
	}

	BTreeNode* search(int key){ return search(root, key); }

	BTreeNode* remove(int key){ return remove(root, key); }

	void display() {
		if (root != nullptr)
			display(root,0);
	}

	int find_levels() { return find_levels(root); }

	BTreeNode* max_node() { return max_node(root); }

	int max_min() { maxEl = 0; minEl = 1000000; max_min(root); return maxEl - minEl; }

private:
	BTreeNode* remove(BTreeNode* node, int key)
	{
		if (node == nullptr) return nullptr;

		int i = 0;
		while (i < node->keys.size() && key > node->keys[i])
			i++;

		if (i < node->keys.size() && key == node->keys[i])
			node->keys.erase(node->keys.begin() + i);

		if (node->isLeaf)
			return nullptr;

		return remove(node->children[i], key);
	}

	BTreeNode* search(BTreeNode* node, int key)
	{
		if (node == nullptr) return nullptr;

		int i = 0;
		while (i < node->keys.size() && key > node->keys[i])
			i++;

		if (i < node->keys.size() && key == node->keys[i])
			return node;

		if (node->isLeaf)
			return nullptr;

		return search(node->children[i], key);
	}

	void display(BTreeNode* node, int depth)
	{
		int i;
		std::cout << std::setw(depth * 4) << " " << "+--";
		std::cout << '[';
		for (i = 0; i < node->keys.size(); i++)
		{
			std::cout << node->keys[i];
			if (i != node->keys.size() - 1)
				std::cout<< '|';
		}
		std::cout << "] ";
		std::cout << std::endl;
		for (i = 0; i < node->children.size(); i++)
		{
			if (!node->isLeaf)
			{
				display(node->children[i],depth + 1);
			}
		}
		
	}

	void insert_non_full(BTreeNode* node, int key)
	{
		int i = node->keys.size() - 1;

		if (node->isLeaf)
		{
			node->keys.push_back(0);
			while (i >= 0 && key < node->keys[i])
			{
				node->keys[i + 1] = node->keys[i];
				i--;
			}
			node->keys[i + 1] = key;
		}
		else
		{
			while (i >= 0 && key < node->keys[i])
				i--;

			if (node->children[i + 1]->keys.size() == 2 * t - 1)
			{
				split_child(node, i + 1, node->children[i + 1]);
				if (key > node->keys[i + 1])
					i++;
			}
			insert_non_full(node->children[i + 1], key);
		}
	}

	void split_child(BTreeNode* parent, int i, BTreeNode* child)
	{
		BTreeNode* newNode = new BTreeNode(t, child->isLeaf);

		for (int j = 0; j < t - 1; j++) 
			newNode->keys.push_back(child->keys[j + t]);

		if (!child->isLeaf)
			for (int j = 0; j < t; j++)
				newNode->children.push_back(child->children[j + t]);

		parent->children.insert(parent->children.begin() + i + 1, newNode);
		parent->keys.insert(parent->keys.begin() + i, child->keys[t - 1]);

		child->keys.resize(t - 1);
		child->children.resize(t);
	}

	int find_levels(BTreeNode* node)
	{
		if (node == nullptr)
			return 0;
		int Height = 0;
		for (int i = 0; i < node->children.size(); i++)
		{
			Height = std::max(Height,find_levels(node->children[i]));
		}
		return Height + 1;
	}

	BTreeNode* max_node(BTreeNode* node)
	{
		if (!(node->isLeaf))
		{
			for (int i = 0; i < node->children.size(); i++)
			{
				if (i + 1 == node->children.size())
					max_node(node->children[i]);
			}
		}
		else
		{
			return node;
		}
	}
	void max_min(BTreeNode* node)
	{
		for (int i = 0; i < node->keys.size(); i++)
		{
			maxEl = std::max(maxEl, node->keys[i]);
			minEl = std::min(minEl, node->keys[i]);
		}
		if (!(node->isLeaf))
			for (int i = 0; i < node->children.size(); i++)
				max_min(node->children[i]);
	}
};

int main()
{
	setlocale(LC_ALL, "RUS");
	
	binTree bst(1);
	binTree buffTree;
	BTree bTree(3);
	int treeCmd = 0;
	int cmd = 0;
	int move = 0;

	std::cout << "1.Бинарное дерево" << std::endl
		<< "2.Cбалансированное дерево поиска" << std::endl;
	std::cin >> treeCmd;
	switch (treeCmd)
	{
	case 1:
		while (true)
		{
			std::cout << "Выберите команду: "
				<< std::endl << "\t1. Вставка;"
				<< std::endl << "\t2. Поиск;"
				<< std::endl << "\t3. Удаление;"
				<< std::endl << "\t4. Вывод (инфиксная форма);"
				<< std::endl << "\t5. Вывод (граф);"
				<< std::endl << "\t6. Нахождение среднего арифметического;"
				<< std::endl << "\t7. Количество узлов;"
				<< std::endl << "\t8. Максимальный элемент дерева"
				<< std::endl << "Команда: ";
			std::cin >> cmd;
			std::cout << std::endl;
			switch (cmd)
			{
			case 1:
				std::cout << "Введите число для вставки: ";
				std::cin >> move;

				bst.insert(move);

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 2:
				std::cout << "Введите число для поиска: ";
				std::cin >> move;

				if (bst.search(move)) {
					std::cout << "Узел с значением " << move << " найден." << std::endl;
				}
				else {
					std::cout << "Узел с значением " << move << " не найден." << std::endl;
				}

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 3:
				std::cout << "Введите число для удаления: ";
				std::cin >> move;

				buffTree.root = nullptr;
				buffTree.remove(bst.root, move);
				bst = buffTree;

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 4:
				bst.display_line();

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 5:
				bst.display();

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 6:
				std::cout << "Среднее арифметическое дерева: " << bst.average() << std::endl;

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 7:
				std::cout << "Количество узлов дерева: " << bst.node_count() << std::endl;

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 8:
				buffTree.root = nullptr;
				buffTree.remove(bst.root, bst.max_el());
				bst = buffTree;
				std::cout << "Максимальный элемент удалён" << std::endl;
				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			default:
				return 0;
			}
		}
	case 2:
		while (true)
		{
			std::cout << "Выберите команду: "
				<< std::endl << "\t1. Вставка;"
				<< std::endl << "\t2. Поиск;"
				<< std::endl << "\t3. Удаление;"
				<< std::endl << "\t4. Вывод (инфиксная форма);"
				<< std::endl << "\t5. Количество уровней;"
				<< std::endl << "\t6. Вернуть узел с максимальным значением;"
				<< std::endl << "\t7. Разница максимального и минимального элементов"
				<< std::endl << "Команда: ";
			std::cin >> cmd;
			std::cout << std::endl;
			switch (cmd)
			{
			case 1:
				std::cout << "Введите число для вставки: ";
				std::cin >> move;

				bTree.insert(move);

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 2:
				std::cout << "Введите число для поиска: ";
				std::cin >> move;

				if (bTree.search(move)) {
					std::cout << "Узел с значением " << move << " найден." << std::endl;
				}
				else {
					std::cout << "Узел с значением " << move << " не найден." << std::endl;
				}

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 3:
				std::cout << "Введите число для удаления: ";
				std::cin >> move;

				bTree.remove(move);

				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 4:
				std::cout << "Обход дерева: " << std::endl;
				bTree.display();
				std::cout << std::endl;
				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 5:
				std::cout << "Количество уровней дерева: " << bTree.find_levels() << std::endl;
				std::cout << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			case 6:
				std::cout << "Узел с максимальным значением возвращён." << std::endl;
				bTree.max_node();
				system("pause");
				std::cout << std::endl;
				break;
			case 7:
				std::cout << "Разница максимального и минимального элемента: ["<< bTree.max_min() << ']' << std::endl;
				system("pause");
				std::cout << std::endl;
				break;
			default:
				return 0;
			}
		}
	default:
		return 0;
	}
}