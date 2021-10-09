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
@user.route("/drop", methods=["POST"])
def userDrop():
    filename = request.json.get("filename")
    roomId = request.json.get("roomId")
    user = User.query.get(getUserId())
    # roomid = UserRoomRelation.query.filter_by(userId=user.id).first().roomId
    print(filename)
    print(roomId)
    if filename == "no":
        resList = randDice()
        resLevel = dice2level(resList)
        resName = level2name[resLevel]

    else:
        resList = detectDices(filename)
        resLevel = dice2level(resList)
        resName = level2name[resLevel]

    prizeList = Prize.query.filter_by(roomId=roomId).all()
    r.hincrby(roomId, "now", 1)
    ret = [{
            "prizeId": prize.id,
            "awardName": prize.name,
            "avatarUrl": prize.picture,
            "level": prize.level,
            "awardNum": prize.count
        } for prize in prizeList if prize.level >= resLevel and resLevel != 0 and prize.count > 0]
    print(ret)
    return jsonify(OK(
        dicelist=resList,
        resname=resName,
        reslevel=resLevel,
        awardList=ret
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
    roomId = request.json.get("roomid")
    prize = Prize.query.get(prizeId)
    user = User.query.get(getUserId())
    print(roomId)

    # urr = UserRoomRelation.query.filter_by(userId=user.id).first()
    # if urr is None or urr.roomId != prize.roomId:
    #     return jsonify(Error1005())

    prize.count -= 1
    upr = UserPrizeRelation(userId=user.id, prizeId=prizeId, roomId=roomId)
    db.session.add(upr)
    db.session.commit()
    return jsonify(OK())



# 查看排行榜
@user.route("/rank", methods=["POST"])
def userRank():
    # 传roomid，查rank，排序，返回ranklist

    pass


# 查看奖品
@user.route("/leftprize", methods=["POST"])
def userLeftPrize():
    # 计算查prize表，返回房间内num大于0的奖品
    roomId = request.json.get("roomid")
    prizeList = Prize.query.filter_by(roomId=roomId).all()
    ret = [
        {
            "id": prize.id,
            "name": prize.name,
            "picture": prize.picture,
            "level": prize.level,
            "resname": level2name[prize.level],
            "count": prize.count
        }
        for prize in prizeList if prize.count > 0]
    return jsonify(OK(awardList=ret))

    pass


@user.route("/myprize", methods=["POST"])
def userMyPrize():
    # 传roomid和userid
    # 查prize表，返回用户自己在改房间奖品
    user = User.query.get(getUserId())
    roomId = request.json.get('roomid')
    # urr = UserRoomRelation.query.filter_by(userId=user.id).first()
    # if urr is None:
    #     return jsonify(Error1005())
    # roomId = urr.roomId
    print("userid", user.id)
    print("roomid", roomId)
    prizeIdList = [i.prizeId for i in UserPrizeRelation.query.filter_by(userId=user.id, roomId=roomId).all()]
    prizeList = [Prize.query.get(i) for i in prizeIdList]
    ret = [
        {
            "id": prize.id,
            "name": prize.name,
            "picurl": prize.picture,
            "level": prize.level,
            "resname": level2name[prize.level],
            "count": prize.count
        }
        for prize in prizeList]
    print(ret)
    return jsonify(OK(
        awardList=ret
    ))


    pass