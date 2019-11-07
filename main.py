import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from libs import week_handler
from libs import person_handler
from libs import date_helper

app = Flask("Who's there")

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

@app.route("/vote/<person>")
@app.route("/vote/<person>/<year>/<week_number>")
def vote(year=None, week_number=None, person=None):
    valid_url_input = date_helper.validate_week_input(year, week_number)
    if not valid_url_input: # If the input is not valid redirect to current week
        return redirect_if_not_valid('/vote/' + person + '/')
    
    week_data = week_handler.load_week(year, week_number)
    return render_template("vote.html", week=week_data, name=person.capitalize())

@app.route("/vote/yes/<date>/<person>")
def vote_yes(date, person):
    person_handler.vote(True, date, person)
    return redirect(request.referrer)

@app.route("/vote/no/<date>/<person>")
def vote_no(date, person):
    person_handler.vote(False, date, person)
    return redirect(request.referrer)

def redirect_if_not_valid(page):
    year = str(date_helper.get_current_year())
    week_number = str(date_helper.get_current_week_number())
    url = '%s%s%s%s' % (page, year, '/', week_number)
    return redirect(url)

if __name__ == "__main__":
    app.run(debug=True, port=5000)