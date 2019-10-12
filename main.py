import datetime

import os
from pathlib import Path

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from libs import week_date_helper
from libs import week_data_handler
from libs import data_helper

app = Flask("Who's there")

app_main_path = Path(os.path.abspath(
    "/".join(os.path.realpath(__file__).split("/")[:-1])))
data_path = Path(os.path.abspath(app_main_path/'../week/'))

week_days = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

@app.route("/")
@app.route("/index")
def index():
    return redirect("/week/show")

@app.route("/week/add/")
@app.route("/week/add/<future>")
def add_week(future=None):
    week_number = int(week_date_helper.get_current_week_number())
    year = int(week_date_helper.get_current_year())
    if (future and future.isdigit()):
        week_number += int(future)
        if (week_number > 52):
            week_number -= 52
            year += 1
    url = '%s%s%s%s' % ('/week/editor/', str(year), '/', str(week_number))
    return redirect(url)


@app.route("/week/editor/", methods=['GET', 'POST'])
@app.route("/week/editor/<year>/<week_number>", methods=['GET', 'POST'])
def edit_week(year=None, week_number=None):
    valid_url_input = week_date_helper.validate_week_input(year, week_number)
    
    if(not valid_url_input):
        year = str(week_date_helper.get_current_year())
        week_number = str(week_date_helper.get_current_week_number())
        url = '%s%s%s%s' % ('/week/editor/', year, '/', week_number)
        return redirect(url)
    
    if request.method == 'POST':
        week_data = week_data_handler.update_week(data_path, request.form, year, week_number)
    else:    
        week_data = week_data_handler.load_week(data_path, year, week_number)

    week_data = add_days_name_to_date(week_data)
    return render_template("add_week.html", week=week_data)

@app.route("/week/show/")
@app.route("/week/show/<year>/<week_number>")
def show_week(year=None, week_number=None):
    valid_url_input = week_date_helper.validate_week_input(year, week_number)

    if(not valid_url_input):
        year = str(week_date_helper.get_current_year())
        week_number = str(week_date_helper.get_current_week_number())
        url = '%s%s%s%s' % ('/week/show/', year, '/', week_number)
        return redirect(url)
    
    file_name = week_data_handler.get_file_name(data_path, year, week_number)
    week_data = {}
    
    if(data_helper.file_exists(file_name)):
        week_data = week_data_handler.load_week(data_path, year, week_number)

    week_data = add_days_name_to_date(week_data)
    return render_template("show_week.html", week=week_data)

@app.route("/vote/")
@app.route("/vote/<person>")
def vote(person=None):
    return person

def add_days_name_to_date(week_data):
    counter = 0
    if (week_data.get('days')):
        for day in week_data['days']:
            day['day_name'] = week_days[counter]
            counter += 1
    return week_data

if __name__ == "__main__":
    app.run(debug=True, port=5000)