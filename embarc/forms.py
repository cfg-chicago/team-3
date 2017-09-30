from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class AddJourneyForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    picture = FileField('Picture', validators=[FileRequired()])


class AddReflectionForm(Form):
    description = StringField('description', validators=[DataRequired()])

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
