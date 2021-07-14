import numpy as np
from tqdm.auto import tqdm
from typing import Dict


class RungeKutta4:
	def __init__(self, dt: float = 0.001, weightings: np.array = None, dr_dt=None, d2r_dt2=None):
		"""
		Example usage:

		>>> from numpy import exp
		>>>
		>>> def dy_dt(y, d2y_dt2, t)
		>>>     return exp(y + d2y_dt2 + t)
		>>>
		>>> def d2y_dt2(y, dy_dt, t)
		>>>     return exp(y + dy_dt + t)
		>>>
		>>>
		>>> analyzer = RungeKutta4(dt=0.001, dr_dt=dy_dt, d2r_dt2=d2y_dt2)
		>>> results = analyzer(r=100, dr_dt=0, t_=0, steps=1000)

		:param dt: constant change in time
		:param weightings: weightings for Runga Kutta (4) method
		:param dr_dt: \frac{dr}{dt} = f(\frac{d^{2}r}{dt^{2}}, r, t)
		:param d2r_dt2: \frac{d^{2}r}{dt^{2}} = f(\frac{dr}{dt}, r, t)
		"""

		self.function_dr_dt = dr_dt if dr_dt is not None else self.function_dr_dt
		self.function_d2r_dt2 = d2r_dt2 if d2r_dt2 is not None else self.function_d2r_dt2
		self.w = np.array([1, 2, 2, 1]) if weightings is None else weightings
		self.dt = dt

	def __call__(self, r: float, dr_dt: float, t: float, steps: int) -> Dict:
		# Initialization of the main Dictionary
		outputs = {
			"r": [r],
			"dr_dt": [dr_dt],
			"d2r_dt2": [np.nan],    # we don't have the initial conditions for the second derivative
			"t": [t]
		}
		for _ in tqdm(range(steps), desc="Generating values"):
			# 1 updating the second derivative using last known information
			outputs["d2r_dt2"].append(self.function_d2r_dt2(r=outputs["r"][-1], dr_dt=outputs["dr_dt"][-1], t=outputs["t_"][-1]))
			# 2 updating the first derivative using last known information
			outputs["dr_dt"].append(self.function_dr_dt(r=outputs["r"][-1], d2r_dt2=outputs["d2r_dt2"][-1], t=outputs["t_"][-1]))
			# 3 updating the main equation using \frac{dr}{dt}
			outputs["r"].append(outputs["r"][-1] + outputs["dr_dt"][-1] / self.dt)
			# 4 updating the time  using last known information
			outputs["t"].append(outputs["t"][-1] + self.dt)
		return outputs

	def function_dr_dt(self, r: float, d2r_dt2: float, t: float) -> float:
		raise NotImplementedError

	def function_d2r_dt2(self, r: float, dr_dt: float, t: float) -> float:
		raise NotImplementedError

	def _kr4_dr_dt(self, r: float, d2r_dt2: float, t: float) -> float:
		"""
		Applies the Runge Kutta method (4) for the first derivative function
		:param r:
		:param d2r_dt2:
		:param t:
		:return:
		"""
		k1 = self.function_dr_dt(r, d2r_dt2, t)
		k2 = self.function_dr_dt(r + k1 * self.dt / 2, d2r_dt2, t + self.dt / 2)
		k3 = self.function_dr_dt(r + k2 + self.dt / 2, d2r_dt2, t + self.dt / 2)
		k4 = self.function_dr_dt(r + k3 * self.dt, d2r_dt2, t + self.dt)

		k = np.array([k1, k2, k3, k4])
		return r + (1 / np.sum(self.w)) * np.sum(self.w * k)

	def _kr4_d2r_dt2(self, r: float, dr_dt: float, t: float) -> float:
		"""
		Applies the Runge Kutta method (4) for the second derivative function
		:param r:
		:param dr_dt:
		:param t:
		:return:
		"""
		k1 = self.function_d2r_dt2(r, dr_dt, t)
		k2 = self.function_d2r_dt2(r, dr_dt + k1 * self.dt / 2, t + self.dt / 2)
		k3 = self.function_d2r_dt2(r, dr_dt + k2 + self.dt / 2, t + self.dt / 2)
		k4 = self.function_d2r_dt2(r, dr_dt + k3 * self.dt, t + self.dt)

		k = np.array([k1, k2, k3, k4])
		return dr_dt + (1 / np.sum(self.w)) * np.sum(self.w * k)


x = RungeKutta4()



