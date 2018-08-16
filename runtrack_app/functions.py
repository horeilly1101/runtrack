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

def group_runs(runs, start_date=None, end_date=date.today(), distances=False):
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
	grouped_runs = group_runs(runs, start_date=start_date, end_date=end_date, distances=True)
	i = list(map(lambda run: sum(run), grouped_runs))
	print("GROUP "+str(grouped_runs))
	print(i)
	return i



print("hi")