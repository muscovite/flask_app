import os
from flask import Flask
from flask_app import routes
from flask_app import db

# Entry point for Flask apps. Mostly contains some boilerplate code needed to
# get the app up and running
def create_app():
    # Create the app
    app = Flask(__name__)

    # If you want to use sessions, you need to set a secret key
    # This app uses session variables to pass around form validation messages
    app.secret_key = "super secure key"

    # Register routes with your app
    app.register_blueprint(routes.routes)

    # Load the database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./my_db.db"
    db.init_db(app)

    return app
