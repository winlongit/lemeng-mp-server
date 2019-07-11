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
bp = Blueprint('xcc_pay', __name__, url_prefix="/wx/pay")

mp_id = config.get('MP_APPID')
mp_secret = config.get('MP_SECRET')
mp_mch_id = config.get('MP_MCH_ID')
mp_mch_key = config.get('MP_MCH_KEY')
# 这里吃的大亏，回调地址不能用 https ， fuck
http_root = config.get('HTTP_ROOT')
notify_url = http_root + '/wx/pay/notifyurl'

mch_key = config.get('WECHAT_MCH_KEY')
"""
appid – 微信公众号/或者小程序号
api_key – 商户 key, 不要在这里使用小程序的密钥
mch_id – 商户号
(sub_mch_id – 可选，子商户号，受理模式下必填，这里不填)
(mch_cert – 商户证书路径，这里不填)
mch_key – 必填，商户证书私钥路径(小程序，这里也填商户号key)
timeout – 可选，请求超时时间，单位秒，默认无超时设置
sandbox – 可选，是否使用测试环境，默认为 False
"""
wx_pay = WeChatPay(appid=mp_id,
                   mch_id=mp_mch_id,
                   mch_key=mp_mch_key,
                   api_key=mp_mch_key)


@bp.route("/reqPay", methods=["POST", "GET"])
def get_json1():
    # 这里还有一个 请求 sign 的构造过程， wechatpy 都已经封装好了
    rs = wx_pay.order.create(trade_type="JSAPI",
                             total_fee=1,  # 订单总金额，单位为分
                             notify_url=notify_url,  # 异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的 http 地址，不能是 https ，不能携带参数。
                             user_id=request.args.get("openid"),  # 微信分配的小程序ID,擦嘞
                             body="测试",  # 商品详细描述，对于使用单品优惠的商户，该字段必须按照规范上传
                             client_ip=request.remote_addr,  # 这就是 spbill_create_ip，换两个名字
                             out_trade_no=str(int(time.time())),  # 商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*且在同一个商户号下唯一
                             )
    # 获取 paySign
    # paySign wx_pay.jsapi.get_jsapi_signature(rs["prepay_id"])
    jsapi_params = wx_pay.jsapi.get_jsapi_params(rs["prepay_id"])
    return jsonify(jsapi_params)


# 微信推送消息是XML格式，使用wechatpy的parse_payment_result方法可以将结果转化成OrderedDict类型，且帮你做好了验签。
@bp.route("/notifyurl", methods=["GET", "POST"])
def get_notify_url():
    notify_data = request.data
    print(notify_data)
    data = wx_pay.parse_payment_result(notify_data)
    print(data)
    # 然后就可以根据返回的结果，处理之前的订单了。
    # TODO 写上处理结果的逻辑。存储数据库之类的
    # 唯一需要注意的一点，微信推送消息后，需要给微信服务器返回一个消息：
    return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"


