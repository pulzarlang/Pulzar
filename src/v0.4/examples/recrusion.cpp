#include <iostream>
#define fib(n)    if(n<2) {
        return 1;
	}
 fib(n-1)+fib(n-2)

int main() {
	int n = 0;
	int x = fib(5);
	std::cout << x << "\n";
}