from app.extension import db
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    OpenID = db.Column(db.String(255), unique=True)
    sessionKey = db.Column(db.String(255))
    username = db.Column(db.String(255))
    avatar = db.Column(db.String(255))


class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(db.Integer, primary_key=True)
    roomAdminId = db.Column(db.Integer)
    roomName = db.Column(db.String(255))
    roomUserNum = db.Column(db.Integer)


class Prize(db.Model):
    __tablename__ = "prize"
    id = db.Column(db.Integer, primary_key=True)
    roomId = db.Column(db.Integer)
    level = db.Column(db.Integer)
    name = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    count = db.Column(db.Integer)


class UserRoomRelation(db.Model):
    __tablename__ = "userroomrelation"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    roomId = db.Column(db.Integer)


class UserPrizeRelation(db.Model):
    __tablename__ = "userprizerelation"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    prizeId = db.Column(db.Integer)
    roomId = db.Column(db.Integer)


# 用户在房间的排名
class UserRank(db.Model):
    __tablename__ = "userrank"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    roomId = db.Column(db.Integer)
    level = db.Column(db.Integer)