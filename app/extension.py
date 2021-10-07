import redis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
r = redis.Redis()