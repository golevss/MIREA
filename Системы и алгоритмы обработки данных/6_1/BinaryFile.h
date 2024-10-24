#ifndef _3_BINARYFILE_H
#define _3_BINARYFILE_H

#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// ����������� ��������� ��� �������� ������ � �������
struct s_book
{
    char dateOfBirth[11];
    char name[50];
};

// ������� ��� ����������� ������ �� ���������� ����� � ��������
void txt_to_bin(ifstream& txt, ofstream& bin)
{
    if (!bin.is_open() || !txt.is_open())
    {
        cout << "������ �������� ���������� �����\n";
        return;
    }

    FriendRecord friendRecord;

    // ������ ������ �� ���������� ����� � ������ �� � �������� ����
    while (txt.getline(friendRecord.dateOfBirth, sizeof(friendRecord.dateOfBirth)) &&
        txt.getline(friendRecord.name, sizeof(friendRecord.name)))
    {
        bin.write((char*)&friendRecord, sizeof(friendRecord));
        txt.ignore(); // ���������� ������ ����� ������
    }
    txt.close();
    bin.close();
    cout << "������� ������ �������\n";
}

// ������� ��� ����������� ������ �� ��������� ����� � ���������
void bin_to_txt(ifstream& binn, ofstream& txtt)
{
    FriendRecord friendRecord;

    if (!txtt.is_open())
    {
        cout << "������ �������� ���������� �����\n";
        return;
    }

    // ������ ������ �� ��������� ����� � ������ �� � ��������� ����
    while (binn.read((char*)&friendRecord, sizeof(FriendRecord)))
    {
        txtt << friendRecord.dateOfBirth << endl << friendRecord.name << endl;
    }

    // �������� �� ������ ������ �� ��������� �����
    if (!binn.eof() && binn.fail())
    {
        cout << "������ ������ �� ��������� �����" << endl;
    }
    cout << "������� ������ �������\n";
}

// ������� ��� ������ ������ �� ��������� ����� �� �����
void print_from_bin(ifstream& bin)
{
    FriendRecord friendRecord;
    bin.read((char*)&friendRecord, sizeof(FriendRecord));

    // ����� ������ �� ��������� ����� �� �����
    while (!bin.eof())
    {
        cout << friendRecord.dateOfBirth << endl << friendRecord.name << endl;
        bin.read((char*)&friendRecord, sizeof(FriendRecord));
    }
    bin.close();
}

// ������� ��� �������� ������ �� ���������� �����
void delete_by_key(const char* bin_name, int n)
{
    fstream bin(bin_name, ios::binary | ios::in);

    // �������� �� �������� �������� �����
    if (!bin.is_open())
    {
        cerr << "������ �������� �����\n";
        return;
    }

    fstream temp("temp_file.dat", ios::binary | ios::out);

    // �������� �� �������� �������� ���������� �����
    if (!temp.is_open())
    {
        cerr << "������ �������� ���������� �����\n";
        bin.close();
        return;
    }

    FriendRecord friendRecord;
    int key = 1;

    // ����������� ������ �� ��������� ����� �� ���������, �������� ������ � ��������� ������
    while (bin.read((char*)&friendRecord, sizeof(FriendRecord)))
    {
        if (key != n)
        {
            temp.write((char*)&friendRecord, sizeof(FriendRecord));
        }
        key++;
    }
    bin.close();
    temp.close();

    // �������� ��������� ����� � �������������� ���������� �����
    remove(bin_name);
    rename("temp_file.dat", bin_name);
}

// ������� ��� ������ ������ �� ���������� �����
s_book find_by_key(const char* bin_name, int n)
{
    ifstream bin(bin_name, ios::binary);
    s_book record;

    // �������� �� �������� �������� �����
    if (!bin)
    {
        cerr << "�� ������� ������� ���� ��� ������";
        return s_book();
    }

    // ����� � ����� �� ����� ������ �� ���������� �����
    size_t friendSize = sizeof(s_book);
    bin.seekg((n - 1) * friendSize, ios::beg);
    bin.read((char*)&record, sizeof(s_book));
    cout << record.dateOfBirth << endl << record.name << endl;

    // �������� �� ������ ������
    if (bin.good())
    {
        cout << "������ ������ �� ����������\n";
    }
    else
    {
        cout << "���������� ������ ������\n";
    }
    bin.close();
    return record;
}

#endif //_3_BINARYFILE_H