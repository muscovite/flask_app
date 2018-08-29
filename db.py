#
# Contains methods for querying and setting up the database
#

import sqlite3
import time
from datetime import datetime

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

# Return grade information for a single student
def get_student(student_id):
    db = get_db()
    students = db.execute('SELECT * from student').fetchall()
    return students

# Return all existing students
def get_students():
    db = get_db()
    students = db.execute('SELECT * from student').fetchall()
    return students

# Return all existing assignments
def get_assignments():
    db = get_db()
    assignments = db.execute('SELECT * from assignment').fetchall()
    return assignments

# Add a new assignment
def add_assignment(title, weight, due_date):
    db = get_db()
    query = """INSERT INTO assignment (title, weight, due_date) 
               VALUES (?, ?, ?)"""
    db.execute(query, [title, weight, due_date])
    db.commit()

# Add a new student to the class
def add_student(name):
    db = get_db()
    query = "INSERT INTO student (name) VALUES (?)" 
    db.execute(query, [name])
    db.commit()

# Add a new score for an assignment for a given student, or updates it if
# one already exists
def add_or_update_score(student_id, **kwargs):
    # probably need kwargs or something with assignment info
    pass
