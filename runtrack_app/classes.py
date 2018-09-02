'''Contains objects crucial to the app design

classes:
	Runs -- combines runs into a sorted list

	GoalRuns -- combines a goal and Runs object into a 2-tuple

	GroupGoalRuns -- combines GoalRuns objects into a list

	GroupGoalRunsWeekly -- subclass of GroupGoalRuns
'''

from datetime import date, timedelta
from copy import deepcopy
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
		sorted_runs = deepcopy(runs)
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
				return []

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
		return float(reduce(lambda total, run: total + run.distance, self._runs, 0))

	def longest_run(self):
		'''returns Run object with highest distance

		kw args;
			self -- Runs object
		'''
		return max(self._runs, key=lambda run: run.distance)

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
		return self.runs.sum() - self.goal.distance

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

class GroupGoalRuns():
	'''Combines GoalRuns objects into a list

	kw args:
		goals -- list of Goal objects

		runs -- list of Run objects

	instance variables:
		_ggr -- a list of GoalRuns objects

	public methods:
		first -- returns the earliest GoalRuns object

		sum_goals -- returns the sum of distance of all Goal objects

		sum_runs -- returns the sum of distances of all Runs objects

		num_runs -- returns the number of runs

		first_monday -- returns a Date instance of the first Monday

		weekly -- returns a list of GroupGoalRunsWeekly objects

		diff -- returns difference between total sums of runs and goals
	'''
	def __sort_goals(goals):
		'''static method that sorts a list of goals by date

		kw args:
			goals -- a list of Goal objects
		'''
		sorted_goals = deepcopy(goals)
		sorted_goals.sort(key=lambda goal: goal.date)
		return sorted_goals

	def __combine_goals_runs(goals, runs):
		'''combines a goals and Runs objects into a list of GoalRuns

		kw args:
			goals -- a list of Goal objects

			runs -- a list of Run objects
		'''
		# copy inputs
		goals_copy = GroupGoalRuns.__sort_goals(goals)
		runs_copy = deepcopy(runs)
		runs_daily = Runs(runs_copy).daily()

		# implement a variation of Merge algorithm
		combined = []
		goals_copy.append(Goal(date=date.max))
		runs_daily.append(Runs([Run(date=date.max)]))

		i = 0
		j = 0
		while goals_copy[i].date != date.max or runs_daily[j].date != date.max:
			if goals_copy[i].date == runs_daily[j].date:
				combined.append(GoalRuns(goal=goals_copy[i], runs=runs_daily[j]))
				i, j = i + 1, j + 1

			elif goals_copy[i].date < runs_daily[j].date:
				combined.append(GoalRuns(goal=goals_copy[i]))
				i += 1

			else:
				combined.append(GoalRuns(runs=runs_daily[j]))
				j += 1

		return combined

	def __init__(self, goals, runs):
		'''initializes GroupGoalRuns object (a list of GoalRuns objects)

		kw args:
			goals -- list of Goal objects

			runs - list of Run objects
		'''
		# grouped goal runs
		self._ggr = GroupGoalRuns.__combine_goals_runs(goals, runs)

	def __str__(self):
		'''converts GroupGoalRuns into string

		kw args:
			self -- GroupGoalRuns object
		'''
		return str(self._ggr)

	def __len__(self):
		'''gets length of GroupGoalRuns objects

		kw args:
			self -- GroupGoalRuns object
		'''
		return len(self._ggr)

	def __getitem__(self, key):
		'''returns item with associated self._ggr index

		kw args:
			self -- GroupGoalRuns object

			key -- Integer corresponding to self._ggr index
		'''
		return self._ggr[key]

	def first(self):
		'''gets earliest GoalRun object recorded

		kw args:
			self -- GroupGoalRun object
		'''
		if len(self):
			return self._ggr[0]

	def sum_goals(self):
		'''computes total goal distances

		kw args:
			self -- GroupGoalRuns object
		'''
		return reduce(lambda total, goalruns: total + goalruns.goal.distance, self._ggr, 0)

	def sum_runs(self):
		'''computes total run distances

		kw args:
			self -- GroupGoalRuns object
		'''
		return reduce(lambda total, goalruns: total + goalruns.sum(), self._ggr, 0)

	def num_runs(self):
		'''computes total number of runs

		kw args:
			self -- GroupGoalRuns object
		'''
		return reduce(lambda total, goalruns: total + goalruns.num_runs(), self._ggr, 0)

	def first_monday(self):
		'''
		computes the first day (Monday) of the first week where a GoalRun is recorded

		kw args:
			self -- GroupGoalRun object
		'''
		if len(self):
			first_date = self.first().date
			return first_date - timedelta(days=first_date.weekday())

	def diff(self):
		'''returns difference between total runs and total goals

		kw args:
			self -- GroupGoalRuns object
		'''
		return self.sum_runs() - self.sum_goals()

