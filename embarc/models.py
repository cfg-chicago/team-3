from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .app import db

class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
