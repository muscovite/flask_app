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
from flask_app.forms import (
    AddAssignmentForm,
    AddGradeForm,
    AddStudentForm,
    ViewStudentForm,
)

# Groups your routes into a blueprint so the app can register them from
# another file. You can use multiple blueprints to keep your routes organized.
# http://flask.pocoo.org/docs/1.0/tutorial/views/
routes = Blueprint("routes", __name__)

# Since we're storing form validation information in session variables, we
# need to clear their state before returning status about the next form
# submission
def _reset_session():
    session["error"] = None
    session["success"] = None


# Helper function that queries the database and converts the results into a
# format usable by an HTML select field
def _get_assignments_choices():
    results = db.get_assignments()
    return [(r.id, r.title) for r in results]


# The main page. You can add new assignments, students and grades from here.
@routes.route("/", methods=["GET"])
def index():
    add_assignment_form = AddAssignmentForm()
    add_student_form = AddStudentForm()
    view_student_form = ViewStudentForm()

    students = db.get_students()
    assignments = db.get_assignments()

    # Note: there is also a WTForms extension QuerySelectField that converts
    # SQLAlchemy query results into the appropriate Select field format
    student_choices = [(s.id, s.name) for s in students]
    view_student_form.students.choices = student_choices

    error = session.get("error", {})
    success = session.get("success", {})
    _reset_session()

    return render_template(
        "index.html",
        view_student_form=view_student_form,
        add_student_form=add_student_form,
        add_assignment_form=add_assignment_form,
        assignments=assignments,
        students=students,
        success=success,
        error=error,
    )


# Route that handles form submission. Add a new assignment
@routes.route("/assignment/add", methods=["POST"])
def add_assignment():
    assignment_form = AddAssignmentForm(request.form)

    if not assignment_form.validate():
        session["error"] = {"add_assignment": assignment_form.errors}
        return redirect(url_for("routes.index"))

    weight = float(assignment_form.weight.data)
    db.add_assignment(
        assignment_form.title.data, weight, assignment_form.due_date.data
    )
    session["success"] = {"add_assignment": "Added a new assignment!"}
    return redirect(url_for("routes.index"))


# Route that handles form submission. Add a new student
@routes.route("/student/add/", methods=["POST"])
def add_student():
    student_form = AddStudentForm(request.form)

    if not student_form.validate():
        session["error"] = {"add_student": student_form.errors}
        return redirect(url_for("routes.index"))

    db.add_student(student_form.name.data)
    session["success"] = {"add_student": "Added a new student!"}
    return redirect(url_for("routes.index"))


# Helper function to construct direct url for a student's grade page
def url_for_student(id):
    return redirect(url_for("routes.student") + str(id))


# Calculate a student's current class average
def get_class_average(grades_and_weights):
    total_weight = 0
    average = 0

    for grade in grades_and_weights:
        average += grade[0] * grade[1]
        total_weight += grade[1]

    # The total weight of assignments might not add up to 1 yet, ex. we are
    # only partway through the semester, or the student is late on submissions
    # so we need to scale the average appropriately
    return average / total_weight


# Display detailed grade information for a single student
# We handle POST so you can access this page after selecting a student from the
# dropdown on the main page.
# We handle GET so you can also directly link to a student's page, if you know
# their ID.
@routes.route("/student/", methods=["GET", "POST"])
@routes.route("/student/<id>", methods=["GET"])
def student(id=None):
    if request.method == "POST":
        id = request.form["students"]

    if not id:
        return render_template("student.html")

    add_grade_form = AddGradeForm()

    student = db.get_student(id)
    grades = db.get_student_grades(id)
    assignments = _get_assignments_choices()

    grades_and_weights = [
        (grade.score, grade.assignment.weight) for grade in grades
    ]
    average = get_class_average(grades_and_weights) if grades_and_weights else 0

    add_grade_form.assignments.choices = assignments
    add_grade_form.student_id.data = id

    error = session.get("error", {})
    success = session.get("success", {})
    _reset_session()

    return render_template(
        "student.html",
        name=student.name,
        average=average,
        grades=grades,
        assignments=assignments,
        add_grade_form=add_grade_form,
        error=error,
        success=success,
    )


# Route that handles form submission. Add a new grade for a given student
@routes.route("/grade/add/", methods=["POST"])
def add_grade():
    id = request.form["student_id"]
    grade_form = AddGradeForm(request.form)

    # Unfortunately, since the assignments are dynamically generated, you need
    # to provide them to the form before validation so that it knows what to
    # validate against
    assignments = _get_assignments_choices()
    grade_form.assignments.choices = assignments

    if not grade_form.validate():
        session["error"] = {"add_grade": grade_form.errors}
        return url_for_student(id)

    score = float(grade_form.score.data)
    student_id = int(grade_form.student_id.data)

    db.add_grade(
        score,
        grade_form.submit_date.data,
        student_id,
        grade_form.assignments.data,
    )

    session["success"] = {"add_grade": "Added a new grade!"}
    return url_for_student(id)
