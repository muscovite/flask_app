from flask import Blueprint, render_template

routes = Blueprint('routes', __name__,)

@routes.route("/")
def index():
    return "Hello World!"

@routes.route("/greet/")
@routes.route("/greet/<name>/")
def greet(name=None):
    return render_template("greet.html", name=name)

@routes.route("/count/<int:number>/")
def count(number):
    return "num %d" % number
