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
from .models import db, Journey, Reflection, User
from .events import socketio
from .forms import AddJourneyForm, AddReflectionForm

from flask import render_template, redirect, url_for, session, request
from werkzeug.utils import secure_filename


@app.route('/')
def index():
    journeys = Journey.query.all()
    print(journeys)
    return render_template('index.html', journeys=journeys)


@app.route('/journey/<journey_slug>/')
def show_journey(journey_slug):
    context = {
        "journey_name" : Journey.query.filter_by(id=journey_slug).first().name,
        "journey_description": Journey.query.filter_by(id=journey_slug).first().description,
        "journey_img_name" : Journey.query.filter_by(id=journey_slug).first().picture,
        "reflections" : Reflection.query.filter_by(journeyid=journey_slug)
    }
    return render_template('journey.html', **context)


@app.route('/add-journey/', methods=['GET', 'POST'])
def add_journey():
    add_journey_form = AddJourneyForm()
    if add_journey_form.validate_on_submit():
        journey_name = add_journey_form.name.data
        journey_description = add_journey_form.description.data
        journey_picture = add_journey_form.picture.data
        journey_picture_filename = secure_filename(journey_picture.filename)
        journey_picture.save(os.path.join(app.root_path, 'static/cdn/{}'.format(journey_picture_filename)))
        journey = Journey(name=journey_name, description=journey_description, picture=journey_picture_filename)
        print("Name: {}, Description: {}, Filename: {}".format(journey_name, journey_description, journey_picture_filename))

        db.session.add(journey)
        db.session.commit()
        journeys = Journey.query.all()
        return redirect(url_for('index'))

    
    return render_template('add_journey.html', form=add_journey_form)


@app.route('/add-reflection/', methods=['GET', 'POST'])
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
