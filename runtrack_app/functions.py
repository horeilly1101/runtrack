'''
File that contains functions that will be useful throughout
the application
'''
from datetime import date, datetime, timedelta
import calendar
import math
from copy import copy
from functools import reduce
from runtrack_app.models import Run, Goal
from flask_login import current_user, login_required

def sort_runs(runs):
	'''
	sorts a list of Run objects by Run.started_at
	kw args:
		runs - a list of Run objects
	'''
	sorted_runs = copy(runs)
	sorted_runs.sort(key = lambda run: run.started_at)
	return sorted_runs

def sort_goals(goals):
	'''
	sorts a list of Goal objects by Goal.date
	kw args:
		goals - a list of Goal objects
	'''
	sorted_goals = copy(goals)
	sorted_goals.sort(key = lambda goal: goal.date)
	return sorted_goals

def sum_runs(runs):
	'''
	returns the sum of a list of Run objects
	kw args:
		runs - a list of Run objects
	'''
	return sum(list(map(lambda run: float(run.distance), runs)))

def group_runs_daily(runs, 
	start_date=None, 
	end_date=date.today()):
	'''
	returns a list of lists that groups runs according to their days,
	between start_date and end_date (inclusive)
	kw args:
		runs - a list of Run objects
		start_date - a datetime object that specifies which date the function
			should begin grouping runs together at, defaults to the first date the
			user has a run recorded at
		end_date - a datetime object that specifies which date the function
			should stop grouping runs together at, defaults to the current day
	'''
	sorted_runs = sort_runs(runs)

	if not start_date:
		start_date = sorted_runs[0].started_at.date()

	grouped_runs = []
	day = end_date
	while day >= start_date:
		daily_runs = []
		while len(sorted_runs) and sorted_runs[-1].started_at.date() == day:
			daily_runs.append(sorted_runs.pop())
		grouped_runs.append(daily_runs[::-1])
		day -= timedelta(days=1)

	grouped_runs.reverse()
	return grouped_runs

def total_daily_distances(runs, start_date=None, end_date=date.today()):
	'''
	returns a list of floats, where the floats represent total running distances
	for each day between start_date and end_date (inclusive)
	kw args:
		runs - a list of Run objects
		start_date - a datetime object that specifies which date the function
			should begin grouping runs together at, defaults to the first date the
			user has a run recorded at
		end_date - a datetime object that specifies which date the function
			should stop grouping runs together at, defaults to the current day
	'''
	grouped_runs = group_runs_daily(runs, start_date=start_date, end_date=end_date)
	return list(map(lambda run: sum_runs(run), grouped_runs))

def group_runs_weekly(runs, 
	num_weeks=None, 
	end_date=date.today()):
	'''
	returns a list of lists that groups runs according to their weeks,
	between start_date and end_date (inclusive)
	kw args:
		runs - a list of Run objects
		num_weeks - an integer number of weeks to return, defaults to zero and
			returns all weeks in record
		end_date - a datetime object that specifies which date the function
			should stop grouping runs together at, defaults to the current day
	'''
	sorted_runs = sort_runs(runs)
	last_monday = end_date - timedelta(days=end_date.weekday())

	if num_weeks:
		start_date = last_monday - timedelta(days=7 * (num_weeks - 1))
	else:
		start_date = sorted_runs[0].started_at.date()

	grouped_runs = []
	day = last_monday
	while day >= start_date - timedelta(days=start_date.weekday()):
		weekly_runs = []
		while len(sorted_runs) and sorted_runs[-1].started_at.date() >= day:
			weekly_runs.append(sorted_runs.pop())

		grouped_runs.append(weekly_runs[::-1])
		day -= timedelta(days=7)

	grouped_runs.reverse()
	return grouped_runs

def total_weekly_distances(runs, num_weeks=None, end_date=date.today()):
	'''
	returns a list of floats, where the floats represent total running distances
	for each day between start_date and end_date (inclusive)
	kw args:
		runs - a list of Run objects
		start_date - a datetime object that specifies which date the function
			should begin grouping runs together at, defaults to the first date the
			user has a run recorded at
		end_date - a datetime object that specifies which date the function
			should stop grouping runs together at, defaults to the current day
	'''
	grouped_runs = group_runs_weekly(runs, num_weeks=num_weeks, end_date=end_date)
	return list(map(lambda run: sum_runs(run), grouped_runs))

