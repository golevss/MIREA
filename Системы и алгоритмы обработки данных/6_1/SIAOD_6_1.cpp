#include "hash_table.hpp"
#include "file_to_hash.hpp"

// Определение структуры HashTableBucket для хранения элемента хеш-таблицы
struct HashTableBucket
{
    unsigned long int key = 0;
    int numberRecord = 0;
    bool flag = false;
};

// Определение структуры HashTable для реализации хеш-таблицы
struct HashTable
{
private:
    HashTableBucket* table;
    int size = 0;
public:
    // Конструктор для инициализации таблицы заданного размера
    HashTable(int size) {
        this->size = size;
        this->table = new HashTableBucket[size];
    }

    //Первая хэш-функция
    int firstFunc(unsigned long int key)
    {
        return key / this->size;
    }

    //Вторая хэш-функция
    int secondFunc(unsigned long int key)
    {
        return 1 + (key / (this->size - 2));
    }

    // Функция вставки в таблицу
    void insertBucket(unsigned long int key, int numb)
    {
        int index = firstFunc(key);
        int index_2 = secondFunc(key);
        int i = 0;
        while (this->table[index].flag)
        {
            index = index + i * index_2;
            i++;
            if (index >= this->size)
            {
                reMakeTable();
            }
        }

        this->table[index].key = key;
        this->table[index].numberRecord = numb;
        this->table[index].flag = true;
    }

    // Функция поиска в таблице
    int findBucket(unsigned long int key)
    {
        int index = firstFunc(key);
        int index_2 = secondFunc(key);
        int i = 0;
        while (this->table[index].key != key)
        {
            index = index + i * index_2;
            i++;
        }
        if (this->table[index].key == key)
        {
            return index;
        }
        else
        {
            return -1;
        }
    }
    void reMakeTable()
    {
        int new_size = this->size * 2;
        HashTableBucket* newTable = new HashTableBucket[new_size];
        for (int i = 0; i < this->size; i++)
        {
            if (table[i].flag)
            {
                unsigned long int key = table[i].key;
                int numberRecord = table[i].numberRecord;
                int newIndex = firstFunc(key);
                int newIndex_2 = secondFunc(key);
                int i = 0;
                while (this->table->flag)
                {
                    newIndex = newIndex + i * newIndex_2;
                    i++;
                }
                newTable[newIndex].key = key;
                newTable[newIndex].numberRecord = numberRecord;
                newTable[newIndex].flag = true;
            }
        }
        delete[] table;
        this->table = newTable;
        this->size = new_size;
    }
};

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    const char* textFileName = "data.txt";

    std::ifstream inputFile(textFileName);
    int i = 0;
    std::vector<s_book> vec;
    s_book record;

    while (inputFile >> record.ISBN >> record.author >> record.name)
    {
        vec.push_back(record);
        i++;
    }

    HashTable HashTableHashTable(i);
    for (int in = 0; in < i; in++)
    {
        HashTable.insertBucket(charToInt(vec[in].ISBN), in);
    }

    int number;
    std::cout << "Выведите номер записи: ";
    std::cin >> number;
    HashTable.findBucket(number);
}