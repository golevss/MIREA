#include <iostream>
#include <fstream>
#include <bitset>
#include <map>
#include <Windows.h>

const unsigned long int size = 10000000;

void task_2()
{
    unsigned char a = 0;
    std::map<int, int> m;
    int size_input;
    int input;
    std::cout << "Введите количество чисел" << std::endl;
    std::cin >> size_input;

    std::cout << "Введите "<< size_input<<" чисел" << std::endl;
    for (int i = 0; i < size_input;i++)
    {
        std::cin >> input;
        if (m[input] == 0)
            a += 1<<input;
        m[input] += 1;
        
    }
    std::cout << "Отсортированный массив: " << std::endl;
    std::cout << std::bitset<8>(a) << std::endl;
    for (int i = 0; i < 8; i++)
    {
        if ((a>>i) & 1)
        {
            for (int j = 0; j < m[i] ; j++)
            {
                std::cout << i << ' ';
            }
        }
    }
    std::cout << std::endl;
}

void task_3()
{
    std::bitset<size>* numbers = new std::bitset<size>;

    unsigned long int input;
    std::cout << "Введите по очереди семизначные числа (0 для завершения):" << std::endl;
    while (true) {
        std::cin >> input;
        if (input == 0) {
            break;
        }
        if (input >= size / 10 && input < size) {
            numbers->set(input - 1, 1);
        }
        else {
            std::cout << "Только семизначные числа!" << std::endl;
        }
    }

    std::ofstream outfile("sortedList.txt");
    for (unsigned long int i = 0; i < size; i++) {
            if (numbers->test(i)) {
                outfile << i + 1 << std::endl;
            }
    }
    outfile.close();
    std::cout << "Результат сортировки был записан в файл." << std::endl;
}


int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    int num = 0;
    std::cout << "Введите номер задания: ";
    std::cin >> num;
    while (true) {
        switch (num)
        {
        case 2:
            task_2();
            system("pause");
            std::cout << std::endl;
            return 0;
        case 3:
            task_3();
            system("pause");
            std::cout << std::endl;
            return 0;
        default:
            return 0;
        }
    }
    return 0;
}