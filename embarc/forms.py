from flask_wtf import Form
from wtforms import StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class AddJourneyForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])


class AddReflectionForm(Form):
    name = StringField('name', validators=[DataRequired()])
    journey = StringField('journey', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
