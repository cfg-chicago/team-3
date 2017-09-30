from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .app import db, login_manager

class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(3000), unique=False, nullable=False)
    picture = db.Column(db.String(250), unique=False, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Reflection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(3000), unique=False, nullable=False)
    journey = db.Column(db.String(200), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=False, nullable=False)
    user_type = db.Column(db.String(10), unique=False, nullable=False)
    # fb_login = db.Column(db.String(120), unique=False, nullable=False)
    # picture = db.Column(db.String(250), unique=False, nullable=True)

    def __init__(self, username, password, user_type):
        self.username = username
        self.user_type = user_type
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.id)

