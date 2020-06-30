#include <iostream>
#define add(x,y) x+y

#define x() 5

int main() {
	int answer = add(5,10+1);
	std::cout << x()+answer << "\n";
}