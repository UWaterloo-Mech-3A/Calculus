from numpy import nan
from typing import Dict
import pandas as pd
from sympy import Symbol, diff, factorial
from sympy.core.add import Add
from sympy.core.mul import Mul
from typing import Union


def n_diff(f: Union[Add, Mul], variable: Symbol, n: int):
	for _ in range(n):
		f = f.diff(variable)
	return f


def taylor(f: Union[Add, Mul], variable: Symbol, x0: float = 0.0, n: int = 10):
	fn = n_diff(f, variable, n)
	if n > 0:
		return ((fn.subs({variable: x0}) / factorial(n)) * (variable - x0) ** n) + taylor(f, variable, x0, n - 1)
	else:
		return (fn.subs({variable: x0}) / factorial(n)) * (variable - x0) ** n


def function(x: float):
	return x ** 2 - 4


def bisection(f: function, a: float, b: float, tol=0.001, iterations=100, history: pd.DataFrame = None):
	p = (a + b) / 2
	if history is None: history = pd.DataFrame(columns=["a", "b", "p", "f(p)"])

	if f(a) * f(b) > 0: Exception("No root exists between {} and {}".format(a, b))

	history = history.append({
		"a": a,
		"b": b,
		"p": p,
		"f(p)": f(p)
	}, ignore_index=True)

	if abs(f(p)) > tol and iterations > 0:
		if f(a) * f(p) > 0:
			a = p
		else:
			b = p
		return bisection(f, a, b, tol, iterations - 1, history)
	else:
		return p, history


def does_converges(g: Union[Add, Mul], variable: Symbol, x0):
	return abs(g.diff(variable).subs({variable: x0}).simplify()) < 1


def direct_iteration(f: Union[Add, Mul], variable: Symbol, variable_start: float = 0.0, iterations: int = 100):
	if does_converges(f, variable, variable_start):
		if iterations > 0:
			print(variable_start)
			variable_start = f.subs({variable: variable_start}).simplify()
			print(variable_start.evalf())
			print()
			return direct_iteration(f, variable, variable_start, iterations - 1)
		else:
			print(variable_start.evalf())
			return variable_start
	else:
		print("Does not converge at starting point given")


def newtons_method(f: Union[Add, Mul], variable: Symbol, x0: float = 0.0, tol: float = 0.001, iterations: int = 100):
	f_ = f.diff(variable)
	for i in range(iterations):
		numerator = f.subs({variable: x0})
		denominator = f_.subs({variable: x0})
		x1 = x0 - numerator / denominator
		print(x1)
		if abs(x0 - x1) > tol:
			return x1
		else:
			x0 = x1
	return x0

