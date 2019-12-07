#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       Administrator
    @   date    :       2019/6/27 21:39
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
import hashlib
import random
import time
import urllib.request
from xml.etree import ElementTree as eTree
from wechatpy.pay import WeChatPay

from flask import Blueprint, jsonify

from app import app
from app.utils.wechat_base import Map
from wechatpy import WeChatPay

try:
    from flask import request
except Exception:
    request = None

config = app.config
bp = Blueprint('xcc_shop_proc_manage', __name__, url_prefix="/wx/proc_manage")


@bp.route("/add_proc", methods=["POST", "GET"])
def get_json1():
    print(request.args)

    return jsonify({"ok":"ok"})
