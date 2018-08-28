import os
from flask import Flask
from routes import routes
from . import db

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(routes)
    app.instance_path = './instance'
    db.init_app(app)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

# Install
# pip install flask

# Running app
# FLASK_APP=main.py FLASK_DEBUG=1 flask run

# Init the db
# FLASK_APP=main.py FLASK_DEBUG=1 flask init-db

# Other params
# --port 1234 (default: 5000)
# --host=0.0.0.0
