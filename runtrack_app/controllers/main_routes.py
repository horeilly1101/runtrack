"""controllers that deal with a user's main_routes"""

from datetime import date, timedelta
from calendar import day_abbr, month_name

from flask import render_template, flash, redirect, Blueprint
from flask_login import current_user, login_required

from runtrack_app import db
from runtrack_app.views.forms import AddGoalForm, AddRunForm
from runtrack_app.models.tables import Run, Goal
from runtrack_app.models.group_goal_runs import GroupGoalRuns, GroupGoalRunsWeekly
from runtrack_app.models.runs import Runs

main = Blueprint("main_routes", __name__)


def readable_date(input_date):
    """helper method to make a date object more readable

    :param input_date: a date object
    :return: more readable string representation of a date
    """
    return "{} {}, {}".format(month_name[input_date.month], str(input_date.day), str(input_date.year))


@main.route("/")
@main.route("/index")
@login_required
def index():
    """index page for the main_routes section of the app."""
    user = current_user
    today = date.today()
    new_runs = Runs(user.runs)

    # Get last week main_routes distances
    week_ago = today - timedelta(days=6)
    daily_runs = new_runs.daily_distances_between(week_ago, today)

    # Get last 7 weekdays
    days = []
    for day_int in range(today.weekday()-6, today.weekday()+1):
        day = day_int % 7
        days.append(day_abbr[day])

    # Get alltime distances
    alltime_ggr = GroupGoalRuns(user.goals, user.runs).weekly(dummy=True, at_least=4)
    alltime_runs = GroupGoalRunsWeekly.weekly_distances(alltime_ggr)

    # Get alltime weekdays
    alltime_weeks = list(map(lambda wggr: wggr.name(), alltime_ggr))

    # Get weekly data
    weekly_runs = alltime_runs[-4:]
    weeks = alltime_weeks[-4:]

    return render_template("main_routes/index.html", days=days, daily_runs=daily_runs, weeks=weeks,
                           weekly_runs=weekly_runs, alltime_weeks=alltime_weeks, alltime_runs=alltime_runs)


@main.route("/add_goal", methods=["GET", "POST"])
@login_required
def add_goal():
    """Add a goal to the backend database."""
    user = current_user
    form = AddGoalForm()

    if form.validate_on_submit():
        goal_check = Goal.query.filter_by(user_id=user.id, date=form.date.data).first()
        if not goal_check:
            goal = Goal(distance=form.distance.data, user_id = user.id, date=form.date.data)
            db.session.add(goal)
            db.session.commit()
            flash('Your goal has been added!')
        else:
            goal_check.distance = form.distance.data
            db.session.add(goal_check)
            db.session.commit()
            flash('Your goal has been updated!')

        return redirect('main_routes')
    return render_template("main_routes/add_goal.html", form=form)


@main.route("/add_run", methods=["GET", "POST"])
@login_required
def add_run():
    """Add a run to the backend database."""
    user = current_user
    form = AddRunForm()

    if form.validate_on_submit():
        run = Run(distance=form.distance.data, date=form.date.data, user_id=user.id)
        db.session.add(run)
        db.session.commit()

        flash('Your run has been added!')
        return redirect('main_routes')
    return render_template("main_routes/add_run.html", form=form)


@main.route("/main_routes")
@login_required
def runs():
    """Route that displays a users running data"""
    user = current_user

    grouped_goalruns = GroupGoalRuns(goals=user.goals, runs=user.runs)
    weeks = grouped_goalruns.weekly()[::-1]

    # weekdays = list(map(lambda i: day_abbr[i], range(7)))

    return render_template("main_routes/runs.html", weeks=weeks, float=float, len=len, readable_date=readable_date)
