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
    app.secret_key = 'super secure key'
    db.init_app(app)

    # Register routes with your app
    app.register_blueprint(routes.routes)

    # Tell app where the database instance should live
    app.instance_path = './instance'
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
