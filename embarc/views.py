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
from .models import db, Journey, Reflection, login_manager, User, Feedback
from .events import socketio
from .forms import AddJourneyForm, AddReflectionForm, LoginForm, CreateUserForm, AddFeedbackForm

from flask import render_template, redirect, url_for, session, request, g, flash
from werkzeug.utils import secure_filename

from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
def index():
    journeys = Journey.query.all()
    return render_template('index.html', journeys=journeys, user=current_user)


@app.route('/admin_feedback/')
def show_admin_feedback():
    feedback = Feedback.query.all()
    context = {
        'feed_list' : []
    }
    for feed in feedback:
        context['feed_list'].append(feed)
    return render_template('admin_feedback.html', user=current_user, **context)


@app.route('/journey/<journey_slug>/feedback/', methods=['GET', 'POST'])
def show_feedback(journey_slug):
    context = {
        "journeyid" : journey_slug
        # "journeyname": Journey.query.filter_by(id=journey_slug).first().name
    }
    add_feedback_form = AddFeedbackForm()
    if add_feedback_form.validate_on_submit():
        rating = int(add_feedback_form.rating.data)
        q1 = add_feedback_form.q1.data
        q2 = add_feedback_form.q2.data
        q3 = add_feedback_form.q3.data
        q4 = add_feedback_form.q4.data
        q5 = add_feedback_form.q5.data
        q6 = add_feedback_form.q6.data

        feedback = Feedback(name=session['username'], journeyid=journey_slug, rating=rating, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6)
        db.session.add(feedback)
        db.session.commit()
        print(Feedback.query.all())
    return render_template('feedback.html', form=add_feedback_form, user=current_user, **context)


@app.route('/profile/', methods=['GET', 'POST'])
def show_user():
    context = {
        "user" : session['username'],
        "reflections" : Reflection.query.filter_by(name=current_user.username)
    }
    return render_template('user.html', **context)


@app.route('/journey/<journey_slug>/', methods=['GET', 'POST'])
def show_journey(journey_slug):
    context = {
        "journey_id": journey_slug,
        "journey_name" : Journey.query.filter_by(id=journey_slug).first().name,
        "journey_description": Journey.query.filter_by(id=journey_slug).first().description,
        "journey_img_name" : Journey.query.filter_by(id=journey_slug).first().picture,
        "reflections" : Reflection.query.filter_by(journeyid=journey_slug)
    }
    add_reflection_form = AddReflectionForm()
    if add_reflection_form.validate_on_submit():
        reflection_name = current_user.username
        reflection_description = add_reflection_form.description.data
        reflection_picture = add_reflection_form.picture.data
        reflection_picture_filename = secure_filename(reflection_picture.filename)
        reflection_picture.save(os.path.join(app.root_path, 'static/cdn/{}'.format(reflection_picture_filename)))
        print('Picture: {}'.format(reflection_picture))
        reflection_picture_filename = secure_filename(reflection_picture.filename)
        reflection_picture.save(os.path.join(app.root_path, 'static/cdn/{}'.format(reflection_picture_filename)))
        reflection = Reflection(name=reflection_name, description=reflection_description, journeyid=journey_slug,
                                journeyname=context["journey_name"], picture=reflection_picture_filename)
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
    # returns the user home if user is already logged in
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        # searches the database for the username
        user = User.query.filter_by(username=username).first()

        # if the username does not exist in the database, give warning
        if not user:
            flash('User does not exist.', 'danger')
            return render_template('login.html', form=form, user=current_user)

        # if the input password does not match the one on record in db, deny access
        if user.password != password:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('login.html', form=form, user=current_user)


        session['username'] = username

        login_user(user)

        flash('You have successfully logged in.', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', form=form, user=current_user)


@app.route('/logout/')
def logout():
    logout_user()
    session.clear()
    flash('You have successfully logged out.', 'success')
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

        # if user doesn't already exist, create new user and login
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
        else:
            flash('Username already exists.', 'danger')

    return render_template('create_user.html', form=form, user=current_user)
