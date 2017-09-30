#!venv/bin/python

from embarc.models import db

import os

myfile = './embarc/test.db'
if os.path.isfile(myfile):
    os.remove()

db.create_all()
