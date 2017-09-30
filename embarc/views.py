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
from .forms import MusicSubmitForm

from flask import render_template, redirect, url_for


@app.route('/')
def index():
    print('sup')
    return render_template('index.html')
