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
from .models import db, Journey, Reflection, login_manager, User
from .events import socketio
from .forms import AddJourneyForm, AddReflectionForm, LoginForm, CreateUserForm

from flask import render_template, redirect, url_for, session, request, g, flash
from werkzeug.utils import secure_filename

from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
def index():
    journeys = Journey.query.all()
    return render_template('index.html', journeys=journeys, user=current_user)


@app.route('/profile/', methods=['GET', 'POST'])
def show_user():
    context = {
        "user" : session['username'],
        "reflections" : Reflection.query.filter_by(name=session['username'])
    }
    return render_template('user.html', **context, user=current_user)


@app.route('/journey/<journey_slug>/', methods=['GET', 'POST'])
def show_journey(journey_slug):
    context = {
        "journey_name" : Journey.query.filter_by(id=journey_slug).first().name,
        "journey_description": Journey.query.filter_by(id=journey_slug).first().description,
        "journey_img_name" : Journey.query.filter_by(id=journey_slug).first().picture,
        "reflections" : Reflection.query.filter_by(journeyid=journey_slug)
    }
    add_reflection_form = AddReflectionForm()
    if add_reflection_form.validate_on_submit():
        reflection_name = session['username']
        reflection_description = add_reflection_form.description.data
        reflection = Reflection(name=reflection_name, description=reflection_description, journeyid=journey_slug,
                                journeyname=context["journey_name"])
        db.session.add(reflection)
        db.session.commit()
        return redirect(url_for('show_journey', journey_slug=journey_slug))
    return render_template('journey.html', form=add_reflection_form, user=current_user, **context)


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
        db.session.add(journey)
        db.session.commit()
        journeys = Journey.query.all()
        return redirect(url_for('index'))

    return render_template('add_journey.html', form=add_journey_form, user=current_user)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def get_current_user():
    g.user = current_user

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('User does not exist.', 'danger')
            return render_template('login.html', form=form, user=current_user)

        if user.password != password:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('login.html', form=form, user=current_user)


        session['username'] = username

        login_user(user)

        flash('You have successfully logged in.', 'success')
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form, user=current_user)


@app.route('/logout/')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

@app.route('/create_user/', methods=['GET', 'POST'])
def create_user():
    form = CreateUserForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        session['username'] = username
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        group = request.form.get('group')
        password = request.form.get('password')
        teacher_access_code = request.form.get('teacher_access_code')

        user = User.query.filter_by(username=username).first()

        # if user doesn't already exist
        if not user:
            if teacher_access_code == 'teacher':
                user_type = 'ADMIN'
            else:
                user_type = 'STUDENT'
            user = User(username, first_name, last_name, email,
                group, password, user_type)
            session['username'] = username
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash('You have successfully registered.', 'success')
        return redirect(url_for('index'))

    return render_template('create_user.html', form=form)