class GroupGoalRunsWeekly(GroupGoalRuns):
	'''group goalruns objects into a list

	super class:
		GroupGoalRuns

	kw args:
		goals -- a list of Goal objects

		runs -- a list of Run objects

		monday -- a date object

		sunday -- a date object

	instance variables:
		_ggr -- a list of GoalRuns objects (inherits)

		_wggr -- a list of GoalRuns objects

		monday -- a date object

		sunday -- a date object

	methods: 
		(inherited from GroupGoalRuns class)

		longest_run -- returns Run instance of the longest run

		compare_distance -- returns the difference in distance between two wggr instances

		compare_longest_run -- returns the difference in longest runs between two wggr instances
	'''
	def __init__(self, goals, runs, monday, sunday):
		GroupGoalRuns.__init__(self, goals, runs)
		self._wggr = self._ggr
		self.monday = monday
		self.sunday = sunday

	def longest_run(self):
		'''returns Run object of longest run

		kw args:
			self -- GroupGoalRunsWeekly object
		'''
		runs = Runs()
		for goalruns in self._wggr:
			runs.extend(goalruns.runs)
		return runs.longest_run()

	def compare_distance(self, wggr):
		'''returns the difference and percent increase in distances between two wggr objects

		kw args:
			self -- a GroupGoalRunsWeekly object

			wggr -- a GroupGoalRunsWeekly object
		'''
		diff = self.sum_runs() - wggr.sum_runs()
		return (diff, diff / wggr.sum_runs())

	def compare_longest_run(self, ggr):
		'''
		returns the difference and percent increase in distancs between longest
		runs of two wggr objects

		kw args:
			self -- a GroupGoalRunsWeekly object

			wggr -- a GroupGoalRunsWeekly object
		'''
		diff = self.longest_run() - wggr.longest_run()
		return (diff, diff / wggr.longest_run())

def __add_dummy_weeks(combined):
	'''adds empty lists if weeks are skipped in weekly function

	kw args:
		combined -- list of GroupGoalRunsWeekly object
	'''
	# last_monday = combined[0].monday
	# for week in combined:
	# 	if week.monday - last_monday > timedelta(days=7):
	pass

# Define method for GroupGoalRuns
# BROKEN
def weekly(self, dummy=False):
	'''combines GroupGoalRuns object by week

	kw args:
		self -- GroupGoalRuns object
	'''
	# initialize values
	monday = self.first_monday()
	sunday = monday + timedelta(days=6)
	combined, goals, runs = [], [], []

	# combine the objects by week
	for goalruns in self._ggr:
		if goalruns.date <= sunday:
			if goalruns.goal.distance > 0:
				goals.append(goalruns.goal)
			runs.extend(goalruns.runs._runs)

		elif goalruns.date > sunday:
			# Clean up
			combined.append(GroupGoalRunsWeekly(goals=goals, runs=runs, monday=monday, sunday=sunday))
			monday, sunday = monday + timedelta(days=7), sunday + timedelta(days=7)
			runs, goals = [], []

			if goalruns.goal.distance > 0:
				goals.append(goalruns.goal)
			runs.extend(goalruns.runs._runs)

	if goals or runs:
		combined.append(GroupGoalRunsWeekly(goals=goals, runs=runs, monday=monday, sunday=sunday))

	# # update to current day
	# today = date.today()
	# while sunday < today:
	# 	monday, sunday = monday + timedelta(days=7), sunday + timedelta(days=7)
	# 	combined.append(GroupGoalRunsWeekly(goals=goals, runs=runs, monday=monday, sunday=sunday))

	return combined

# Add method to class
GroupGoalRuns.weekly = weekly

