"""Contains Runs class"""

import datetime
from copy import copy
from functools import reduce
from runtrack_app.models.tables import Run
from typing import List


class Runs:
	"""Combines main_routes into a sorted list"""
	
	@staticmethod
	def _sort_runs(runs: List[Run]) -> List[Run]:
		"""sorts a list of Run objects in nondecreasing order by date

		:param runs: list of main_routes to be sorted by date
		:return: sorted list of main_routes
		"""

		sorted_runs = copy(runs)
		sorted_runs.sort(key=lambda run: run.date)
		return sorted_runs

	def __init__(self, runs: List[Run] = None, date: datetime.date = None) -> None:
		"""Combines main_routes into a sorted list

		:param runs: a list of Run objects, defaults to an empty list
		:param date: the date of the main_routes
		"""

		if runs is None:
			runs = []

		self._runs = Runs._sort_runs(runs)

		if date:
			self.date = date
			if self._runs and self._runs[0].date != self.date:
				raise ValueError("Date corresponds to earliest run")
		else:
			self.date = None if not self._runs else self._runs[0].date

	def empty(self) -> bool:
		"""computes whether or not _runs is empty

		:return: whether or not _runs is empty
		"""

		return False if self._runs else True

	def __str__(self) -> str:
		"""converts Runs object into a string

		:return: representative string
		"""

		return str(self._runs)

	def __len__(self) -> int:
		"""Gets length of Runs object

		:return: number of main_routes in objet
		"""

		return len(self._runs)

	def __getitem__(self, key: int) -> Run:
		"""returns item with associated self._runs index

		:param key: int corresponding to self._runs index
		:return: requested Run object
		"""

		return self._runs[key]

	def add_all(self, runs: List[Run]) -> None:
		"""Merges a Runs object and a list of Run objects into a single Runs object

		:param runs: Runs object to be merged
		"""

		# Sort inputs in nondecreasing order
		sorted_runs = Runs._sort_runs(runs)
		_runs_copy = copy(self._runs)

		# Increase length of self._runs
		self._runs = sorted_runs + _runs_copy

		# Implement Merge algorithm
		sorted_runs.append(Run(date=datetime.date.max))
		_runs_copy.append(Run(date=datetime.date.max))
		i = 0
		j = 0
		for k in range(len(self._runs)):
			if sorted_runs[i].date <= _runs_copy[j].date:
				self._runs[k] = sorted_runs[i]
				i += 1
			else:
				self._runs[k] = _runs_copy[j]
				j += 1

	def add(self, run: Run) -> None:
		"""Adds a Run object to a Runs object

		:param run: Run to be added
		"""

		self.add_all([run])

	def extend(self, runs_instance: "Runs") -> None:
		"""Combines two Runs instances

		:param runs_instance: Runs object to be added
		"""

		self.add_all(runs_instance._runs)

	def interval(self, start_date, end_date):
		"""gets all main_routes in a time interval

		kw args:
			start_date -- date object

			end_date -- date object
		"""
		if start_date > end_date:
			raise ValueError("Invalid interval")

		else:
			if self._runs:
				interval_runs = []
				for run in self._runs:
					if run.date > end_date:
						break
					elif run.date >= start_date:
						interval_runs.append(run)
				return Runs(interval_runs)

			else:
				return Runs()

	def last(self):
		"""Gets the most recent run

		kw args:
			self -- Runs object
		"""
		if not self.empty():
			return self._runs[-1]
		else:
			return Run()

	def first(self):
		"""Gets the first recorded run

		kw args:
			self -- Runs object
		"""
		if not self.empty():
			return self._runs[0]
		else:
			return Run()

	def one_day(self):
		"""Computes whether all Run objects have the same date

		kw args:
			self -- Runs object
		"""
		if not self.empty():
			first_run = self.first()
			for run in self._runs:
				if run.date != first_run.date:
					return False
			return True
		else:
			return True

	def daily(self):
		"""combines Runs objects together based on day

		kw args:
			self -- Runs object
		"""
		if self.empty():
			return []
		elif self.one_day():
			return [self]
		else:
			current_date = self.first().date
			daily_runs = [Runs(date=current_date)]
			for run in self._runs:
				if run.date == current_date:
					daily_runs[-1].add(run)
				else:
					daily_runs.append(Runs([run]))
					current_date = run.date
			return daily_runs

	def daily_distances_between(self, start_date, end_date):
		"""returns a list of distances run daily in specified interval

		kw args:
			start_date -- Date object

			end_date -- Date object
		"""
		daily_runs = self.interval(start_date, end_date).daily()
		totals = []
		current_date = start_date
		i = 0

		while current_date <= end_date:
			if i < len(daily_runs) and daily_runs[i].date == current_date:
				totals.append(daily_runs[i].sum())
				i += 1

			else:
				totals.append(0)

			current_date += datetime.timedelta(days=1)

		return totals

	def sum(self):
		"""Sums the distances of main_routes in the instance

		kw args:
			self -- Runs object
		"""
		return float(reduce(lambda total, run: total + float(run.distance), self._runs, 0))

	def longest_run(self):
		"""returns Run object with highest distance

		kw args;
			self -- Runs object
		"""
		return max(self._runs, key=lambda run: float(run.distance))

	def average(self):
		"""computes average run distance

		kw args:
			self -- Runs object
		"""
		if len(self):
			sum_runs = self.sum()
			return float(sum_runs) / len(self)
		else:
			return 0
