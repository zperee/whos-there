import datetime

from flask import Flask, render_template, request, redirect, url_for, session

from libs import week_handler, person_handler, date_helper, auth_handler
from functools import wraps

app = Flask("Who's there")
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"

# Here is a custom decorator that verifies the JWT is present in
# the request, as well as insuring that this user has a role of
# `admin` in the access token
def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if not auth_handler.is_authenticated():
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return decorated_view

@app.route("/")
@app.route("/index")
def index():
    return redirect("/week/show")

@app.route("/week/editor/")
@app.route("/week/editor/<year>/<week_number>", methods=['GET', 'POST'])
def edit_week(year=None, week_number=None):
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
    valid_url_input = date_helper.validate_week_input(year, week_number)
    if not valid_url_input: # If the input is not valid redirect to current week
        return redirect_if_not_valid('/week/show/')
    
    week_data = week_handler.load_week(year, week_number)
    return render_template("show_week.html", week=week_data)

@app.route("/vote")
@app.route("/vote/<year>/<week_number>")
@login_required
def vote(year=None, week_number=None):
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
    person_handler.vote(True, date, person)
    return redirect(request.referrer)

@app.route("/vote/no/<date>/<person>")
@login_required
def vote_no(date, person):
    person_handler.vote(False, date, person)
    return redirect(request.referrer)

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    auth_handler.logout()
    return redirect(url_for('index'))

@app.route('/user/manage')
@login_required
def manage_user():
    users = auth_handler.load_all_user()
    return render_template("manage_user.html", all_user = users)

def redirect_if_not_valid(page):
    year = str(date_helper.get_current_year())
    week_number = str(date_helper.get_current_week_number())
    url = '%s%s%s%s' % (page, year, '/', week_number)
    return redirect(url)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
