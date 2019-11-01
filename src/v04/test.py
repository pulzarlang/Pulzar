import os
code = '''
#include <iostream>
using namespace std;
int main() {
    cout << "hello world";
    return 0;
}
'''
f = open("output.cpp", "w")
f.write(code)
f.close()
os.system("g++ output.cpp")
os.system("a.exe")