from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class AddJourneyForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    picture = FileField(validators=[FileRequired()])


class AddReflectionForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])

class LoginForm(Form):
	username = StringField('Username', [DataRequired()])
	password = PasswordField('Password', [DataRequired()])