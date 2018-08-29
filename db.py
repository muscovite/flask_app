import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# Bunch of boilerplate copied from Flask tutorials
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# Database interaction

# Return assignment information for a single student
def get_student(student_id):
    pass

# Return assignment information for all students
def get_students():
    pass

# Add a new student to the class
def create_student(name):
    pass

# Add a new assignment for a given student
def add_assignment(student_id, **kwargs):
    # probably need kwargs or something with assignment info
    pass

# Add a new assignment for a given student, or update an existing assignment
# if the given assignment_name already exists in the database
def update_assignment(student_id, assignment_name)
    # assignments are keyed by string
    pass

# Remove an assignment from a given student
def remove_assignment(student_id, assignment_name)
    # assignments are keyed by string
    pass

