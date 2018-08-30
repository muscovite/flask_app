# ExtraHop HackRice 2018 workshop app

This is a basic web app that manages students and grades for a single class.

## Setup
Make sure you have Python and [pip](https://pip.pypa.io/en/stable/installing/) installed. Note that this app was built on Python 2.7, so some of the steps here may vary if you're using a different version.

### Linux
Installing dependencies
- Flask: `pip install flask`    
- WTForms: `pip install wtforms` 

Managing the app
- Navigate to the folder that contains `main.py`
- Set environment variables for current shell session: `export FLASK_APP=main.py FLASK_DEBUG=1`
  - Alternatively, you can also prefix `FLASK_APP=main.py FLASK_DEBUG=1` to the following commands
- Initialize database: `flask init-db`
  - Run this command to update your database after making changes to `schema.sql`. This clears data stored in the existing database.
- Run app: `flask init-db`

Configurable options
- Run Flask app on a different port: `flask run --port 1234` (default is 5000)

### OSX
todo

### App structure
- `main.py`: Flask entry point to the app. Performs some setup actions.
- `routes.py`: Contains all the routes/endpoints used in the app
- `db.py`: Contains methods for setting up and interacting with the database
- `forms.py`: Defines the WTForms used in the app
- `schema.sql`: Defines the database schema
- `templates`: Jinja2 webpage templates
  -  `base.html`: Provides macros and basic structure common to all pages
  -  `index.html`: Template for the main overview page
  -  `student.html`: Template for student page
- `static`: By convention, stores JS files, images and CSS files
  - `style.css`: CSS for the web app 
- `instance`: The database lives here 

## Documentation
- [Flask](http://flask.pocoo.org/docs/1.0/)
- [WTForms](https://wtforms.readthedocs.io/en/stable/)
- [sqlite3](https://docs.python.org/2.7/library/sqlite3.html)/ [SQLite](https://www.sqlite.org/docs.html) 
- [Jinja2](http://jinja.pocoo.org/docs/2.10/)
