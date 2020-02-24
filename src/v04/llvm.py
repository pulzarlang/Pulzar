from numba import jit
import numpy as np
import timeit

# Define a function normally without using numba

def test_without_numba(n):
    x = 0
    for i in n:
        x += n[i] ** 2
    return x

# Define a function using numba jit. Using the argument nopython=True gives the
# fastest possible run time, but will error if numba cannot precomplile all the
# code. Using just @jit will allow the code to mix pre-compiled and normal code
# but will not be as fast as possible

@jit(nopython=True)
def test_with_numba(n):
    x = 0
    for i in n:
        x += n[i] ** 2
    return x


# Run functions first time without timing (compilation included in first run)
test_without_numba([x for x in range(1000)])
test_with_numba([x for x in range(1000)])

# Time functions with timeit (100 repeats).
# Multiply by 1000 to give milliseconds

timed = timeit.timeit(stmt = test_without_numba, number=100) * 1000
print ('Miliseconds without numba: %.3f' %timed)

timed = timeit.timeit(stmt = test_with_numba, number=100) * 1000
print ('Miliseconds with numba: %.3f' %timed)
