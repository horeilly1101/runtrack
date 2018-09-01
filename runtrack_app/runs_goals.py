'''
File that contains the primary data structure of the applcation,
a list of 2-tuples that each contain a goal and a set of runs
that occurred on that day.
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

	methods:
		add -- adds a run in the correct order

		extend -- combines a run object

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

 	def extend(self, runs):
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

		# Implement Merge algorithmj
		sorted_runs.append(float("inf"))
		_runs_copy.append(float("inf"))
		i = 0
		j = 0
		for k in range(len(self._runs) + len(runs)):
			if sorted_runs[i] <= _runs_copy[j]:
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
		self.extend([run])

	def last(self):
		if len(self._runs):
			return self._runs[-1]
		else:
			return Run()

	def first(self):
		if len(self._runs):
			return self._runs[0]
		else:
			return Run()

class Goals():
	def __init__(self, goals = []):
		self._goals = goals

	def sort():
		sorted_goals = 

class RunsGoals():
	def __init__(self, runs = [], goals = [], groupby = 1):
		self._runs = runs
		self._goals = goals