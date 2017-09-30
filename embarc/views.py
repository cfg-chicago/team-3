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
from .models import db, Journey, Reflection
from .events import socketio
from .forms import AddJourneyForm, AddReflectionForm

from flask import render_template, redirect, url_for, session, request
from werkzeug.utils import secure_filename


@app.route('/')
def index():
    journeys = Journey.query.all()
    print(journeys)
    return render_template('index.html', journeys=journeys)


@app.route('/add-journey', methods=['GET', 'POST'])
def add_journey():
    add_journey_form = AddJourneyForm()
    if add_journey_form.validate_on_submit():
        return redirect(url_for('index'))
        journey_name = add_journey_form.name.data
        journey_description = add_journey_form.description.data
        #journey_picture = add_journey_form.picture.data
        #filename = secure_filename(journey_picture.filename)
        #f.save(os.path.join(app.instance_path, 'static/cdn/{}'.format(filename)))
        journey = Journey(name=journey_name, description=journey_description)#, picture=filename)
        print("Name: {}, Description: {}".format(journey_name, journey_description))

        db.session.add(journey)
        db.session.commit()
        journeys = Journey.query.all()
        return redirect(url_for('index'))
    return render_template('add_journey.html', form=add_journey_form)


@app.route('/add-reflection', methods=['GET', 'POST'])
def add_reflection():
    add_reflection_form = AddReflectionForm()
    if add_reflection_form.validate_on_submit():
        reflection_name = add_reflection_form.name.data
        reflection_description = add_reflection_form.description.data
        reflection_journey = add_reflection_form.journey.data
        reflection = Reflection(name=reflection_name, description=reflection_description, journey=reflection_journey)
        db.session.add(reflection)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_reflection.html', form=add_reflection_form)