def group_runs_daily_and_weekly(runs, num_weeks=None, end_date=date.today()):
	'''
	returns a list of lists of lists that groups runs according to their weeks
	and days, between start_date and end_date (inclusive)
	kw args:
		runs - a list of Run objects
		num_weeks - an integer number of weeks to return, defaults to zero and
			returns all weeks in record
		end_date - a datetime object that specifies which date the function
			should stop grouping runs together at, defaults to the current day
	'''
	weekly_grouped_runs = group_runs_weekly(runs, num_weeks=num_weeks, end_date=end_date)

	last_monday = end_date - timedelta(days=end_date.weekday())
	if num_weeks:
		start_date = last_monday - timedelta(days=7 * (num_weeks - 1))
	else:
		start_date = weekly_grouped_runs[0][0].started_at.date()
		num_weeks = math.ceil((end_date - start_date).days / 7)

	grouped_runs = []
	for week in range(num_weeks):
		day_end = start_date + timedelta(days=6-start_date.weekday()) \
			if start_date <= end_date else end_date

		grouped_runs.append(group_runs_daily(weekly_grouped_runs[week], start_date=start_date, end_date=day_end))
		start_date += timedelta(days=7)

	return grouped_runs

def last_goal(goals):
	'''
	returns the last day a goal is recorded for.  Designed to run faster than 
	sort_goals
	kw args:
		goals - a list of Goal objects
	'''
	last_date = date.min
	for goal in goals:
		if goal.date > last_date:
			last_date = goal.date
	return last_date

def combine_daily(runs, goals):
	'''
	returns a list of 2-tuples, where the tuples contain a goal, and all runs for 
	the day in a list (e.g. tuple([goal, run_list])).  The days are in order from 
	least to most recent.  If there is a goal for a given day, it will be the first 
	element in the list.
	kw args:
		runs - a list of Run objects
	'''
	# get grouped runs and filter out days with no runs
	end_date = date.today()
	grouped_runs = group_runs_daily(runs, start_date=None, end_date=end_date)
	filtered_runs = list(filter(lambda run: run, grouped_runs))

	# sort goals by date
	sorted_goals = sort_goals(goals)

	# initialize variables and iterate through sequences
	i, j = (0, 0)
	combined_seq = []
	while i < len(filtered_runs) or j < len(sorted_goals):
		if (j == len(sorted_goals)):
			combined_seq.append((Goal(distance=0, date=filtered_runs[i][0].started_at.date()), filtered_runs[i]))
			i += 1
		elif (i == len(filtered_runs)):
			combined_seq.append((sorted_goals[j], [Run(distance=0)]))
			j += 1
		elif (filtered_runs[i][0].started_at.date() < sorted_goals[j].date):
			combined_seq.append((Goal(distance=0, date=filtered_runs[i][0].started_at.date()), filtered_runs[i]))
			i += 1
		elif (filtered_runs[i][0].started_at.date() > sorted_goals[j].date):
			combined_seq.append((sorted_goals[j], [Run(distance=0)]))
			j += 1
		elif filtered_runs[i][0].started_at.date() == sorted_goals[j].date:
			combined_seq.append((sorted_goals[j], filtered_runs[i]))
			i += 1
			j += 1
	return combined_seq

def combine_daily_and_weekly(runs, goals):
	'''
	returns a list of lists of 2-tuples, where the tuples contain a goal, and all runs for 
	the day in a list (e.g. tuple([goal, run_list])).  The days are in order from 
	least to most recent.  If there is a goal for a given day, it will be the first 
	element in the list.
	kw args:
		runs - a list of Run objects
		goals - a list of Goal objects
	'''
	last_goal_date = last_goal(goals)
	end_date = date.today() if last_goal_date <= date.today() else last_goal_date

	combined_daily = combine_daily(runs, goals)
	last_monday = end_date - timedelta(days=end_date.weekday())

	start_date = combined_daily[0][0].date

	combined_weekly = []
	day = last_monday
	while day >= start_date - timedelta(days=start_date.weekday()):
		weekly_runs = []
		while len(combined_daily) and combined_daily[-1][0].date >= day:
			weekly_runs.append(combined_daily.pop())

		combined_weekly.append(weekly_runs)
		day -= timedelta(days=7)

	return combined_weekly[::-1]

def combined_summary(combined_seq):
	'''
	returns the total run and goal distances in a list that has the same form as
	the output of combine_daily
	kw args:
		combined_seq - a list of tuples where the first element is a Goal object
			and the second is a list of Run objects
	'''
	goal_total = 0
	run_total = 0
	num_runs = 0
	daily_run_totals = [0] * 7
	all_run_totals = []

	for goal, runs in combined_seq:
		goal_total += float(goal.distance)
		num_runs += len(runs)
		daily_run_totals[goal.date.weekday()] = sum_runs(runs)
		all_run_totals.extend(list(map(lambda run: float(run.distance), runs)))

	run_total = sum(daily_run_totals)
	return (goal_total, 
		run_total, 
		daily_run_totals, 
		all_run_totals, num_runs)