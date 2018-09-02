from runtrack_app import app, db

# import db in shell
@app.shell_context_processor
def make_shell_context():
	return {'db': db}

if __name__ == "__main__":
	from runtrack_app.classes import Runs, GoalRuns
	from runtrack_app.models import Run, Goal
	from datetime import date, timedelta

	today = date.today()
	runs = []
	for i in range(0, 14):
		runs.append(Run(distance = 2 * i, date=today-timedelta(days=i)))

	gr = GoalRuns(runs = Runs([Run(date=today-timedelta(days=1))]), date = today)

	print(gr)