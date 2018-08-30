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

# Return a single student
def get_student(id):
    db = get_db()
    student = db.execute('SELECT * FROM student WHERE id = ?', [id]).fetchall()
    return student[0]

# Return all existing students
def get_students():
    db = get_db()
    students = db.execute('SELECT * FROM student').fetchall()
    return students

# Add a new student to the class
def add_student(name):
    db = get_db()
    query = "INSERT INTO student (name) VALUES (?)"
    db.execute(query, [name])
    db.commit()

# Return all existing assignments
def get_assignments():
    db = get_db()
    assignments = db.execute('SELECT * FROM assignment').fetchall()
    return assignments

# Return all existing assignments to use as choices for adding grades
def get_assignments_choices():
    db = get_db()
    assignments = db.execute('SELECT id, title FROM assignment').fetchall()
    return assignments

# Add a new assignment
def add_assignment(title, weight, due_date):
    db = get_db()
    query = """INSERT INTO assignment (title, weight, due_date)
               VALUES (?, ?, ?)"""
    db.execute(query, [title, weight, due_date])
    db.commit()

# Return all grades for a given student
def get_student_grades(student_id):
    db = get_db()
    query = """SELECT score, submit_date, title, weight FROM grade
               JOIN assignment ON assignment.id = grade.assignment_id
               WHERE grade.student_id = ?"""
    grades = db.execute(query, [student_id]).fetchall()
    return grades

# Add a new score for an assignment for a given student, or update it if
# one already exists
# Note that there's probably a more complex single query that can handle
# both existence checking and then update/insert in one go.
# See if you can figure it out (:
def add_grade(score, submit_date, student_id, assignment_id):
    db = get_db()

    # Check if a grade entry already exists for this student and assignment
    # combination
    query = "SELECT * FROM grade WHERE student_id = ? AND assignment_id = ?"
    exists = db.execute(query, [student_id, assignment_id]).fetchone()

    if exists:
        query = """UPDATE grade SET score = ?, submit_date = ?
                   WHERE student_id = ? AND assignment_id = ?"""
    else:
        query = """INSERT INTO grade
                        (score, submit_date, student_id, assignment_id)
                   VALUES (?, ?, ?, ?)"""

    db.execute(query, [score, submit_date, student_id, assignment_id])
    db.commit()

