#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       JackyPJB
    @   date    :       2019/6/2 0002 下午 6:52
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""

__author__ = 'Max_Pengjb'

from flask import request, session, Blueprint, jsonify
# 获取config
from app import app
config = app.config
from app.utils.mp_login_auth import LoginAuth

bp = Blueprint('xcc_auth', __name__, url_prefix="/xcc")

mp_id = config.get('MP_APPID')
mp_secret = config.get('MP_SECRET')

wx_login_auth = LoginAuth(mp_id, mp_secret)

# GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
@bp.route("/login", methods=["POST", "GET"])
def get_json():
    data = request.get_json()
    code = data["code"]
    print(data)
    print(code)
    # 用code换取需要的access_token
    data2 = wx_login_auth.get_access_token(code)
    # 调用上面方法，从返回的json数据里得到 对应数据 openid
    print(data2)
    return jsonify({"name": "sb", "age": 2})
