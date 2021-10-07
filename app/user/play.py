import json

from app.user import user
from flask import request, jsonify
from app.model.dbmodel import *
from app.utils.jwt import getToken
from app.model.response import *
from app.utils.jwt import *
from app.utils.dice import *
from app import r


# 扔骰子
@user.route("drop", methods=["POST"])
def userDrop():
    jsondata = request.json

    user = User.query.get(getUserId())
    roomid = UserRoomRelation.query.filter_by(userId=user.id).first().roomId

    if jsondata is None:
        resList = randDice()
        resLevel = dice2level(resList)
        resName = level2name[resLevel]

    else:
        filename = jsondata.get("filename")
        resList = detectDices(filename)
        resLevel = dice2level(resList)
        resName = level2name[resLevel]

    prizeList = Prize.query.filter_by(roomId=roomid).all()
    r.hincrby(roomid, "now", 1)
    return jsonify(OK(
        dicelist=resList,
        resname=resName,
        prizes=[{
            "awardName": prize.name,
            "avatarUrl": prize.picture,
            "level": prize.level,
            "awardNum": prize.count
        } for prize in prizeList if prize.level <= resLevel]
    ))
    # 如果没有图片，就随机
    # 如果有图片，给yolo识别返回结果
    # 更新用户rank，没有则创建
    # 返回可获得的奖品
    # 提示下一个人投
    pass


# 用户选择奖品
@user.route("/chooseprize", methods=["POST"])
def userChoosePrize():
    # 根据奖品id，判断一下是不是大于0，然后添加用户奖品relation
    prizeId = request.json.get("prizeid")
    prize = Prize.query.get(prizeId)
    user = User.query.get(getUserId())

    urr = UserRoomRelation.query.filter_by(userId=user.id).first()
    if urr is None or urr.roomId != prize.roomId:
        return jsonify(Error1005())

    prize.count -= 1
    upr = UserPrizeRelation(userId=user.id, prizeId=prizeId, roomId=urr.roomId)
    db.session.add(upr)
    db.session.commit()
    return jsonify(OK())



# 查看排行榜
@user.route("/rank", methods=["POST"])
def userRank():
    # 传roomid，查rank，排序，返回ranklist

    pass


# 查看奖品
@user.route("/leftprize", methods=["GET"])
def userLeftPrize():
    # 计算查prize表，返回房间内num大于0的奖品
    roomId = request.json.get("roomid")
    prizeList = Prize.query.filter_by(roomId=roomId).all()
    ret = [
        {
            "id": prize.id,
            "name": prize.name,
            "picurl": prize.picture,
            "level": prize.level,
            "count": prize.count
        }
        for prize in prizeList]
    return jsonify(ret)

    pass


@user.route("/myprize", methods=["GET"])
def userMyPrize():
    # 传roomid和userid
    # 查prize表，返回用户自己在改房间奖品
    user = User.query.get(getUserId())
    urr = UserRoomRelation.query.filter_by(userId=user.id).first()
    if urr is None:
        return jsonify(Error1005())
    roomId = urr.roomId
    prizeIdList = [i.prizeId for i in UserPrizeRelation.query.filter_by(userId=user.id, roomId=roomId).all()]
    prizeList = [Prize.query.get(i) for i in prizeIdList]
    ret = [
        {
            "id": prize.id,
            "name": prize.name,
            "picurl": prize.picture,
            "level": prize.level,
            "count": prize.count
        }
        for prize in prizeList]
    return jsonify(ret)


    pass