""" 
Summary: 
    Main python file to run the webapp.
Args:
    app: defines the name of the web app
    app.config["SECRET_KEY"]: Secret for the session
"""
# import modules
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from libs import week_handler, person_handler, date_helper, auth_handler
from functools import wraps

#global varibales
app = Flask("Who's there")
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"

def login_required(fn):
    """
    Summary: 
        Checks if for the path a user is requesting a 
        login is required. So define that a methode is protected
        add the "@login_required" tag.
    Args:
        Function: The function which is protected.
    Returns:
        If a user is authenticated, the requested side. Otherwise
        it redirects to the login page.
    """
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if not auth_handler.is_authenticated():
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return decorated_view

@app.route("/")
@app.route("/index")
def index():
    """
    Summary: 
        Start page of the tool. 
    Returns:
        Redirects to the overview page.
    """
    return redirect("/week/show")

@app.route("/week/editor/")
@app.route("/week/editor/<year>/<week_number>", methods=['GET', 'POST'])
def edit_week(year=None, week_number=None):
    """
    Summary: 
        Allows to create or edit a week
    Args:
        String: Year of the week
        String: Week number of the week
    Returns:
        Week editor with loaded week data
    """
    valid_url_input = date_helper.validate_week_input(year, week_number)
    if not valid_url_input: # If the input is not valid redirect to current week
       return redirect_if_not_valid('/week/editor/')

    if request.method == 'POST': 
        week_data = week_handler.update_week(request, year, week_number)
    else:    
        week_data = week_handler.load_week(year, week_number)

    return render_template("add_week.html", week=week_data)

@app.route("/week/add/<future>")
def add_week(future):
    """
    Summary: 
        Calculates the week number for a given amount of weeks
        in the future.
    Args:
        String: Number of weeks in the future from the current week
    Returns:
        Week editor for the week in the future
    """
    week_number = int(date_helper.get_current_week_number())
    year = int(date_helper.get_current_year())
    if (future and future.isdigit()):
        week_number += int(future)
        if (week_number > 52):
            week_number -= 52
            year += 1
    url = '%s%s%s%s' % ('/week/editor/', str(year), '/', str(week_number))
    return redirect(url)

@app.route("/week/show/")
@app.route("/week/show/<year>/<week_number>")
def show_week(year=None, week_number=None):
    """
    Summary: 
        Displays the overview of a week
    Args:
        String: Year of the week
        String: Week number of the week
    Returns:
        Week overview for the week requested week
    """
    valid_url_input = date_helper.validate_week_input(year, week_number)
    if not valid_url_input: # If the input is not valid redirect to current week
        return redirect_if_not_valid('/week/show/')
    
    week_data = week_handler.load_week(year, week_number)
    return render_template("show_week.html", week=week_data)

@app.route("/vote")
@app.route("/vote/<year>/<week_number>")
@login_required
def vote(year=None, week_number=None):
    """
    Summary: 
        Loads a week and gives the user the ability to vote if 
        he or she can attend to the dinner
    Args:
        String: Year of the week
        String: Week number of the week
    Returns:
        The voting page, for a requested week
    """
    user = auth_handler.load_user()
    print(user)
    valid_url_input = date_helper.validate_week_input(year, week_number)
    if not valid_url_input: # If the input is not valid redirect to current week
        return redirect_if_not_valid('/vote/')
    
    week_data = week_handler.load_week(year, week_number)
    return render_template("vote.html", week=week_data, name=user.capitalize())

@app.route("/vote/yes/<date>/<person>")
@login_required
def vote_yes(date, person):
    """
    Summary: 
        Vote attending for a selected meal
    Args:
        String: Date of the dinner
        String: Person username
    Returns:
        The page before the request was sent
    """
    person_handler.vote(True, date, person)
    return redirect(request.referrer)

@app.route("/vote/no/<date>/<person>")
@login_required
def vote_no(date, person):
    """
    Summary: 
        Vote not attending for a selected meal
    Args:
        String: Date of the dinner
        String: Person username
    Returns:
        The page before the request was sent
    """
    person_handler.vote(False, date, person)
    return redirect(request.referrer)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Summary: 
        Loads the login page for the tool
    Returns:
        The login page
    """
    if request.method == 'POST': 
        user_success = auth_handler.login(request)
        if user_success:
            return redirect(url_for("vote", person=auth_handler.load_user()))
        else:
            return render_template("login.html", error=True)
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    """
    Summary: 
        Logs the current user out
    Returns:
        The index site
    """
    auth_handler.logout()
    return redirect(url_for('index'))

@app.route('/user/manage', methods=['GET', 'POST'])
@login_required
def manage_user():
    """
    Summary: 
        Loads the user management site with all users
    Returns:
        The user management site
    """
    if request.method == 'POST': 
        auth_handler.add_user(request)
        
    users = auth_handler.load_all_user()
    return render_template("manage_user.html", all_user = users)

@app.route("/user/manage/delete/<username>")
@login_required
def delete_user(username):
    """
    Summary: 
        Deletes a selected user from the tool
    Args:
        String: Username of the user which want to be deleted
    Returns:
        The page before the request was sent
    """
    auth_handler.delete_user(username)
    return redirect(request.referrer)

@app.route("/user/summary")
def summary():
    """
    Summary: 
        Creates a summary (piechart) of how many times a person attended
        for dinner
    Returns:
        The summary page with the piechart
    """
    pie_chart = person_handler.summary()
    return render_template("summary.html", chart=pie_chart)

def redirect_if_not_valid(page):
    """
    Summary: 
        Redirects to the current week when the user provided
        invalid week parameters.
    Args:
        String: Requested page
    Returns:
        The requested page for the current week
    """
    year = str(date_helper.get_current_year())
    week_number = str(date_helper.get_current_week_number())
    url = '%s%s%s%s' % (page, year, '/', week_number)
    return redirect(url)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
