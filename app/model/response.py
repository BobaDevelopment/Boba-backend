def OK(msg="", **kwargs):
    return {
        "status": 0,
        "msg": msg,
        "data": kwargs
    }


# 验证不通过
def Error1001():
    return {
        "status": 1001,
        "msg": "Unauthorized"
    }

# 账号或者密码错误
def Error1002():
    return {
        "status": 1002,
        "msg": "Wrong account or password"
    }

# 请求参数错误
def Error1003():
    return {
        "status": 1003,
        "msg": "Wrong request parameter"
    }

# 文件上传错误
def Error1004():
    return {
        "status": 1004,
        "msg": "Upload failed"
    }

# 没有权限操作对象
def Error1005():
    return {
        "status": 1005,
        "msg": "No permission to manipulate objects"
    }