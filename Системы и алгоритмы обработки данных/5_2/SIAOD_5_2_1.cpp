#include <iostream>
#include <fstream>
#include <cmath>
#include <Windows.h>

void in_file(std::ofstream& fout, const char* name)
{
    fout.open(name, std::ios::out | std::ios::trunc);
    for (int i = 24; i < 48; i++) {
        fout << i << std::endl;
    }
    if (fout.good()) {
        std::cout << "При создании файла ошибок не возникло." << std::endl;
    }
    else {
        std::cout << "При создании файла возникли ошибки" << std::endl;
    }
    fout.close();
}

void file_output(const char* name)
{
    int x;
    std::ifstream fout;
    fout.open(name, std::ios::in);
    while (fout >> x) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
    fout.close();
}

void add_new_line(std::ofstream& fout, const char* name, int x)
{
    fout.open(name, std::ios::out | std::ios::app);
    fout << x;
    fout.close();
}

void find_numbers(const char* name, int nums)
{
    std::ifstream fout;
    fout.open(name);
    int x;
    int i;
    std::cout << "> ";
    for (i = 1; (i < nums && (!fout.eof())); i++) {
        fout >> x;
    }
    if (!fout.eof() && (i == nums)) {
        fout >> x;
        std::cout << x;
    }
    fout.close();
}

int length_file(const char* name)
{
    int num = 0, line;
    std::ifstream file;
    file.open(name);
    while (file >> line)
    {
        num++;
    }
    file.close();
    return num;
}

void personal_task(const char* a_file, const char* b_file)
{
    int x;
    int num_1 = 0;
    int num_2 = 0;
    int f_elem;
    int l_elem;
    std::ifstream first_file;
    std::ofstream second_file;

    first_file.open(a_file, std::ios::in);
    first_file >> l_elem;
    while (first_file >> f_elem) { num_1++; }
    first_file.close();

    first_file.open(a_file, std::ios::in);
    second_file.open(b_file, std::ios::out | std::ios::trunc);

    second_file << f_elem << std::endl;
    while (first_file >> x)
    {
        if (num_2 !=0 && num_2!=num_1)
            second_file << x << std::endl;
        num_2++;
    }
    second_file << l_elem << std::endl;

    if (second_file.good()) {
        std::cout << "Ошибок при вводе не найдено." << std::endl;
    }

    first_file.close();
    second_file.close();

    std::ifstream output_second_file;
    output_second_file.open(b_file, std::ios::in);
    std::cout << "Вывод чисел нового файла:" << std::endl;
    while (output_second_file >> x) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
}

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    std::ofstream fout;
    if (!fout) {
        std::cout << "Не удаётся открыть файл";
        return -1;
    }

    std::string inputFileName;
    std::string outputFileName = "secondfile.txt";
    std::cout << "Введите имя первого текстового файла: ";
    std::cin >> inputFileName;
    in_file(fout, inputFileName.c_str());

    while (true) {
        int a = 0;
        std::cout << std::endl;
        std::cout << "1) Вывести содержимое файла." << std::endl << "2) Добавить новую запись" << 
        std::endl << "3) Прочитать число через порядковый номер." << std::endl << "4) Определить количество чисел." <<
        std::endl << "5) Доп задание." << std::endl << std::endl;
        std::cout << "Введите номер действия: ";
        std::cin >> a;
        switch (a)
        {
        case 1:
            file_output(inputFileName.c_str());
            system("pause");
            std::cout << std::endl;
            break;
        case 2:
            int x;
            std::cout << "Введите элемент, который хотите добавить: ";
            std::cin >> x;
            add_new_line(fout, inputFileName.c_str(), x);
            system("pause");
            std::cout << std::endl;
            break;
        case 3:
            int nums;
            std::cout << "Введите порядковый номер в файле: ";
            std::cin >> nums;
            find_numbers(inputFileName.c_str(), nums);
            system("pause");
            std::cout << std::endl;
            break;
        case 4:
            std::cout << length_file(inputFileName.c_str()) << " чисел содержится в файле." << std::endl;
            system("pause");
            std::cout << std::endl;
            break;
        case 5:
            personal_task(inputFileName.c_str(), outputFileName.c_str());
            system("pause");
            std::cout << std::endl;
            break;
        default:
            return 0;
        }
    }
    return 0;
}