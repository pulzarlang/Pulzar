#include <iostream>
#define search(arr,n,)    for (i; i < n; i++) {
        if(arr[i]==match) {
            return i;
		}
	}


int main() {
	int n = 0;
	int arr[] = {};
	std::cin >> n;
	for (i; i < n; i++) {
        std::cin >> arr[i];
	}

	search(arr,n,5);
}