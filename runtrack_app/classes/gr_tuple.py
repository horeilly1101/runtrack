"""Contains GoalRuns class"""

from runtrack_app.models import Goal
from runtrack_app.classes.runs import Runs
import datetime


class GRTuple:
	"""Combines a Goal and a Runs into an effective 2-tuple."""

	def __init__(self, goal: Goal = Goal(distance=0), runs: Runs = Runs(), date: datetime.date = None) -> None:
		"""
		initialize the object. We assume that the goal and the runs are all on the same day.
		:param goal: the goal to be stored
		:param runs: the runs to be stored
		:param date: the date associated with the goals and runs (defaults to None)
		"""

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

	def __str__(self) -> str:
		"""converts GoalRuns object into a string"""

		return str((self.goal, self.runs))

	def diff(self) -> float:
		"""gets the difference between total run distance and goal"""

		return self.runs.sum() - float(self.goal.distance)

	def sum(self) -> float:
		"""gets the sum of all run distances"""

		return self.runs.sum()

	def num_runs(self) -> int:
		"""gets total number of runs in GoalRuns object"""

		return len(self.runs)

	def add_run(self, run) -> None:
		"""
		adds a Run object to GoalRuns object
		:param run: run to be added
		"""

		self.runs.add(run)

	def readable_runs(self) -> str:
		"""returns runs in a readable string"""

		str_runs = 0 if not len(self.runs) else str(self.runs.first().distance)
		for run in self.runs[1:]:
			str_runs += " + " + str(run.distance)
		return str_runs
