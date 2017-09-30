import facebook
import re
import httplib2
import os
import datetime
import udatetime
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools as tools
from oauth2client.file import Storage

from .app import app, redis
from .models import db, Journey
from .events import socketio
from .forms import AddJourneyForm, AddReflectionForm

from flask import render_template, redirect, url_for, session, request
from werkzeug.utils import secure_filename


@app.route('/')
def index():
    print(Journey.query.all())
    return render_template('index.html')


@app.route('/add-journey', methods=['GET', 'POST'])
def add_journey():
    add_journey_form = AddJourneyForm()
    if add_journey_form.validate_on_submit():
        journey_name = add_journey_form.name.data
        journey_description = add_journey_form.description.data
        journey_picture = add_journey_form.picture.data
        filename = secure_filename(journey_picture.filename)
        f.save(os.path.join(
            url_for('static', filename='cdn/{}'.format(filename))
        ))
        journey = Journey(name=journey_name, description=journey_description, picture=filename)
        db.session.add(journey)
        db.session.commit()
        journeys = Journey.query.all()
        print(journeys[0])
        return redirect(url_for('index'))
    return render_template('add_journey.html', form=add_journey_form)


@app.route('/add-reflection')
def add_reflection():
    add_reflection_form = AddReflectionForm()
    return render_template('add_reflection.html', form=add_reflection_form)
