from flask import Flask
from flask import render_template

app = Flask("Who's there")

@app.route("/")
@app.route("/index")
def jinja():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)