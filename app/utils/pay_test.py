import time

from wechatpy import WeChatPay
mp_id = 'wxc6221cda3f95b53f'
mp_mch_id = '1533695991'
mp_mch_key = 'c9a5241f1d9b1a21659f75cb0e3d82ba'
# 这里吃的大亏，回调地址不能用 https ， fuck
http_root = 'http://swu.mynatapp.cc'
notify_url = http_root + '/wx/shop_pc_pay/notifyurl'
wx_pay = WeChatPay(appid=mp_id, mch_id=mp_mch_id, mch_key=mp_mch_key, api_key=mp_mch_key)
# 这里还有一个 请求 sign 的构造过程， wechatpy 都已经封装好了
rs = wx_pay.order.create(trade_type="NATIVE",
                         total_fee=1,  # 订单总金额，单位为分
                         notify_url=notify_url,  # 异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的 http 地址，不能是 https ，不能携带参数。
                         # user_id=request.args.get("openid"),  # 小程序appid下的唯一标识 trade_type=JSAPI和sub_appid已设定，此参数必传
                         body="测试",  # 商品详细描述，对于使用单品优惠的商户，该字段必须按照规范上传
                         out_trade_no=str(int(time.time())),  # 商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*且在同一个商户号下唯一
                         )
print(rs)
code_url = rs['code_url']
print(code_url)
# 获取 url_code 把这个code返回给前端，让前端生成 qrcode


