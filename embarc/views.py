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
from .events import socketio
from .forms import AddJourneyForm

from flask import render_template, redirect, url_for


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-journey')
def add_journey():
    add_journey_form = AddJourneyForm()
    return render_template('add_journey.html', form=add_journey_form)