"""  之前没用 wechatpy ， 自己手动写的方法， 能用，但是有现成的封装好的不是更好吗
    感谢 wechatpy 的作者 https://wechatpy.readthedocs.io/zh_CN/master/pay.html#module-wechatpy.pay
# 生成随机字符串，长度要求在32位以内
def creat_nonce_str():
    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ascii_letters = ascii_lowercase + ascii_uppercase
    digits = '0123456789'
    char = ascii_letters + digits
    return "".join(random.choice(char) for _ in range(16))


to_uft8 = lambda x: x.encode("utf-8") if isinstance(x, str) else x


# 签名所有发送或者接收到的数据为集合M,将集合M内非空参数值的参数按照参数名ASCII码从小到大排序
# URL键值对的格式（即key1 = value1 & key2 = value2…）拼接成字符串stringA
# tringA最后拼接上key得到stringSignTemp字符串，并对stringSignTemp进行MD5运算，
# 再将得到的字符串所有字符转换为大写
def sign(pay_data):
    stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, mp_mch_key)
    return hashlib.md5(to_uft8(stringSignTemp)).hexdigest().upper()


# 生成xml格式发送
def to_xml(arr):
    xml = ["<xml>"]
    for k, v in arr.items():
        if v.isdigit():
            xml.append("<{0}>{1}</{0}>".format(k, v))
        else:
            xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)


# 每个element对象都具有以下属性：
# 1.tag：string对象，表示数据代表的种类。
# 2.attrib：dictionary对象，表示附有的属性。
# 3.text：string对象，表示element的内容。
# 4.tail：string对象，表示element闭合之后的尾迹。
# 例如：< tag attrib1 = 1 > text < / tag > tail
def to_dict(content):
    raw = {}
    root = eTree.fromstring(content)
    for child in root:
        raw[child.tag] = child.text
    return raw


# 实行发送请求，并且得到返回结果
def pay_send_get(url, xml_data):
    req = urllib.request.Request(url, bytes(xml_data, encoding="utf8"))
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler())
    # try:
    # resp = urllib.request.urlopen(url,bytes(data, encoding="utf8"), timeout=20)
    resp = opener.open(req, timeout=20).read()
    print("统一下单返回：")
    print(resp)
    # # except urllib.request.HTTPSHandler as e:
    # #     resp = e
    res_data = Map(to_dict(resp))

    # 微信服务器返回的xml里有:
    # 返回状态码：return_code
    # 此字段是通信标识，非交易标识，交易是否成功需要查看result_code来判断
    # 返回信息:return_msg     如果无错为空
    if res_data.return_code == "FAIL":
        # raise PayError(data.return_msg)
        raise res_data.return_msg

    # 得到了返回的xml，并且转成dict类型
    return res_data
# python小程序付款参考： https://www.jianshu.com/p/07ed48e4a50b
@bp.route("/reqPay1", methods=["POST", "GET"])
def get_json():
    spbill_create_ip = request.remote_addr
    openid = request.args.get("openid")
    print(openid)
    data = {
        'appid': mp_id,  # 微信分配的小程序ID,擦嘞，这里的appid 的 i 是小写
        'mch_id': mp_mch_id,  # 微信支付分配的商户号
        'nonce_str': creat_nonce_str(),  # 随机字符串，长度要求在32位以内
        'body': '测试',  # 商品详细描述，对于使用单品优惠的商户，该字段必须按照规范上传
        'out_trade_no': str(int(time.time())),  # 商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*且在同一个商户号下唯一
        'total_fee': '1',  # 订单总金额，单位为分
        'spbill_create_ip': spbill_create_ip,  # 支持IPV4和IPV6两种格式的IP地址。调用微信支付API的机器IP 支付提交用户端ip，得到终端ip
        'notify_url': notify_url,  # 异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。
        'attach': '{"msg": "自定义数据"}',  # 附加数据，在查询API和支付通知中原样返回，可作为自定义参数使用。
        'trade_type': "JSAPI",  # 小程序取值如下：JSAPI
        'openid': openid  # 用户标识 当 trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。
    }
    get_sign = sign(data)
    print("第一次搞到sign：")
    print(get_sign)
    data["sign"] = get_sign
    print(data)
    get_xml = to_xml(data)
    print(get_xml)
    res_data = pay_send_get("https://api.mch.weixin.qq.com/pay/unifiedorder", get_xml)
    print(res_data)
    # 得到prepay_id 微信生成的预支付会话标识，用于后续接口调用中使用，该值有效期为2小时
    prepay_id = res_data["prepay_id"]
    # 生成wx.requestPayment小程序中的paySign签名: https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=7_7
    paySign_data = {
        'appId': mp_id,  # 微信分配的小程序ID 擦嘞，这里的appId 的 I 是大写
        'timeStamp': str(int(time.time())),  # 时间戳从1970年1月1日00:00:00至今的秒数,即当前的时间
        'nonceStr': creat_nonce_str(),  # 随机字符串，不长于32位
        'package': 'prepay_id={0}'.format(prepay_id),
        # 统一下单接口返回的 prepay_id 参数值，提交格式如：prepay_id=wx2017033010242291fcfe0db70013231072
        'signType': 'MD5'  # 签名类型，默认为MD5
    }
    # 生成 sign 签名
    get_paySign = sign(paySign_data)
    print("这次搞到的sign" + get_paySign)
    paySign_data["paySign"] = get_paySign
    print(paySign_data)
    return jsonify(paySign_data)
    
@bp.route("/notifyurl", methods=["GET", "POST"])
def get_notify_url():
    print("yes,here")
    allthings = request.stream.read()
    print(allthings)
    respData = {'return_code': "SUCCESS"}
    # respData = arrayToXml(respData)
    return to_xml(respData)
"""
