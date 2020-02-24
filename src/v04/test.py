def numba_mean(x):
    total = 0
    for xi in x:
        total += xi
    return total / len(x)