from runtrack_app import app, db

# import db in shell
@app.shell_context_processor
def make_shell_context():
	return {'db': db}

if __name__ == "__main__":
	from runtrack_app.classes import Runs, GoalRuns, GroupGoalRuns
	from runtrack_app.models import Run, Goal
	from datetime import date, timedelta

	print("Runs")