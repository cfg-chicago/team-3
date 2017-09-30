from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .app import db

class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(3000), unique=False, nullable=False)
    picture = db.Column(db.String(200), unique=False, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# class Reflection(db.Model):

