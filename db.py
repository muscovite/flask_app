#
# Contains methods for querying and setting up the database
#

import sqlite3
import time
from datetime import datetime

import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#
# Database models
#
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True, nullable=False)
    grades = db.relationship("Grade", backref="student", lazy=True)


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), unique=True, nullable=False)
    weight = db.Column(db.Float(), nullable=False)
    due_date = db.Column(db.Date(), nullable=False)
    grades = db.relationship("Grade", backref="assignment", lazy=True)


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float(), nullable=False)
    submit_date = db.Column(db.Date(), nullable=False)
    student_id = db.Column(
        db.Integer, db.ForeignKey("student.id"), nullable=False
    )
    assignment_id = db.Column(
        db.Integer, db.ForeignKey("assignment.id"), nullable=False
    )


#
# Database initialization
#


def init_db(app):
    # Flask lets you create a test context to initialize an app
    with app.test_request_context():
        db.init_app(app)
        db.create_all()


#
# Database interaction
#

# Return a single student
# SQL: SELECT * FROM student where id = <id>
def get_student(id):
    return Student.query.filter_by(id=id).first()


# Return all existing students
# SQL: SELECT * FROM student
def get_students():
    return Student.query.all()


# Add a new student to the class
# SQL: INSERT INTO student (name) VALUES (<name>)
def add_student(name):
    student = Student(name=name)
    db.session.add(student)
    db.session.commit()


# Return all existing assignments
# SQL: SELECT * FROM assignment
def get_assignments():
    return Assignment.query.all()


# Add a new assignment
# SQL: INSERT INTO assignment (title, weight, due_date)
#      VALUES (<title>, <weight>, <due_date>)
def add_assignment(title, weight, due_date):
    assignment = Assignment(title=title, weight=weight, due_date=due_date)
    db.session.add(assignment)
    db.session.commit()


# Return all grades for a given student
# SQL: SELECT score, submit_date, title, weight FROM grade
#      JOIN assignment ON assignment.id = grade.assignment_id
#      WHERE grade.student_id = <student_id>
def get_student_grades(student_id):
    return Student.query.filter_by(id=student_id).first().grades


# Add a new score for an assignment for a given student
# SQL: INSERT INTO grade (score, submit_date, student_id, assignment_id)
#      VALUES (<score>, <submit_date>, <student_id>, <assignment_id>)
def add_grade(score, submit_date, student_id, assignment_id):
    grade = Grade(
        score=score,
        submit_date=submit_date,
        student_id=student_id,
        assignment_id=assignment_id,
    )
    db.session.add(grade)
    db.session.commit()
