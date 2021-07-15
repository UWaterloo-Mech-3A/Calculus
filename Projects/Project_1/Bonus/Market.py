import random
import numpy as np


class Individual:
	def __init__(self, individual_index: int, assigned_fruit_index: int, fruits_in_market: int,
	             max_item_value: float = 10.0, currency: float = 100.00):
		self._index = individual_index
		self._goods = [False] * fruits_in_market
		self._personal_good_worth = [random.uniform(0, max_item_value) for _ in range(fruits_in_market)]
		self.fruit_index = assigned_fruit_index
		self.currency = currency

		if assigned_fruit_index != -1:
			self._goods[assigned_fruit_index] = True

	@staticmethod
	def _further_better_trade_exists(global_preferences: np.array, global_possessions: np.array,
	                                 item_index: int, price: float) -> bool:
		"""
		Does there exist a path where I can sell the fruit I'm looking at to a person who values it more than me

		note: rows = player index

		:param item_index:
		:param global_preferences: 2d matrix categorizing every person and their desired good's max buying price
		:param global_possessions: 2d matrix categorizing every person and their current good in possession
		:return:
		"""

		# Check to see if anyone in the market views the good in question higher than you
		# AKA. get all rows with item_index column, and track the individuals who do value it more than you AND do not
		#   have that fruit
		value_column, possession_column = global_preferences[:, item_index], global_possessions[:, item_index]
		# value_column * ~possession_column ==> only those who don't have an item will register a value
		for value in value_column * ~possession_column:
			if value > price:
				return True
		return False

	def get_preferences(self):
		return self._personal_good_worth

	def consider_buy(self, global_preferences, global_possessions, fruit_index, price) -> bool:
		# is there a trading path for you
		better_trade_exists = self._further_better_trade_exists(global_preferences, global_possessions, fruit_index)
		i_want_it = self._personal_good_worth[fruit_index] >= price
		return i_want_it or better_trade_exists

	def consider_sell(self, global_preferences, global_possessions, fruit_index, price) -> bool:
		better_trade_exists = self._further_better_trade_exists(global_preferences, global_possessions, fruit_index)
		keep_it = self._personal_good_worth[fruit_index] < price
		return keep_it or not better_trade_exists

	def sell(self):
		index = self.fruit_index
		self._goods[index] = False
		return index


