#include <iostream>
#include <fstream>
#include <cstring>
#include <vector>
#include <cmath>
#include <stdio.h> 
#include <time.h> 

struct s_book {
    char ISBN[13];
    char author[50];
    char name[50];
};

void convert_to_binary(const char* textFileName, const char* binaryFileName) {
    std::ifstream inputFile(textFileName);
    std::ofstream outputFile(binaryFileName, std::ios::out | std::ios::binary);

    if (!inputFile.is_open()) {
        std::cout << "Ошибка открытия текстового файла" << std::endl;
        return;
    }
    if (!outputFile.is_open()) {
        std::cout << "Ошибка создания двоичного файла" << std::endl;
        return;
    }

    s_book record;
    while (inputFile >> record.ISBN >> record.author >> record.name) {
        outputFile.write((char*)(&record), sizeof(s_book));
    }

    inputFile.close();
    outputFile.close();

    std::cout << "Преобразование завершено" << std::endl;
}

void save_to_text(const char* binaryFileName, const char* textFileName) {
    std::ifstream inputFile(binaryFileName, std::ios::binary);
    std::ofstream outputFile(textFileName);

    if (!inputFile.is_open()) {
        std::cout << "Ошибка открытия двоичного файла" << std::endl;
        return;
    }
    if (!outputFile.is_open()) {
        std::cout << "Ошибка создания текстового файла" << std::endl;
        return;
    }

    s_book record;
    while (inputFile.read(reinterpret_cast<char*>(&record), sizeof(s_book)))
    {
        outputFile << record.ISBN << std::endl << record.author << std::endl << record.name << std::endl;
    }

    inputFile.close();
    outputFile.close();

    std::cout << "Сохранение в текстовый файл завершено" << std::endl;
}

void print_all_records(const char* binaryFileName) {
    std::ifstream inputFile(binaryFileName, std::ios::binary);
    if (!inputFile.is_open()) {
        std::cout << "Ошибка открытия двоичного файла" << std::endl;
        return;
    }

    s_book record;
    while (inputFile.read(reinterpret_cast<char*>(&record), sizeof(s_book))) {
        std::cout << "ISBN: " << record.ISBN << ",\tАвтор: " << record.author << ",\tНазвание: " << record.name << std::endl;
    }

    inputFile.close();
}

void access_record_by_index(const char* binaryFileName, int index) {
    std::ifstream inputFile(binaryFileName, std::ios::binary);
    if (!inputFile.is_open()) {
        std::cout << "Ошибка открытия двоичного файла" << std::endl;
        return;
    }

    s_book record;
    inputFile.seekg(index * sizeof(s_book));

    if (inputFile.read(reinterpret_cast<char*>(&record), sizeof(s_book))) {
        std::cout << "ISBN: " << record.ISBN << ",\tАвтор: " << record.author << ",\tНазвание: " << record.name << std::endl;
    }
    else {
        std::cout << "Запись с указанным номером не найдена" << std::endl;
    }

    inputFile.close();
}

void lin_search(const char* binaryFileName, char IBSN[13])
{
    std::ifstream inputFile(binaryFileName, std::ios::binary);
    if (!inputFile.is_open()) {
        std::cout << "Ошибка открытия двоичного файла" << std::endl;
        return;
    }
    clock_t start = clock();
    s_book record;
    while (inputFile.read(reinterpret_cast<char*>(&record), sizeof(s_book))) {
        bool flag = true;
        for (int i = 0; i < 13; i++)
        {
            if (IBSN[i] != record.ISBN[i])
                flag = false;
        }
        if (flag)
            std::cout << "ISBN: " << record.ISBN << ",\tАвтор: " << record.author << ",\tНазвание: " << record.name << std::endl;
    }
    clock_t end = clock();
    double seconds = (double)(end - start) / CLOCKS_PER_SEC;
    std::cout << std::endl << "~~~" << seconds << "~~~" << std::endl;
    inputFile.close();
}

void bin_search(const char* binaryFileName, char IBSN[13])
{
    std::ifstream inputFile(binaryFileName, std::ios::binary);
    if (!inputFile.is_open()) {
        std::cout << "Ошибка открытия двоичного файла" << std::endl;
        return;
    }

    s_book record;
    std::vector<std::string> vec;

    while (inputFile.read(reinterpret_cast<char*>(&record), sizeof(s_book))) {
        char el[13];
        for (int i = 0; i < 13;i++)
        {
            el[i] = record.ISBN[i];
        }
        vec.push_back(el);
    }
    inputFile.close();

    clock_t start = clock();
    std::string search = IBSN;

    int index;
    int i = vec.size() / 2;
    int delta = vec.size() / 2;
    while (true)
    {
        if (vec.at(i) == search)
        {
            index = i;
            break;
        }
        if (vec.at(i) < search)
        {
            i += delta / 2;
            if (delta!=1)
                delta = delta / 2;

        }
        if (vec.at(i) > search)
        {
            i -= delta / 2;
            if (delta != 1)
                delta = delta / 2;
        }
    }

    clock_t end = clock();
    double seconds = (double)(end - start) / CLOCKS_PER_SEC;
    
    std::ifstream outputFile(binaryFileName, std::ios::binary);
    outputFile.seekg(index * sizeof(s_book));
    if (outputFile.read(reinterpret_cast<char*>(&record), sizeof(s_book)))
        std::cout << "ISBN: " << record.ISBN << ",\tАвтор: " << record.author << ",\tНазвание: " << record.name << std::endl;
    outputFile.close();
    std::cout << std::endl << "~~~" << seconds << "~~~" << std::endl;
}

int main() {
    setlocale(LC_ALL, "RUS");
    const char* binaryFileName = "data.dat";
    char textFileName[100];

    std::cout << "Введите имя текстового файла: ";
    std::cin >> textFileName;
    int choice;

    while (true) {
        std::cout << "Выберите операцию:" << std::endl << "1. Преобразовать текстовый файл в двоичный" <<
            std::endl << "2. Сохранить двоичный файл в текстовый" << std::endl << "3. Вывести все записи из двоичного файла" <<
            std::endl << "4. Доступ к записи по номеру" << std::endl << "5. Линейный поиск по ISBN" <<
            std::endl << "6. Бинарный поиск по ISBN" << std::endl;
        std::cout << "Введите номер операции: ";
        std::cin >> choice;
        std::cout << std::endl;
        switch (choice) {
        case 1:
            convert_to_binary(textFileName, binaryFileName);
            system("pause");
            std::cout << std::endl;
            break;
        case 2:
            save_to_text(binaryFileName, textFileName);
            system("pause");
            std::cout << std::endl;
            break;
        case 3:
            print_all_records(binaryFileName);
            system("pause");
            std::cout << std::endl;
            break;
        case 4:
            int index;
            std::cout << "Введите номер записи: ";
            std::cin >> index;
            access_record_by_index(binaryFileName, index);
            system("pause");
            std::cout << std::endl;
            break;
        case 5:
            char lin_ISBN[13];
            std::cout << "Введите ISBN: ";
            std::cin >> lin_ISBN;
            lin_search(binaryFileName, lin_ISBN);
            system("pause");
            std::cout << std::endl;
            break;
        case 6:
            char bin_ISBN[13];
            std::cout << "Введите ISBN: ";
            std::cin >> bin_ISBN;
            bin_search(binaryFileName, bin_ISBN);
            system("pause");
            std::cout << std::endl;
            break;
        default:
            return 0;
            break;
        }
        std::cout << std::endl;
    }
    return 0;
}