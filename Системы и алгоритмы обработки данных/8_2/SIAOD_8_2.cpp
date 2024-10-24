#include <iostream>
#include <vector>
#include <algorithm>

int lenDyn = 0;
int lenBru = 0;

int max_sum(std::vector<std::vector<int>>& triangle)
{
    int n = triangle.size();

    std::vector<int> maxSums = triangle[n - 1];

    for (int i = n - 2; i >= 0; --i)
        for (int j = 0; j <= i; ++j)
        {
            lenDyn++;
            maxSums[j] = triangle[i][j] + std::max(maxSums[j], maxSums[j + 1]);
        }
    return maxSums[0];
}

int brute_force(const std::vector<std::vector<int>>& triangle, int row, int col)
{
    if (row == triangle.size() - 1)
        return triangle[row][col];
    
    lenBru++;
    int leftPathSum = brute_force(triangle, row + 1, col);
    int rightPathSum = brute_force(triangle, row + 1, col + 1);

    return triangle[row][col] + std::max(leftPathSum, rightPathSum);
}

int main()
{
    setlocale(LC_ALL, "RUS");

	std::vector<std::vector<int>> vec = { { 7 }, {3,8}, {8,1,0}, {2,7,4,4}, {4,5,2,6,5} };
    int result = max_sum(vec);
    std::cout << "Наибольшая сумма на пути: " << result << "\t\t\t| Количество переборов: " << lenDyn << std::endl;
    std::cout << "Наибольшая сумма на пути (метод грубой силы): " << brute_force(vec, 0, 0) << " | Количество переборов: " << lenBru << std::endl;
}
