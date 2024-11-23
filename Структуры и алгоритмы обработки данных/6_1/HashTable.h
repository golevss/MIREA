#ifndef _3_HASHTABLE_H
#define _3_HASHTABLE_H

#include <iostream>
#include <utility>
#include <fstream>
#include <string>
#include <vector>

typedef int Tkey;
using namespace std;

// ����������� ��������� HashTableBucket ��� �������� �������� ���-�������
struct HashTableBucket {
    Tkey key; // ���� ��������
    int numberRecord; // ����� ������
    bool Popen = false; // ���� ����������� ��������
};

// ����������� ��������� HashTable ��� ���������� ���-�������
struct HashTable {
private:
    HashTableBucket* table; // ��������� �� ������ ��������� ���-�������
    int size; // ������ �������
public:
    // ����������� ��� ������������� ������� ��������� �������
    HashTable(int size) {
        this->size = size;
        table = new HashTableBucket[size];
    }

    // ������� ��� ���������� ���� �� ���������� �����
    int hashFunc(const string& key) {
        int sum = 0;
        for (char c : key) { // ������� �������� �����
            sum += c; // ������� ����� ASCII ����� ��������
        }
        return sum % size; // ����������� ������� �� ������� ����� �� ������ �������
    }

    // ������� ��� ������ ������� �������� �� �����
    int findIndex(int key) {
        return key % size;
    }

    // ������� ��� ���������� ������������ ���������� �������
    float loadFactor() const {
        int count = 0;
        for (int i = 0; i < size; i++) {
            if (table[i].Popen) {
                count++;
            }
        }
        return static_cast<float>(count) / size;
    }

    // ������� ��� ������� �������� � ���-�������
    void insertInHashTable(const int& key, int numberRecord) {
        if (loadFactor() > 0.7) {
            rehashTable();
        }

        int index = findIndex(key);
        while (table[index].Popen) {
            index = (index + 1) / size;
        }
        table[index].key = key;
        table[index].numberRecord = numberRecord;
        table[index].Popen = true;
    }

    // ������� ��� ������ �������� �� ����� � �������
    HashTableBucket findKey(const int& key) {
        int index = findIndex(key);
        while (table[index].Popen) {
            if (table[index].key == key) {
                return table[index];
            }
            index = (index + 1) / size;
        }
        cout << "Key not found" << endl;
        return HashTableBucket();
    }

    // ������� ��� �������� �������� �� ����� �� �������
    void deleteKey(const int& key) {
        int index = findIndex(key);
        while (table[index].Popen) {
            if (table[index].key == key) {
                table[index].Popen = false;
                return;
            }
            index = (index + 1) / size;
        }
        cout << "Key not found" << endl;
    }

    // ������� ��� ������ ����������� ���-�������
    void printHashTable() {
        for (int i = 0; i < size; i++) {
            if (table[i].Popen) {
                cout << "Bucket " << i << " : (Key: " << table[i].key << " , recordNumber: " << table[i].numberRecord << ")" << endl;
            }
            else {
                cout << "----------------�����----------------" << endl;
            }
        }
    }

    // ������� ��� ��������������� �������
    void rehashTable() {
        int new_size = size * 2;
        HashTableBucket* newTable = new HashTableBucket[new_size];
        for (int i = 0; i < size; i++) {
            if (table[i].Popen) {
                int key = table[i].key;
                int recordNumber = table[i].numberRecord;
                int newIndex = findIndex(key) % new_size;
                while (newTable[newIndex].Popen) {
                    newIndex = (newIndex + 1) % new_size;
                }
                newTable[newIndex].key = key;
                newTable[newIndex].numberRecord = recordNumber;
                newTable[newIndex].Popen = true;
            }
        }
        delete[] table;
        table = newTable;
        size = new_size;
    }
};

#endif //_3_HASHTABLE_H