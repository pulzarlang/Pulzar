#include <iostream>
#define test()    for (int i = 0; i < 10; i++) {
        std::cout << nums[i] << "\n";
	}


int main() {
	char x[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
	std::cout << "English alphabet:" << "\n";
	for (char a : x) {
        std::cout <<a;
	}

	int nums[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
	for (int i = 0; i < 10; i++) {
        std::cout << nums[i] << "\n";
	}

	return 0;
}