import numpy as np
from matplotlib import pyplot as plt


def bisection(f, a: float, b: float, tolerance: float, i: int = 0, limit: int = 100):
    if np.sign(f(a)) == np.sign(f(b)): raise Exception("No root exists between a and b")

    p = (a + b) / 2.0
    i += 1
    if f(p) < tolerance or i >= limit: return p
    print("step {}: \t\t p: {} \t\t f(p): {}".format(i, p, f(p)))

    if np.sign(f(p)) == np.sign(f(a)): bisection(f, p, b, tolerance, i, limit)
    elif np.sign(f(p)) == np.sign(f(b)): bisection(f, a, p, tolerance, i, limit)




