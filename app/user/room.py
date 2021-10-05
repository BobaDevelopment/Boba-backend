from app.user import user
from flask import request, jsonify
from app.model.dbmodel import *
from app.utils.jwt import getToken
from app.model.response import *
from app import r
# joinroom and leaveroom
# emit user to drop


# 创建房间
@user.route("/createroom")
def userCreateRoom():
    data = request.json
    roomName = data.get("roomname")
    roomUserNum = data.get("roomusername")
    room = Room(roomName=roomName, roomUserNum=roomUserNum)
    db.session.add(room)
    db.session.commit()
    prizelist = data["prizelist"]
    for prize in prizelist:
        name = prize["name"]
        picurl = prize["url"]
        level = prize["level"]
        count = prize["count"]
        prize = Prize(roomId=room.id, name=name, picture=picurl, level=level, count=count)
        db.session.add(prize)
    db.session.commit()
    from datetime import datetime
    t = datetime.now()
    inviteCode = str(int("%02d%02d%02d" % (t.hour+5, t.minute+4, t.second+3)))
    r.set(inviteCode, str(room.id))
    return jsonify(OK(
        invitecode = inviteCode
    ))


# 删除房间
@user.route("/deleteroom")
def userDeleteRoom():
    pass