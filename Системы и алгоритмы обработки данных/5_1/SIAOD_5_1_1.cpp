#include <iostream>
#include <bitset>
#include <Windows.h>
#include <cmath>

const int n = sizeof(int) * 8;

void task_1();
void task_3();
void task_4();
void task_5();

void task_1()
{
    unsigned int x = 0;
    unsigned int maska = (1 << 0) + (1 << 5) + (1 << 8);

    std::cout << "Введите искомую переменную:";
    std::cin >> x;
    std::cout << std::endl;

    unsigned int result_t1 = (x | maska);
    std::cout << "Здание 1" << std::endl;
    std::cout << "Изменяемое значение (x)\t" << x << "\t|\t" << std::bitset<n>(x) << std::endl;
    std::cout << "Маска (maska)\t\t" << maska << "\t|\t" << std::bitset<n>(maska) << std::endl;
    std::cout << "Результат операции\t" << result_t1 << "\t|\t" << std::bitset<n>(result_t1) << std::endl;
    std::cout << std::endl;
}

void task_2()
{
    unsigned int x = 0;
    unsigned int maska = pow(2,32) - 1;
    maska = maska - ((1 << 0) + (1 << 5) + (1 << 8));

    std::cout << "Введите искомую переменную:";
    std::cin >> x;
    std::cout << std::endl;

    unsigned int result_t1 = (x & maska);
    std::cout << "Здание 1" << std::endl;
    std::cout << "Изменяемое значение (x)\t" << x << "\t\t|\t" << std::bitset<n>(x) << std::endl;
    std::cout << "Маска (maska)\t\t" << maska << "\t|\t" << std::bitset<n>(maska) << std::endl;
    std::cout << "Результат операции\t" << result_t1 << "\t\t|\t" << std::bitset<n>(result_t1) << std::endl;
    std::cout << std::endl;
}

void task_3()
{
    unsigned int x = 0;

    std::cout << "Введите искомую переменную:";
    std::cin >> x;
    std::cout << std::endl;

    unsigned result_t3 = (x << 3);
    std::cout << "Здание 3" << std::endl;
    std::cout << "Изменяемое значение (x)\t" << x << "\t|\t" << std::bitset<n>(x) << std::endl;
    std::cout << "Множитель\t\t" << 8 << "\t|\t" << std::bitset<n>(8) << std::endl;
    std::cout << "Результат операции\t" << result_t3 << "\t|\t" << std::bitset<n>(result_t3) << std::endl;
    std::cout << std::endl;
}
void task_4()
{
    unsigned int x = 0;

    std::cout << "Введите искомую переменную:";
    std::cin >> x;
    std::cout << std::endl;

    unsigned result_t4 = (x >> 3);
    std::cout << "Здание 4" << std::endl;
    std::cout << "Изменяемое значение (x)\t" << x << "\t|\t" << std::bitset<n>(x) << std::endl;
    std::cout << "Делитель\t\t" << 8 << "\t|\t" << std::bitset<n>(8) << std::endl;
    std::cout << "Результат операции\t" << result_t4 << "\t|\t" << std::bitset<n>(result_t4) << std::endl;
    std::cout << std::endl;
}
void task_5()
{
    unsigned int x = 0;

    std::cout << "Введите искомую переменную: ";
    std::cin >> x;
    std::cout << std::endl;

    unsigned int change = 0;
    unsigned int inv = 0;
    unsigned int maska = 0;
    unsigned result_t5 = 0;

    std::cout << "Введите число изменяемых битов:";
    std::cin >> change;
    std::cout << std::endl;
    std::cout << "Введите номера инвертируемых битов:" << std::endl;
    for (int i = 0; i < change; i++)
    {
        std::cin >> inv;
        if (inv < 0 || inv> 32)
        {
            std::cout << "Некорректный ввод";
            i--;
            break;
        }
        maska += (1 << inv);
    }    

    for (int i = 0; i < n; i++)
    {
        if (((x >> i) & 1))
        {
            result_t5 += 1 << i;
        }
        else if (((maska >> i) & 1))
        {
            result_t5 += 1 << i;
        }
    }

    std::cout << std::endl;
    std::cout << "Изменяемое значение (x)\t" << x << "\t|\t" << std::bitset<n>(x) << std::endl;
    std::cout << "Маска (maska)\t\t" << maska << "\t|\t" << std::bitset<n>(maska) << std::endl;
    std::cout << "Результат операции\t" << result_t5 << "\t|\t" << std::bitset<n>(result_t5) << std::endl;
}

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    while (true) {
        int a = 0;
        std::cout << "Введите номер задания: ";
        std::cin >> a;
        std::cout << std::endl;
        switch (a)
        {
        case 1:
            task_1();
            system("pause");
            std::cout << std::endl;
            break;
        case 2:
            task_2();
            system("pause");
            std::cout << std::endl;
            break;
        case 3:
            task_3();
            system("pause");
            std::cout << std::endl;
            break;
        case 4:
            task_4();
            system("pause");
            std::cout << std::endl;
            break;
        case 5:
            task_5();
            system("pause");
            std::cout << std::endl;
            break;
        default:
            return 0;
        }
    }
}
