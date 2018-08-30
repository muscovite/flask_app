#
# Contains all the forms uses in the app
#

from wtforms import (
    DecimalField,
    Form,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
)
# This DateField requires HTML5 support. Use wtforms.DateField if your brower
# is too outdated - it will stil provide date validation but the browser will
# render it in the form as a simple text input field.
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, NumberRange


class ViewStudentForm(Form):
    students = SelectField("name")
    submit = SubmitField("Submit")  # optional?

class AddStudentForm(Form):
    name = StringField("name", validators=[InputRequired()])
    submit = SubmitField("Submit")  # optional?


class AddAssignmentForm(Form):
    title = StringField("title", validators=[InputRequired()])
    weight = DecimalField("weight", validators=[
        InputRequired(), 
        NumberRange(0, 1, "Assignment weight must be between 0 and 1.")
        ])
    due_date = DateField("due_date", validators=[InputRequired()])
    submit = SubmitField("Submit")


class AddGradeForm(Form):
    score = DecimalField("score", validators=[InputRequired()])
    submit_date = DateField("submit_date", validators=[InputRequired()])
    student_id = HiddenField("student_id", validators=[InputRequired()])
    assignments = SelectField(
        "assignment", validators=[InputRequired()], coerce=int
    )
    submit = SubmitField("Submit")
