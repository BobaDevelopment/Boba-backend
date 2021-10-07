from app.user import user
from flask import request, jsonify
from app.model.dbmodel import *
from app.utils.jwt import getToken, getUserId
from app.model.response import *
from app import r
# joinroom and leaveroom
# emit user to drop


# 创建房间
@user.route("/createroom", methods=["POST"])
def userCreateRoom():
    user = User.query.get(getUserId())

    data = request.json
    print(data)
    roomName = data.get("roomname")
    roomUserNum = data.get("roomusernum")
    room = Room(roomName=roomName, roomUserNum=roomUserNum, roomAdminId=user.id)
    db.session.add(room)
    db.session.commit()
    prizelist = data.get("prizeList")
    for prize in prizelist:
        for i in prize["awardList"]:
            name = i["awardName"]
            picurl = i["avatarUrl"]
            level = i["level"]
            count = i["awardNum"]
            prize = Prize(roomId=room.id, name=name, picture=picurl, level=level, count=count)
            db.session.add(prize)
    db.session.commit()
    from datetime import datetime
    t = datetime.now()
    inviteCode = str(int("%02d%02d%02d" % (t.hour+5, t.minute+4, t.second+3)))
    r.set(inviteCode, str(room.id))
    r.hset(str(room.id), "now", 0)
    r.hset(str(room.id), "total", 0)
    return jsonify(OK(
        invitecode = inviteCode
    ))


# 删除房间
@user.route("/deleteroom", methods=["POST"])
def userDeleteRoom():
    pass


@user.route("/joinroom", methods=["POST"])
def userJoinRoom():
    user = User.query.get(getUserId())
    inveteCode = request.json.get("inviteCode")
    roomId = r.get(inveteCode)
    urr = UserRoomRelation(userId=user.id, roomId=roomId)
    db.session.add(urr)
    db.session.commit()
    r.hincrby(roomId, "total", 1)
    return jsonify(OK(
        roomId=roomId
    ))



@user.route("/leaveroom", methods=["POST"])
def userLeaveRoom():
    user = User.query.get(getUserId())
    roomId = request.json.get("roomId")
    urr = UserRoomRelation.query.filter_by(userId=user.id, roomId=roomId).first()
    db.session.delete(urr)
    db.session.commit()
    r.hincrby(roomId, "total", -1)
    return jsonify(OK(

    ))
    pass


@user.route("/isok", methods=["POST"])
def userIsOK():
    user = User.query.get(getUserId())
    roomId = request.json.get("roomid")
    now = r.hget(roomId, "now")
    total = r.hget(roomId, "total")
    urrList = UserRoomRelation.query.filter_by(userId=user.id, roomId=roomId).all()
    urrList = sorted(urrList, key=lambda x:x.id)
    print(urrList)
    print(int(now) % int(total))
    if urrList[int(now) % int(total)].userId == user.id:
        return jsonify(OK(
            status=True
        ))
    else:
        return jsonify(OK(
            status=False
        ))
