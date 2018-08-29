#
# Contains all the routes and route handlers for the app
#

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_app import db
from flask_app.forms import AddStudentForm, AddAssignmentForm, ViewStudentForm
from flask_app.util import date_to_unix

# Groups your routes into a blueprint so the app can register them from
# another file. You can use multiple blueprints to keep your routes organized.
# http://flask.pocoo.org/docs/1.0/tutorial/views/
routes = Blueprint("routes", __name__)

# Since we're storing form validation information in session variables, we
# need to clear their state before returning status about the next form
# submission
def reset_session():
    session["error"] = None
    session["success"] = None


# The main page. You can add new assignments, students and grades from here.
@routes.route("/")
def index():
    add_assignment_form = AddAssignmentForm()
    add_student_form = AddStudentForm()
    view_student_form = ViewStudentForm()

    students = db.get_students()
    assignments = db.get_assignments()
    view_student_form.students.choices = students

    error = session.get("error", {})
    success = session.get('success', {})
    reset_session()

    return render_template(
        "index.html",
        view_student_form=view_student_form,
        add_student_form=add_student_form,
        add_assignment_form=add_assignment_form,
        assignments=assignments,
        students=students,
        success=success,
        error=error
    )


# Add a new assignment
@routes.route("/assignment/add", methods=["POST"])
def add_assignment():
    assignment_form = AddAssignmentForm(request.form)

    if not assignment_form.validate():
        session["error"] = {"add_assignment": assignment_form.errors}
        return redirect(url_for("routes.index"))

    weight = float(assignment_form.weight.data)
    db.add_assignment(assignment_form.title.data, weight, assignment_form.due_date.data)
    session["success"] = {"add_assignment": "Added a new assignment!"}
    return redirect(url_for("routes.index"))


# Display summary of all assignments for this class
@routes.route("/assignment/all")
def assignments_all():
    return "all assignments"


# Display summary of all students and their current class averages
@routes.route("/student/all/")
def students_all():
    return "all grades"


# Add a new student
@routes.route("/student/add/", methods=["POST"])
def add_student():
    student_form = AddStudentForm(request.form)

    if not student_form.validate():
        print "student form error"
        session["error"] = {"add_student": student_form.errors}
        return redirect(url_for("routes.index"))

    db.add_student(student_form.name.data)
    session["success"] = {"add_student": "Added a new student!"}
    return redirect(url_for("routes.index"))



# Display detailed grade information for a single student
@routes.route("/student/", methods=["GET"])
def student():
    id = request.args.get("students", None)

    if not id:
        return "You didn't pick a student"

    student_data = db.get_student(id)
    return "You picked student with id %d" % int(id)

    # return render_template(
    #     "student.html",
    # )
