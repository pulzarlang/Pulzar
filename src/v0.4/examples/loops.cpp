#include <iostream>
int main() {
	int matrix[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
	int i = 0;
	int j = 0;
	int n = 10;
	for (i; i < 10; i++) {
        for (j; j < 10; j++) {
            std::cout << matrix[i][j] << "\n";
		}
	}

}