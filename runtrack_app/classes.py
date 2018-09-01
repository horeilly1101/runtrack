'''Contains objects crucial to the app design

classes:
	Runs -- combines runs into a sorted list
'''

from datetime import date, datetime, timedelta
import calendar
import math
from copy import deepcopy
from functools import reduce
from runtrack_app.models import Run, Goal
from flask_login import current_user, login_required

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
	'''
	def __sort_runs(runs):
		'''sorts a list of Run objects in nondecreasing order by date

		kw args:
			runs -- a list of Run objects
		'''
		sorted_runs = deepcopy(runs)
		sorted_runs.sort(key = lambda run: run.date)
		return sorted_runs

	def __init__(self, runs=[]):
		'''Combines runs into a sorted list

		kw args:
			self -- Runs object

			runs -- a list of Run objects, defaults to an empty list
		'''
		self._runs = Runs.__sort_runs(runs)

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
		_runs_copy = deepcopy(self._runs)

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
			raise ValueError

		else:
			if self._runs:
				interval_runs = []
				for run in self._runs:
					if run.date > end_date:
						break
					elif run.date > start_date:
						interval_runs.append(run)
				return interval_runs

			else:
				return []

	def last(self):
		'''Gets the most recent run

		kw args:
			self -- Runs object
		'''
		if len(self._runs):
			return self._runs[-1]
		else:
			return None

	def first(self):
		'''Gets the first recorded run

		kw args:
			self -- Runs object
		'''
		if len(self._runs):
			return self._runs[0]
		else:
			return None

	def sum(self):
		'''Sums the distances of runs in the instance

		kw args:
			self -- Runs object
		'''
		return float(reduce(lambda total, run: total + run.distance, self._runs, 0))

class RunsGoals():
	def __init__(self, runs = [], goals = [], groupby = 1):
		self._runs = runs
		self._goals = goals