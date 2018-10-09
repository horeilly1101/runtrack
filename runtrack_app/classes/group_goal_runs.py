'''Contains GroupGoalRuns and GroupGoalRunsWeekly classes

classes:
	GroupGoalRuns -- combines GoalRuns objects into a list

	GroupGoalRunsWeekly -- subclass of GroupGoalRuns
'''

from datetime import date, timedelta
import calendar
from copy import copy
from functools import reduce
from runtrack_app.models import Run, Goal
from .runs import Runs
from .goalruns import GoalRuns

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
		sorted_goals = copy(goals)
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
		runs_copy = copy(runs)
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

	def __init__(self, goals=[], runs=[]):
		'''initializes GroupGoalRuns object (a list of GoalRuns objects)

		kw args:
			goals -- list of Goal objects

			runs - list of Run objects
		'''
		# grouped goal runs
		if len(goals) or len(runs):
			self._ggr = GroupGoalRuns.__combine_goals_runs(goals, runs)
		else:
			self._ggr = []

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
		return reduce(lambda total, goalruns: total + float(goalruns.goal.distance), self._ggr, 0)

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

		daily_distances -- returns a list of total daily distances

		name -- returns name of the week

		average_run -- returns length of average run
	'''
	def __init__(self, monday, goals=[], runs=[]):
		GroupGoalRuns.__init__(self, goals, runs)
		self._wggr = self._ggr
		self.monday = monday
		self.sunday = monday + timedelta(days=6)

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
		return (diff, (diff * 100) / wggr.sum_runs())

	def compare_longest_run(self, ggr):
		'''
		returns the difference and percent increase in distancs between longest
		runs of two wggr objects

		kw args:
			self -- a GroupGoalRunsWeekly object

			wggr -- a GroupGoalRunsWeekly object
		'''
		diff = self.longest_run() - wggr.longest_run()
		perc = 0 if not wggr.longest_run() else diff / wggr.longest_run()
		return (diff, perc)

	def daily_distances(self):
		'''computes total distances for each day

		self -- GroupGoalRunsWeekly object
		'''
		runs = Runs()
		for gr in self._wggr:
			runs.extend(gr.runs)
		return runs.daily_distances_between(self.monday, self.monday + timedelta(days=6))

	def name(self):
		'''names a week

		kw args:
			self -- GroupGoalRunsWeekly object
		'''
		monday = self.monday
		sunday = monday + timedelta(days=6)
		monday_str = calendar.month_abbr[monday.month] + " " + str(monday.day)
		if monday.month == sunday.month:
			return monday_str + " - " + str(sunday.day)
		else:
			sunday_str = calendar.month_abbr[sunday.month] + " " + str(sunday.day)
			return monday_str + " - " + sunday_str

	def average_run(self):
		'''computes length of average run

		kw args:
			self -- wggr object
		'''
		runs = Runs()
		for goalruns in self._wggr:
			runs.extend(goalruns.runs)
		return runs.average()

# Define methods for GroupGoalRuns

def add_dummy_weeks(combined):
	'''adds empty lists if weeks are skipped in weekly function

	kw args:
		combined -- list of GroupGoalRunsWeekly object
	'''
	current_date = combined[0].monday
	end_date = date.today()

	i = 0
	while current_date <= end_date:
		if i >= len(combined) or combined[i].monday > current_date:
			combined = combined[:i] + [GroupGoalRunsWeekly(monday=current_date)] + combined[i:]
		else:
			i += 1
		current_date += timedelta(days=7)

	return combined

def weekly(self, dummy=False, at_least=0):
	'''combines GroupGoalRuns object by week

	kw args:
		self -- GroupGoalRuns object

		dummy -- includes weeks with no runs if True

		at_least -- minimum length of output
	'''
	combined = []

	if len(self):
		# initialize values
		monday = self.first_monday()
		sunday = monday + timedelta(days=6)
		goals, runs = [], []

		# combine the objects by week
		for goalruns in self._ggr:
			if goalruns.date <= sunday:
				if float(goalruns.goal.distance) > 0:
					goals.append(goalruns.goal)
				runs.extend(goalruns.runs._runs)

			elif goalruns.date > sunday:
				# Clean up
				combined.append(GroupGoalRunsWeekly(goals=goals, runs=runs, monday=monday))
				monday, sunday = monday + timedelta(days=7), sunday + timedelta(days=7)
				runs, goals = [], []

				if float(goalruns.goal.distance) > 0:
					goals.append(goalruns.goal)
				runs.extend(goalruns.runs._runs)

		# add last week
		if goals or runs:
			combined.append(GroupGoalRunsWeekly(goals=goals, runs=runs, monday=monday))

		if dummy:
			combined = GroupGoalRuns.__add_dummy_weeks(combined)

		while len(combined) < at_least:
			combined = [GroupGoalRunsWeekly(monday=combined[0].monday - timedelta(days=7))] + combined

		return combined

	else:
		today = date.today()
		start_date = today - timedelta(days=today.weekday())

		while len(combined) < at_least:
			combined = [GroupGoalRunsWeekly(monday=start_date)] + combined
			start_date -= timedelta(days=7)

		return combined

def weekly_distances(combined):
	'''returns weekly total distances

	kw args:
		combined -- output of weekly (dummy=True)
	'''
	return list(map(lambda goalruns: goalruns.sum_runs(), combined))

# Add methods to class
GroupGoalRuns.__add_dummy_weeks = add_dummy_weeks
GroupGoalRuns.weekly = weekly
GroupGoalRuns.weekly_distances = weekly_distances