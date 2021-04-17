#include <iostream>
int main() {
	int x = 0;
	for (x; x < 10; x++) {
        if(x%2==0) {
            std::cout << x << "\n";
		}
	}

	return 0;
}