from datetime import datetime, timedelta

import jwt

from app.setting import SECRET_KEY

from flask import request


def getPayload(userId):
    payload = {  # jwt设置过期时间的本质 就是在payload中 设置exp字段, 值要求为格林尼治时间
        "user_id": userId,
        "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24 * 30),
    }
    return payload


# 生成token
def getToken(userId):
    return jwt.encode(getPayload(userId=userId), key=SECRET_KEY, algorithm='HS256')


def checkToken(token):
    global data
    try:
        data = jwt.decode(token, key=SECRET_KEY, algorithms='HS256')
    except Exception as e:
        return None
    return data


# 登录验证装饰器
def getUserId():
    token = request.headers.get('Authorization').split(" ")[1]
    data = checkToken(token)
    return data["user_id"]
