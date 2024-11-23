#include <iostream>
#include <Windows.h>
#include <fstream>
#include <string>
#include <conio.h>  

int createTextFile(std::string fileName);
int readTextFile(std::string fileName);
int addNotetoEndFile(std::string fileName);
void findTextFile(std::string fileName);
int numFile(std::string fileName);
void copyFile(std::string fileName);

int createTextFile(std::string fileName) {
    std::ifstream file(fileName);
    if (file.is_open()) {
        file.close();
        return 0;
    }
}

int readTextFile(std::string fileName) {
    std::ifstream file;
    file.open(fileName);
    int buf;

    if (!file.is_open()) {
        std::cout << "Ошибка открытия" << std::endl;
        file.close();
        return 1;
    }
    else {
        std::cout << "Файл открыт" << std::endl;
        while(file >> buf)
        {   
            std::cout << buf << " ";
        }

        std::cout << std::endl;
        file.close();
        return 0;
    }
}

int addNotetoEndFile(std::string fileName) {
    std::ofstream file(fileName, std::ios::app);
    std::string str;
    if (file.is_open()) {
        std::cout << "Открыли на дозапись (stop - для выхода)" << std::endl;
        while (true){
            std::cin>> str;
            if (str == "stop")
                break;
            else
                file << str << std::endl;
        }
        file.close();
    }
    return 0;
}

void findTextFile(std::string fileName)
{
    int num;
    int line, num_line = 0;
    std::cout << "Введите номер элемента: ";
    std::cin >> num;
    std::ifstream file;
    file.open(fileName);
    while (file >> line)
    {
        num_line++;

        if (num_line == num)
        {
            std::cout << line << std::endl;
            file.close();
            return;
        }
    }
    file.close();
    std::cout << "Не найдено" << std::endl;
}

int numFile(std::string fileName)
{
    int num = 0, line;
    std::ifstream file;
    file.open(fileName);
    while(file >> line)
    {
        num++;
    }
    file.close();
    return num;
}

void copyFile(std::string fileName)
{
    std::string new_file_name;
    std::string buff_end, buff_str, line;
    int num = 0;
    std::cout << "Введите имя нового файла : ";
    std::cin >> new_file_name;

    std::ifstream file;
    file.open(fileName);
    while(file >> line)
    {
        if (num == 0) buff_str = line;
        num++;
        if (num == numFile(fileName)) buff_end = line;
    }
    file.close();
    //----------------------
    num = 0;
    file.open(fileName);
    std::ofstream new_file(new_file_name,std::ios::ate);
    if (new_file.is_open())
    {
        new_file << buff_end << std::endl;
        while(file >> line)
        {
            num++;
            if (num > 1 && num < numFile(fileName))
            {
                new_file << line << std::endl;
            }
        }
        new_file << buff_str << std::endl;
        file.close();
        new_file.close();
    }
}