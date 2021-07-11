import numpy as np
from typing import List
from tqdm.auto import tqdm


class RungeKutta4:
	def __init__(self, weightings: np.array = None):
		"""
		Usage example:
		>>> def dy_dt(y, t):
		>>> 	return y * (e ** t)
		>>>
		>>> rk4 = RungeKutta4()
		>>> rk4.function = dy_dt
		>>> y0 = 100
		>>> t0 = 0
		>>> delta_t = 0.001
		>>> steps = 1000
		>>> results = rk4(delta_t, y0, steps, t0)
		:param weightings:
		"""
		self.w = np.array([1, 2, 2, 1]) if weightings is None else weightings

	def __call__(self, delta_t: float, y0: float, steps: int, t0: float = 0):
		outputs = []
		y, t = y0, t0

		for _ in tqdm(range(steps)):
			k1 = self.function(y,                       t)
			k2 = self.function(y + k1 * delta_t / 2,    t + delta_t / 2)
			k3 = self.function(y + k2 + delta_t / 2,    t + delta_t / 2)
			k4 = self.function(y + k3 * delta_t,        t + delta_t)
			k = np.array([k1, k2, k3, k4])

			y += (1 / np.sum(self.w)) * np.sum(self.w * k)
			outputs.append(y)
		return outputs

	def function(self, y: float, t: float):
		raise NotImplementedError





