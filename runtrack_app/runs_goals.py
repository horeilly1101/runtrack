'''
File that contains the primary data structure of the applcation,
a list of 2-tuples that each contain a goal and a set of runs
that occurred on that day.
'''
from datetime import date, datetime, timedelta
import calendar
import math
from copy import copy
from functools import reduce
from runtrack_app.models import Run, Goal
from flask_login import current_user, login_required

def combine_runs_goals(runs, goals):
	'''
	Takes a list of runs and a list of goals and returns 
	'''

class RunsGoals():
	def __init__(runs = [], goals = []):
		self._runs = runs
		self._goals = goals