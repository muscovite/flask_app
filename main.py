from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/greet/")
@app.route("/greet/<name>/")
def greet(name=None):
    return render_template("greet.html", name=name)

@app.route("/count/<int:number>/")
def count(number):
    return "num %d" % number

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()

# Install
# pip install flask

# Running app
# FLASK_APP=main.py FLASK_DEBUG=1 flask run

# Other params
# --port 1234 (default: 5000)
# --host=0.0.0.0
