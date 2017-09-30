#!venv/bin/python

from embarc.models import db

import os

os.remove('./embarc/test.db')

db.create_all()
