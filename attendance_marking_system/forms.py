from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from attendance_marking_system import cursor

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[ DataRequired(message="Please enter your name") ])
    designation = StringField('Designation', validators=[ DataRequired(message="Please enter your designation") ])
    email = StringField('Email', validators=[ DataRequired(message="Please enter your email"), Email(message="Please enter a valid email") ])
    password = PasswordField('Password', validators=[ DataRequired(message="Please enter the password"), Length(min=8, max=20, message="Password should have atleast 8 characters")])
    cnf_password = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password', message="Passwords do not match")])
    submit = SubmitField('Register')

    def validate_email(self, email):
        cursor.execute("SELECT * FROM tbl_faculty WHERE email='{}'".format(email.data))
        data = cursor.fetchall()
        if len(data) > 0:
            raise ValidationError('Email already exists. Please enter a new email')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(message="Please enter your email"), Email(message="Please enter a valid email") ])
    password = PasswordField('Password', validators=[ DataRequired(message="Please enter the password")])
    submit = SubmitField('Sign In')

class AttendanceForm(FlaskForm):
    lecture_number = SelectField('Lecture Number', description='Lecture Number', choices=[('', 'Lecture Number'), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8) ], coerce=str)
    class_name = SelectField('Lecture Name', description='Lecture Name', choices=[], coerce=str)
    date = DateField('Date', validators=[ DataRequired() ])
    image = FileField('Select an Image', validators=[ FileRequired(message='Please select a valid image') ])
    submit = SubmitField('Submit')

class StudentForm(FlaskForm):
    enrollment = StringField('Enrollment number', validators=[ DataRequired(message="Please enter your student enrollment number") ])
    name = StringField('Name', validators=[ DataRequired(message="Please enter student name") ])
    class_name = SelectField('Lecture Name', description='Lecture Name', choices=[], coerce=str)
    image = FileField('Select an Image', validators=[ FileRequired(message='Please select a valid image') ])
    submit = SubmitField('Add Student')