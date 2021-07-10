from numpy import array, zeros, diag, diagflat, dot
from sympy import Eq, Expr, Symbol


def jacobi(A, b, N=25, x=None):
    """Solves the equation Ax=b via the Jacobi iterative method."""
    # Create an initial guess if needed
    if x is None:
        x = zeros(len(A[0]))

    # Create a vector of the diagonal elements of A
    # and subtract them from A
    D = diag(A)
    R = A - diagflat(D)

    # Iterate for N times
    for i in range(N):
        x = (b - dot(R,x)) / D
    return x


def seidel(a, x, b):
    # Finding length of a(3)
    n = len(a)
    # for loop for 3 times as to calculate x, y , z
    for j in range(0, n):
        # temp variable d to store b[j]
        d = b[j]

        # to calculate respective xi, yi, zi
        for i in range(0, n):
            if (j != i):
                d -= a[j][i] * x[i]
        # updating the value of our solution
        x[j] = d / a[j][j]
    # returning our updated solution
    return x


def eulers_method(x0, xf, num, slope_equation: Expr, y_: Symbol, x_: Symbol, initial_slope: float):
    delta = (xf - x0) / num

    y_explicits = [slope_equation.subs({y_: initial_slope, x_: x0})]
    y_implicits = [slope_equation.subs({y_: initial_slope, x_: x0})]
    for i in range(num):
        slope_e = slope_equation.subs({
            y_: y_explicits[-1],
            x_: x0 + delta * i,
        })
        y_explicits.append(y_explicits[-1] + delta * slope_e)

    for i in range(num):
        y_implicits.append(y_implicits[-1] + delta * -1)


if __name__ == '__main__':
    # int(input())input as number of variable to be solved
    n = 3
    a = []
    b = []
    # initial solution depending on n(here n=3)
    x = [0, 0, 0]
    a = [[4, 1, 2], [3, 5, 1], [1, 1, 3]]
    b = [4, 7, 3]
    print(x)

    # loop run for m times depending on m the error value
    for i in range(0, 25):
        x = seidel(a, x, b)
        # print each time the updated solution
        print(x)

    A = array([[2.0, 1.0], [5.0, 7.0]])
    b = array([11.0, 13.0])
    guess = array([1.0, 1.0])

    sol = jacobi(A, b, N=25, x=guess)


