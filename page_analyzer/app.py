from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
@app.get("/sites")
def sites_get():
    return "Sites"
