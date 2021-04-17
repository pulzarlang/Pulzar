#©Pulzar 2018-2020

#Author : Brian Turza
#Created : 20.8. 19
import math
import numpy as np

#Math constants
constants = {'pi' : 3.1415926535897932384626433832795, 'phi' : 1.61803398874989484820, 'e' : 2.7182818284590452353602874713527, 'googol' : 10 ** 100, 'g' : 9.80665, }

class MathModule:

    def __init__(self):
        pass

    def factorial(self, n):
        n = int(n)
        num = 1
        if n == 0:
            return 1

        elif n < 0:
            return "MathError: factorial can be only positive integer"
        elif n > 0:
            while n >= 1:
                num *= n
                n -= 1
            return num

    def fib(self, n):
        n = int(n)
        return int(((1+np.sqrt(5))**n-(1-np.sqrt(5))**n)/(2**n*np.sqrt(5))) # ( (1 + √5)^n - (1 - √5)^n ) / (2^n * √5)


    def square_root(self, n): return np.sqrt(n)

    def sin(self, n): return np.sin(n)
    
    def cos(self, n): return np.cos(n)

    def tan(self, n): return np.tan(n)
    
    def arcsin(self, n): return np.arcsin(n)

    def integral(self, n):
        """
        input: intrgral(e ** x / sin : (x) dx) 
        output: 
        """
        #TODO Make both define and undefineid integral solver
        pass

    def sort(self, array, algorithm="bubble_sort"):
        if algorithm == "bubble_sort":
            n = len(array)
            for i in range(n - 1):
                for j in range(n - i - 1):
                    if array[j] > array[j + 1]:
                        array[j], array[j + 1] = array[j + 1], array[j]
            return array

        elif algorithm == "bogo_sort":
            import random
            # Sorts array a[0..n-1] using Bogo sort
            def bogoSort(a):
                n = len(a)
                while (is_sorted(a) == False):
                    a = shuffle(a)
                return a
            def is_sorted(a):
                n = len(a)
                for i in range(0, n - 1):
                    if (a[i] > a[i + 1]):
                        return False
                return True

            # To generate permuatation of the array
            def shuffle(a):
                n = len(a)
                for i in range(0, n):
                    r = random.randint(0, n - 1)
                    a[i], a[r] = a[r], a[i]
                return a

            arr = bogoSort(array)
            return arr


class Complex(object):

    def __init__(self, a=0.0, b=0.0):
        '''Creates Complex Number'''
        self.real = a
        self.imag = b

    def __str__(self):
        '''Returns complex number as a string'''
        self.imag = str(self.imag)
        if self.imag[0] == "-":
            return '%s - %si' % (self.real, self.imag[1:])
        else:
            return '%s + %si' % (self.real, self.imag)

    def __add__(self, rhs):
        '''Adds complex numbers'''
        return Complex(self.real + rhs.real, self.imag + rhs.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return Complex(self.real * other.real - self.imag * other.imag,
                       self.imag * other.real + self.real * other.imag)

    def __opposite__(self):
        self.real = self.real
        self.imag = self.imag if self.imag < 0 else self.imag * -1

    def __truediv__(self, other):
        if isinstance(other, Complex):
            other.__opposite__()
            x = self.real * other.real - self.imag * other.imag
            y = self.imag * other.real + self.real * other.imag
            z = other.real ** 2 + other.imag ** 2
            self.new_real = x / z
            self.new_imag = y / z

            return Complex(self.new_real, self.new_imag)

        elif isinstance(other, int) or isinstance(other, float):
            return Complex(self.real / other, self.imag / other)

    def __pow__(self, power, modulo=None):
        if isinstance(power, int) and power >= 0:
            n = 1
            for i in range(1, power + 1):
                n = Complex(self.real, self.imag) * n
            return n

        elif isinstance(power, int) and power == -2:
            # n ^ (-x) = 1 / n ^ x
            result = Complex(1.0, 0.0) / (Complex(self.real, self.imag) ** abs(power))
            return result