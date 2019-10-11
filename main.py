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


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/week/add/", methods=['GET', 'POST'])
@app.route("/week/editor/", methods=['GET', 'POST'])
@app.route("/week/editor/<year>/<week_number>", methods=['GET', 'POST'])
def add_week(year=None, week_number=None):
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

    return render_template("add_week.html", week=week_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


'''
if(data_helper.file_exists(file_path) and (request.path == "/week/add/" or request.path == "/week/editor/")):
            url = '%s%s%s%s' % ('/week/editor/', year, '/', week_number)
        return redirect(url)
        '''