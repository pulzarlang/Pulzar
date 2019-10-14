#©Flash 2018-19

#Author : Brian Turza
#Created : 20.8. 19
from math import *
#Math constants
pi = 3.1415926535897932384626433832795
e = 2.7182818284590452353602874713527
phi = 1.61803398874989484820

class MathModule(object):

    def __init__(self,):
        pass

    def factorial(self,n):
        n = int(n)
        num = 1
        if n == 0:
            print(1)

        elif n < 0:
            print("MathError: factorial can be only positive integer")
        elif n > 0:
            while n >= 1:
                num = num * n
                n -= 1
            return num
    
    def complex(self,n):
        #n = (5+3i) + (7i + 5) = 10 + 10i
        n1 = complex(n)
        n1 = str(n1)
        n2 = n1.replace("j","i")
        print(n2)

    def sin(self,n):
        print(sin(n))
