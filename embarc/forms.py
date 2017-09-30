from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class AddJourneyForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])


class AddReflectionForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])

class LoginForm(Form):
	username = TextField('Username', [DataRequired()])
	password = PasswordField('Password', [DataRequired()])