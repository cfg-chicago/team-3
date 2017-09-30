from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, IntegerField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class AddJourneyForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    picture = FileField('Picture', validators=[FileRequired()])


class AddReflectionForm(Form):
    description = StringField('description', validators=[DataRequired()])

class AddFeedbackForm(Form):
    rating = IntegerField('rating')#, validators=[DataRequired()])
    q1 = StringField('q1')#, validators=[DataRequired()])
    q2 = StringField('q2')#, validators=[DataRequired()])
    q3 = StringField('q3')#, validators=[DataRequired()])
    q4 = StringField('q4')#, validators=[DataRequired()])
    q5 = StringField('q5')#, validators=[DataRequired()])
    q6 = StringField('q6')#, validators=[DataRequired()])
    q7 = StringField('q7')#, validators=[DataRequired()])

class LoginForm(Form):
	username = StringField('Username', [DataRequired()])
	password = PasswordField('Password', [DataRequired()])

class CreateUserForm(Form):
	username = StringField('Username*', [DataRequired()])
	first_name = StringField('First name*', [DataRequired()])
	last_name = StringField('Last name*', [DataRequired()])
	email = StringField('Email*', [DataRequired()])
	group = StringField('Group*', [DataRequired()])
	password = PasswordField('Password*', [DataRequired()])
	teacher_access_code = PasswordField('Teacher access code')
