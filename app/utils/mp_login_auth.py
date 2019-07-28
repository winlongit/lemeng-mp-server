# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import time

from app.utils.wechat_base import Map

__all__ = "LoginAuth"


class LoginAuth:
    def __init__(self, mp_id, mp_secret):
        # 创建一个自己的操作器opener 类型为HTTPSHandler
        self.opener = urllib.request.build_opener(urllib.request.HTTPSHandler)
        self.mp_id = mp_id
        self.mp_secret = mp_secret

    # 对URL地址加参数
    def add_query(self, url, args):
        # 如果没有参数就直接用这个URL
        if not args:
            return url
        return url + (' ?' in url and '&' or '?') + urllib.parse.urlencode(args)

    # 组装初始的URL和参数，发送请求，得到返回的json
    def send_get(self, url, params):
        # 对URL添加参数
        url = self.add_query(url, params)
        # 有了这个opener之后，我们就可以用它来打开/读取 url。整个过程都在opener.open(url)
        # 这个函数中接受三个参数：fullurl，data，timeout。
        # fullurl其实有两种形式：一种是url，另一种是Request对象。
        # 经过httplib处理完成返回的Response对象有点像一个文件对象，直接用read()
        req = urllib.request.Request(url)
        resp = self.opener.open(req)
        data = Map(json.loads(resp.read().decode('utf-8')))
        print("ddddddddddddddd", data)
        if data.errcode:
            msg = "%(errcode)d %(errmsg)s" % data
            raise msg
        return data

    def send_post(self, url, params, data):
        url = self.add_query(url, params)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(data)
        jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))

        resp = urllib.request.urlopen(req, jsondataasbytes)

        data = Map(json.loads(resp.read().decode('utf-8')))
        if data.errcode:
            msg = "%(errcode)d %(errmsg)s" % data
            raise msg
        return data

    # 得到用户的 openid 用户唯一标识 session_key 会话密钥
    # 用时传参 code ，code 是小程序端通过 wx.login 或者 uni.login 获取到的
    def get_access_token(self, code):
        # 请求微信小程序的自己的URL链接，参考微信官方手册
        # https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
        url = "https://api.weixin.qq.com/sns/jscode2session"
        args = dict()
        args.setdefault("appid", self.mp_id)
        args.setdefault("secret", self.mp_secret)
        print("mp_id: ",self.mp_id)
        print("mp_secret: ",self.mp_secret)
        print("code:", code)
        args.setdefault("js_code", code)
        args.setdefault("grant_type", "authorization_code")
        return self.send_get(url, args)

    # 正确时返回的JSON数据包如下：
    # {
    # 'session_key': 'Q6fHQE5CZUwIbaM8BALjFQ==',
    # 'openid': 'oQwz25c3BEwSUjG5a3FINcSIHub8'
    # }

    # 错误时微信会返回JSON数据包如下（示例为Code无效错误）:
    # {"errcode": 40029, "errmsg": "invalid code"}

    # 检验access——token凭证是否有效(用时传参access_token,openid)
    def check_token(self, access_token, openid):
        # 请求的微信URL链接
        url = "https://api.weixin.qq.com/sns/auth"
        args = dict()
        args.setdefault("access_token", access_token)
        args.setdefault("openid", openid)
        return self.send_get(url, args)

    # 正确的Json返回结果：
    # { "errcode":0,"errmsg":"ok"}
    # 错误时的Json返回示例：
    # { "errcode":40003,"errmsg":"invalid openid"}

    # 后面微信支付调用JS接口，需要授权缺少jsapi_ticket，需要使用access——token才行
    def get_jsapi_ticket(self, accesstoken):
        url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket"
        args = dict()
        args.setdefault("access_token", accesstoken)
        args.setdefault("type", "jsapi")
        return self.ticket_send_get(url, args)

    # 成功返回如下JSON：
    # {
    #     "errcode": 0,
    #     "errmsg": "ok",
    #     "ticket": "bxLdikRXVbTPdHSM05e5u5sUoXNKd8-41ZO3MhKoyN5OfkWITDGgnr2fwJ0m9E8NYzWKVZvdVtaUgWvsdshFKA",
    #     "expires_in": 7200
    # }

    # 重新获取access——token(用时传参refresh_token)
    def token_refresh(self, refresh_token):
        # 请求微信URL链接
        url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
        args = dict()
        args.setdefault("appid", self.mp_id)
        args.setdefault("grant_type", "refresh_token")
        args.setdefault("refresh_token", refresh_token)
        return self.send_get(url, args)

    # 正确时返回的JSON数据包如下：
    # {
    #     "access_token": "ACCESS_TOKEN",
    #     "expires_in": 7200,
    #     "refresh_token": "REFRESH_TOKEN",
    #     "openid": "OPENID",
    #     "scope": "SCOPE"
    # }
    # 错误时微信会返回JSON数据包如下（示例为Code无效错误）:
    # {"errcode": 40029, "errmsg": "invalid code"}

    # 获取用户信息(用时传参access_token ,openid)
    def user_info(self, access_token, openid):
        # 请求微信URL链接
        url = "https://api.weixin.qq.com/sns/userinfo"
        args = dict()
        args.setdefault("access_token", access_token)
        args.setdefault("openid", openid)
        args.setdefault("lang", "zh_CN ")
        return self.send_get(url, args)

    # 正确时返回的JSON数据包如下：
    # {
    #     "openid": " OPENID",
    #     " nickname": NICKNAME,
    #     "sex": "1",
    #     "province": "PROVINCE"
    #                 "city":"CITY",
    #                 "country":"COUNTRY",
    #                 "headimgurl":"http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6
    #                               iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLr
    #                               hJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46",
    #                 "privilege":[
    #                              "PRIVILEGE1"
    #                               "PRIVILEGE2"
    #                             ],
    #     "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
    # }
    # 错误时微信会返回JSON数据包如下（示例为openid无效）:
    # {"errcode":40003,"errmsg":" invalid openid "}
