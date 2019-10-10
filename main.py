from flask import Flask
from flask import render_template

from libs import week

app = Flask("Who's there")

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/week/add")
def add_week():
    week_data = week.get_week(1)
    return render_template("add_week.html", week=week_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)