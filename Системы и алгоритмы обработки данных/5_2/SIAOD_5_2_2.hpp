#include <iostream>
#include <Windows.h>
#include <fstream>
#include <string>
#include <conio.h>  
#include <queue>

int createTextFile(std::string fileName);
int readTextFile(std::string fileName);
int addNotetoEndFile(std::string fileName);
void findTextFile(std::string fileName);
void copyFile(std::string fileName);
int numFile(std::string fileName);
void delPartFile(std::string fileName);

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
    std::string buf;

    if (!file.is_open()) {
        std::cout << "Ошибка открытия" << std::endl;
        file.close();
        return 1;
    }
    else {
        std::cout << "Файл открыт" << std::endl;
        int num = 0;
        while (file >> buf)
        {
            std::cout << buf << std::endl;
            num++;
            if (num == 4)
            {
                num = 0;
                std::cout << std::endl;
            }
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
        std::cout << "Открыли для дозапись (stop - для выхода)" << std::endl;
        while (true) {
            std::cout << "Введите ISBN" << std::endl;
            std::cin >> str;
            if (str == "stop")
                break;
            file << str << std::endl;
            std::cout << "Введите автора" << std::endl;
            std::cin >> str;
            file << str << std::endl;
            std::cout << "Введите название" << std::endl;
            std::cin >> str;
            file << str << std::endl;
            std::cout << "Введите год издания" << std::endl;
            std::cin >> str;
            file << str << std::endl;       
        }
        file.close();
    }
    return 0;
}

void findTextFile(std::string fileName)
{
    int num, num_line = 0;
    std::string line;
    std::cout << "Введите номер элемента: ";
    std::cin >> num;
    num *= 4;
    std::ifstream file;
    file.open(fileName);
    while (file >> line)
    {
        num_line++;

        if (num_line > (num-4) && num >= num_line)
        {
            std::cout << line << std::endl;
        }
    }
    file.close();
}

void copyFile(std::string fileName)
{
    std::string new_file_name;
    std::string line;
    std::string author, year;
    int num = 0;
    int buff = 0;
    int num_new = 0;
    std::cout << "Введите имя нового файла : ";
    std::cin >> new_file_name;
    std::cout << "Введите имя автора : ";
    std::cin >> author;
    std::cout << "Введите год : ";
    std::cin >> year;

    std::ifstream file;
    file.open(fileName);
    while (file >> line)
    {
        num++;
        if (line == author)
        {
            buff = num;
        }
        else if (line == year && buff == (num - 2))
        {
            std::cout << "Найдено" << std::endl;
            break;
        }
    }
    file.close();
    //----------------------
    file.open(fileName);
    std::ofstream new_file(new_file_name, std::ios::ate);
    if (new_file.is_open())
    {
        while (file >> line)
        {
            num_new++;
            if (num_new > (num - 4) && num >= num_new)
            {
                new_file << line << std::endl;
            }
        }
        file.close();
        new_file.close();
    }
}

int numFile(std::string fileName)
{
    int num = 0, line;
    std::ifstream file;
    file.open(fileName);
    while (file >> line)
    {
        num++;
    }
    file.close();
    return num/4;
}

void delPartFile(std::string fileName)
{
    std::string year, line;
    std::string f_line, s_line, t_line;
    std::queue<std::string> q;
    int num = 0;
    std::cout << "Введите год" << std::endl;
    std::cin >> year;

    std::ifstream file;
    file.open(fileName);
    
    while (file >> line)
    {
            num++;
            switch (num)
            {
            case 1:
                f_line = line;
                break;
            case 2:
                s_line = line;
                break;
            case 3:
                t_line = line;
                break;
            }
            if (num == 4) num = 0;
            if (line != year)
            {
                q.push(f_line);
                q.push(s_line);
                q.push(t_line);
                q.push(line);
            }
    }
    file.close();
        
}