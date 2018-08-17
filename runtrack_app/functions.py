'''
File that contains functions that will be useful throughout
the application
'''
from datetime import date, datetime, timedelta
import calendar
from copy import copy

def sort_runs(runs):
	'''
	sorts a list of Run objects by Run.started_at

	kw args:
		runs - a list of Run objects
	'''
	sorted_runs = copy(runs)
	sorted_runs.sort(key = lambda run: run.started_at)
	return sorted_runs

def group_runs_daily(runs, start_date=None, end_date=date.today(), distances=False):
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

		distances - a boolean.  If true, the elements of the nested lists will
			be floats that correspond to the distances of the runs.  Otherwise,
			the elements of the nested lists will be the Run objects themselves
	'''
	sorted_runs = sort_runs(runs)

	if not start_date:
		start_date = sorted_runs[0].started_at.date()

	grouped_runs = []
	day = end_date
	while day >= start_date:
		daily_runs = []
		while len(sorted_runs) and sorted_runs[-1].started_at.date() == day:
			if distances:
				daily_runs.append(float(sorted_runs.pop().distance))
			else:
				daily_runs.append(sorted_runs.pop())
		grouped_runs.append(daily_runs)
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
	grouped_runs = group_runs_daily(runs, start_date=start_date, end_date=end_date, distances=True)
	return list(map(lambda run: sum(run), grouped_runs))

def group_runs_weekly(runs, num_weeks=None, end_date=date.today(), distances=False):
	'''
	returns a list of lists that groups runs according to their weeks,
	between start_date and end_date (inclusive)

	kw args:
		runs - a list of Run objects

		num_weeks - an integer number of weeks to return, defaults to zero and
			returns all weeks in record

		end_date - a datetime object that specifies which date the function
			should stop grouping runs together at, defaults to the current day

		distances - a boolean.  If true, the elements of the nested lists will
			be floats that correspond to the distances of the runs.  Otherwise,
			the elements of the nested lists will be the Run objects themselves
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
			if distances:
				weekly_runs.append(float(sorted_runs.pop().distance))
			else:
				weekly_runs.append(sorted_runs.pop())

		grouped_runs.append(weekly_runs)
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
	grouped_runs = group_runs_weekly(runs, num_weeks=num_weeks, end_date=end_date, distances=True)
	return list(map(lambda run: sum(run), grouped_runs))
