#ifndef _3_FILEBYHASH_H
#define _3_FILEBYHASH_H

#include "BinaryFile.h"
#include "HashTable.h"

// ������� ��� �������� ������ �� ����� � ���-�������
void fromFileToHashTab(HashTable& hashtab, int n, const char* bin_name)
{
    cout << "���������� ������: \n";

    // ���������� ���� �� ���� �������� � ���������� ������ � ���-�������
    int key = hashtab.hashFunc(find_by_key(bin_name, n).dateOfBirth);
    hashtab.insertInHashTable(key, n);
}

// ������� ��� �������� ������ �� ���-������� � ����� �� �����
void deleteFromTabnFile(HashTable hashtab, int key, const char* bin_name)
{
    // ����� ������ ������ �� ����� � ���-�������
    int n = hashtab.findKey(key).key;

    // �������� ����� �� ���-������� � ��������������� ������ �� �����
    hashtab.deleteKey(key);
    delete_by_key(bin_name, n);
    hashtab.printHashTable();
}

// ������� ��� ������ ������ � ����� �� ����� �� ���-�������
void findRecordInFile(HashTable hashtab, int key, const char* bin_name)
{
    ifstream file(bin_name, ios::binary);

    // ����� ������ ������ � ����� �� ����� �� ���-�������
    int n = hashtab.findKey(key).numberRecord;
    if (n < 1)
        return; // ���� ������ �� �������, ����� �� �������

    // ����� � ����� ������ �� ����� �� ������ ������
    find_by_key(bin_name, n);
}

#endif //_3_FILEBYHASH_H