from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("main.html")


@app.get("/sites")
def sites_get():
    return "Sites"
