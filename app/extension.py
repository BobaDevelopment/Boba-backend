import redis
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db = SQLAlchemy()
r = redis.Redis()
socketio = SocketIO()