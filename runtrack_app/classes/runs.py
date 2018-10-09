'''Contains Runs class

classes:
	Runs -- combines runs into a sorted list
'''

from datetime import date, timedelta
import calendar
from copy import copy
from functools import reduce
from runtrack_app.models import Run, Goal

class Runs():
	'''Combines runs into a sorted list

	kw args:
		runs -- a list of Run objects

	instance variables:
		_runs -- a list of runs sorted in nondecreasing order by date

	public methods:
		add_all -- Merges a Runs object and a list of Run objects into 
			a single Runs object

		add -- adds a run in the correct order

		extend -- combines two Runs objects

		interval -- gets all runs within a time interval

		last -- returns most recent run

		first -- returns least recent run

		one_day -- returns True if all runs on same day, false otherwise

		daily_distances_between -- returns list of distance totals between two dates

		sum -- returns sum of all run distances
	'''
	def __sort_runs(runs):
		'''sorts a list of Run objects in nondecreasing order by date

		kw args:
			runs -- a list of Run objects
		'''
		sorted_runs = copy(runs)
		sorted_runs.sort(key = lambda run: run.date)
		return sorted_runs

	def __init__(self, runs=[], date=None):
		'''Combines runs into a sorted list

		kw args:
			self -- Runs object

			runs -- a list of Run objects, defaults to an empty list
		'''
		self._runs = Runs.__sort_runs(runs)
		if date:
			self.date = date
			if self._runs and self._runs[0].date != self.date:
				raise ValueError("Date corresponds to earliest run")
		else:
			self.date = None if not self._runs else self._runs[0].date

	def empty(self):
		'''computes whether or not _runs is empty

		kw args:
			self -- Runs object
		'''
		return False if self._runs else True

	def __str__(self):
		'''converts Runs object into a string

		kw args:
			self -- Runs object
		'''
		return str(self._runs)

	def __len__(self):
		'''Gets length of Runs object

		kw args:
			self -- Runs object
		'''
		return len(self._runs)

	def __getitem__(self, key):
		'''returns item with associated self._runs index

		kw args:
			self -- Runs object

			key -- Integer corresponding to self._runs index
		'''
		return self._runs[key]

	def add_all(self, runs):
		'''Merges a Runs object and a list of Run objects into a single Runs object

		kw args:
			self -- Runs object

			runs -- a list of run objects
		'''
		# Sort inputs in nondecreasing order
		sorted_runs = Runs.__sort_runs(runs)
		_runs_copy = copy(self._runs)

		# Increase length of self._runs
		self._runs = sorted_runs + _runs_copy

		# Implement Merge algorithm
		sorted_runs.append(Run(date=date.max))
		_runs_copy.append(Run(date=date.max))
		i = 0
		j = 0
		for k in range(len(self._runs)):
			if sorted_runs[i].date <= _runs_copy[j].date:
				self._runs[k] = sorted_runs[i]
				i += 1
			else:
				self._runs[k] = _runs_copy[j]
				j += 1

	def add(self, run):
		'''Adds a Run object to a Runs object

		kw args:
			self -- Runs object

			run -- Run object
		'''
		self.add_all([run])

	def extend(self, runs_instance):
		'''Combines two Runs instances

		kw args:
			self -- Runs object

			runs_instance -- Runs object
		'''
		self.add_all(runs_instance._runs)

	def interval(self, start_date, end_date):
		'''gets all runs in a time interval

		kw args:
			start_date -- date object

			end_date -- date object
		'''
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
		'''Gets the most recent run

		kw args:
			self -- Runs object
		'''
		if not self.empty():
			return self._runs[-1]
		else:
			return Run()

	def first(self):
		'''Gets the first recorded run

		kw args:
			self -- Runs object
		'''
		if not self.empty():
			return self._runs[0]
		else:
			return Run()

	def one_day(self):
		'''Computes whether all Run objects have the same date

		kw args:
			self -- Runs object
		'''
		if not self.empty():
			first_run = self.first()
			for run in self._runs:
				if run.date != first_run.date:
					return False
			return True
		else:
			return True


	def daily(self):
		'''combines Runs objects together based on day

		kw args:
			self -- Runs object
		'''
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
		'''returns a list of distances run daily in specified interval

		kw args:
			start_date -- Date object

			end_date -- Date object
		'''
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

			current_date += timedelta(days=1)

		return totals

	def sum(self):
		'''Sums the distances of runs in the instance

		kw args:
			self -- Runs object
		'''
		return float(reduce(lambda total, run: total + float(run.distance), self._runs, 0))

	def longest_run(self):
		'''returns Run object with highest distance

		kw args;
			self -- Runs object
		'''
		return max(self._runs, key=lambda run: float(run.distance))

	def average(self):
		'''computes average run distance

		kw args:
			self -- Runs object
		'''
		if len(self):
			sum_runs = self.sum()
			return float(sum_runs) / len(self)
		else:
			return 0