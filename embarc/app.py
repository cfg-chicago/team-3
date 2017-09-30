from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

socketio = SocketIO(app)

db = SQLAlchemy(app)

redis = redis.StrictRedis(host='localhost', port=6379, db=0)
