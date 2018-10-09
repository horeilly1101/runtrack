'''Contains GoalRuns class

classes:
	GoalRuns -- combines a goal and Runs object into a 2-tuple
'''

from datetime import date, timedelta
import calendar
from copy import copy
from functools import reduce
from runtrack_app.models import Run, Goal
from .runs import Runs

class GoalRuns():
	'''Combines a Goal object with a Runs object

	kw args:
		goal -- a Goal object

		runs -- a Runs object

	instance variables:
		_goalruns - a 2-tuple of a Goal object and a GoalRuns object

		goal -- a Goal object

		runs -- a Runs object

	public methods:
		diff -- gets the difference between total run distance and goal
	'''
	def __init__(self, goal=Goal(distance=0), runs=Runs(), date=None):
		'''initializes GoalRuns object

		kw args:
			self -- GoalRuns object

			goal -- Goal object

			runs -- Runs object

		instance variables:
			goal -- Goal object

			runs -- Runs object

			date -- date of GoalRun (must be the same for goal and runs)

		methods:
			diff - returns difference between sum of runs and goal distances

			sum -- returns sum of run distances

			num_runs -- returns total number of runs

			add_run -- adds a run
		'''
		# ensure goal, runs, and date all refer to same date
		if date:
			if (goal.date and goal.date != date) or (runs.one_day() and not runs.empty() and runs.first().date != date):
				raise ValueError("Goal, runs, and date should all have same date")
			else:
				self.date = date

		elif goal.date and runs.empty():
			self.date = goal.date

		elif not goal.date and (not runs.empty() and runs.one_day()):
			self.date = runs.first().date

		elif goal.date and (not runs.empty() and runs.one_day()):
			if goal.date == runs.first().date:
				self.date = goal.date
			else:
				raise ValueError("Goal and Runs should have same date")

		else:
			raise ValueError("Must define at least one kw argument")

		# set remaining instance variables
		self.runs = runs
		self.goal = goal


	def __str__(self):
		'''converts GoalRuns object into a string

		kw args:
			self -- GoalRuns object
		'''
		return str((self.goal, self.runs))

	def diff(self):
		'''gets the difference between total run distance and goal

		kw args:
			self -- GoalRuns object
		'''
		return self.runs.sum() - float(self.goal.distance)

	def sum(self):
		'''gets the sum of all run distances

		kw args:
			self -- GoalRuns object
		'''
		return self.runs.sum()

	def num_runs(self):
		'''gets total number of runs in GoalRuns object

		kw args:
			self -- GoalRuns object
		'''
		return len(self.runs)

	def add_run(self, run):
		'''adds a Run object to GoalRuns object

		kw args:
			self -- GoalRun object

			run -- Run object
		'''
		if not run.date or run.date != self.date:
			raise ValueError("Run must have same date as GoalRuns")
		else:
			self.runs.add(run)

	def readable_runs(self):
		'''returns runs in a readable string

		self -- GoalRuns object
		'''
		str_runs = 0 if not len(self.runs) else str(self.runs.first().distance)
		for run in self.runs[1:]:
			str_runs += " + " + str(run.distance)
		return str_runs