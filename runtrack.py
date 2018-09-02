from runtrack_app import app, db

# import db in shell
@app.shell_context_processor
def make_shell_context():
	return {'db': db}

if __name__ == "__main__":
	from runtrack_app.classes import Runs, GoalRuns, GroupGoalRuns
	from runtrack_app.models import Run, Goal
	from datetime import date, timedelta

	today = date.today()
	runs = []
	for i in range(0, 14):
		runs.append(Run(distance = 2 * i, date=today-timedelta(days=i)))

	goals = []
	for i in range(0, 14, 2):
		goals.append(Goal(distance = 2 * i, date=today-timedelta(days=i)))

	ggr = GroupGoalRuns(goals, runs)
	for gr in ggr:
		print(gr)

	print("sum runs", ggr.sum_runs())