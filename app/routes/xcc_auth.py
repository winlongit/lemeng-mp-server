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

bp = Blueprint('xcc_auth', __name__, url_prefix="/wx/user")

mp_id = config.get('MP_APPID')
mp_secret = config.get('MP_SECRET')

mp_id_efl = config.get('MP_APPID_EFL')
mp_secret_efl = config.get('MP_SECRET_EFL')

wx_login_auth = LoginAuth(mp_id, mp_secret)
wx_login_auth_efl = LoginAuth(mp_id_efl, mp_secret_efl)

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
    return jsonify(data2)

# 有2个小程序，先分开写吧，后面再传参根据不同选择不同的 appid，来统一接口，现在先直接写，节约时间
# TODO
@bp.route("/login_efl", methods=["POST", "GET"])
def get_json_efl():
    data = request.get_json()
    code = data["code"]
    print(data)
    print(code)
    # 用code换取需要的access_token
    data2 = wx_login_auth_efl.get_access_token(code)
    # 调用上面方法，从返回的json数据里得到 对应数据 openid
    print(data2)
    from app.models.EFLUser import EFLUser
    if not EFLUser.objects(xcc_openid=data2.openid):
        user = EFLUser(xcc_openid=data2.openid)
        user.save()
    return jsonify(data2)
