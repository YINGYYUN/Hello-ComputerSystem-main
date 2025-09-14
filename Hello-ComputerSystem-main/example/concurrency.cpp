#include <iostream>
#include <thread>
#include <vector>

int total_sum = 0;
const int COUNT = 10000;

void add() {
    for (int i = 0; i < COUNT; ++i) {
        total_sum++;
    }
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back(add);
    }

    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "预期结果: " << 4 * COUNT << std::endl;
    std::cout << "实际结果: " << total_sum << std::endl;
    
    return 0;
}