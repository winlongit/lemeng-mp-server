#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       Administrator
    @   date    :       2019/7/28 16:37
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :
-------------------------------------------------
"""
from flask import request, session, render_template, Blueprint, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from mongoengine import OperationError
import random
import copy

from app.models.EFLUser import EFLUser
import requests
import json

"""
# 调用百度的对话 api
"""
# 百度授权服务器地址,# client_id 为官网获取的AK， client_secret 为官网获取的SK

# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'

access_token_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=gpybArE5z3euDixnBPRe0Rq4&client_secret=cQVNMxZ5tFNkq2wqtKuSfX4MDCZOafYq'

# headers中添加上content-type这个参数，指定为json格式，post 默认就是这个哟
# headers = {'Content-Type': 'application/json'}

pst_response = requests.post(access_token_host)
access_token_response = pst_response.json()
# 服务器返回的JSON文本参数如下：
#
# access_token： 要获取的Access Token；
# expires_in： Access Token的有效期(秒为单位，一般为1个月)；
# 其他参数忽略，暂时不用;
print(access_token_response)
access_token = access_token_response.get("access_token")

# 沙盒环境
# 【不区分机房】https://aip.baidubce.com/rpc/2.0/unit/bot/chat
# 生产环境
# 【华北机房】https://unit.bj.baidubce.com/rpc/2.0/unit/bot/chat
# 【华东机房】https://unit.su.baidubce.com/rpc/2.0/unit/bot/chat
# 【华南机房】"https://unit.gz.baidubce.com/rpc/2.0/unit/bot/chat
# 目前只有沙箱环境，需要正式环境需要去baidu申请，免费的哦，查看 ： https://ai.baidu.com/forum/topic/show/892085

# 以下是必须的参数，还有更多可选参数参考官网
# https://ai.baidu.com/docs#/UNIT-v2-API/top
data = {"bot_session": "",
        "log_id": "7758521",
        "request": {"bernard_level": 1,  # 系统自动发现不置信意图/词槽，并据此主动发起澄清确认的频率。取值范围：0(关闭)、1(低频)、2(高频)。取值越高代表技能对不置信意图/词槽的敏感度就越高，建议值为1
                    # "client_session": {"client_results": "",
                    #                    "candidate_options": []},
                    "query": "你好",  # 本轮请求query（用户说的话）
                    # 本轮请求query的附加信息
                    "query_info": {"asr_candidates": [],
                                   "source": "KEYBOARD",  # 请求信息来源，可选值："ASR","KEYBOARD"。ASR为语音输入，KEYBOARD为键盘文本输入
                                   # 闲聊输入参数中 request.query_info.type只能为TEXT。
                                   "type": "TEXT"},
                    "updates":"",
                    "user_id": "88888"},
        "bot_id": "72012",
        "version": "2.0"}

# response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
# print(response.json())

# 使用沙河环境
baidu_chat_url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + access_token


# Create a new chat bot named Charlie
chinese_bot = ChatBot('Charlie',
                      storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                      logic_adapters=[
                          'chatterbot.logic.BestMatch'
                      ],
                      database_uri='mongodb://localhost:27017/chatterbot-database'
                      )

trainer = ListTrainer(chinese_bot)

trainer.train([
    "语料库将会不断扩充",
    "你好,我的名字是乐盟精灵",
    "你好, 我是乐盟精灵 ",
    "你好，乐盟精灵",
    "请问有什么需要我服务您的吗？",
    "我目前的健康状态如何？ ",
    "健康状态：1、  你目前已患疾病：高血压  2、   存在的高风险疾病：高血压、 糖尿病、高脂血症、肥胖、动脉硬化 3、   您存在的高危险因素：血压高、 血糖高、血脂高、肥胖、饮食结构不合理、运动量不足、吸烟、饮酒、压 力过大、睡眠不足；4、健康指数（44.5）",
    "您目前的危险因素有变化或需要更新的吗?",
    "我戒烟了",
    "戒烟了！恭喜你，你患心脏病的风险降低了 75%，目前平均危险只有（2.0）%"
])

bp = Blueprint('efl_dialog', __name__, url_prefix="/xcc/efl/dialog")

open_not_informed = {"message": "您好，我是乐盟精灵，这是您第一次使用乐盟精灵，我需要您的帮助来完善您的基本信息", "informed": "no"}
reset_error = {"message": "重置信息失败", "code": "failed"}

questions = {
    "name": {"message": "请问，我该怎么称呼您？", "need_input": "yes", "options": [], "question": "name", "informed": "no"},
    "height": {"message": "请问，您的身高多少？（公分/厘米）？", "need_input": "yes", "options": [], "question": "height",
               "informed": "no"},
    "sex": {"message": "请问您的性别是？", "need_input": "no", "options": ["男", "女"], "question": "sex", "informed": "no"},
    "weight": {"message": "请问，您的体重多少？（斤/公斤)", "need_input": "yes", "options": [], "question": "weight",
               "informed": "no"},
    "age": {"message": "请问，您的年龄多少？（岁） ", "need_input": "yes", "options": [], "question": "age", "informed": "no"},
    "big_target": {"message": "请问您的健康管理目标是？ ", "need_input": "no", "options": ["减肥"], "question": "big_target",
                   "informed": "no"},
    "detail_target": {"message": "您的减肥目标是？ ", "need_input": "no",
                      "options": ["30 天减重 6 斤、体脂肪减去 3 斤", "BMI30 以下、体脂率 20 以下"], "question": "detail_target",
                      "informed": "no"},
    "data": {"message": "根据我们的了解,你还没给我任何体检的报告，你想现在上传数据给 我们吗？", "need_input": "no", "options": ["先不要", "没有健康报告"],
             "question": "data", "informed": "no"},
    "more": {"message": "好的，那我们是否可以多了解下您的状况？ ", "need_input": "no", "options": ["好 ", " 可以"], "question": "more",
             "informed": "no"},
    "type": {"message": "您觉得您的肥胖种类是?", "need_input": "no", "options": ["单纯性肥胖（体质型肥胖，获得性肥胖）", "遗传性肥胖", "继发性肥胖?"],
             "question": "type", "informed": "no"},
    "time": {"message": "您每周有计划的运动时间大概几分钟？ ", "need_input": "no",
             "options": ["10-30分钟", "30-60分钟", "60-100分钟", "100分钟以上"], "question": "time", "informed": "no"},
    "activity": {"message": "你一般都做什么种类的运动？ ", "need_input": "yes", "options": [], "question": "activity", "informed": "no"},
    "taocan": {"message": "根据您的个人身体状况与习惯，加上乐盟精灵机器学习的结果，建 议您采用“乐盟基础个性化健康管理”套餐，并且建议尽早采用乐盟体检套餐并从事相关的基因检测以便更精准的管理好自己的健康 ",
               "need_input": "no", "options": ["好的，谢谢"], "question": "taocan", "informed": "no"},
    "shop": {"message": "另外，我们乐盟商城有很多适合您的健康产品与服务，您 有兴趣了解下或参考下我们的推荐吗？ ", "need_input": "no", "options": ["期待开放"],
             "question": "shop", "informed": "no"},
    "informed": {"message": "结束收集信息", "need_input": "yes", "options": [], "question": "informed", "informed": "yes"}
}


@bp.route("/informed_all", methods=["POST", "GET"])
def task_list3():
    message = request.args.get("message")
    openid = request.args.get("openid")
    cur_question = request.args.get("cur_question")

    print("informed_all message:", message)
    print("informed_all openid:", openid)

    user = EFLUser.objects(xcc_openid=openid).first()
    print(user.to_mongo())
    rs = {"message": 'yoyoyoyoy!', "informed": "yes"}

    # 如果是刚开打小程序,就要判断他是不是收集信息结束了,问候语
    if message == "open":
        # 如果信息齐全,就发  "xxx，我是乐盟精灵"
        if getattr(user, "informed"):
            print("open informed")
            rs["message"] = user.name + ",我是乐盟精灵。"
            return jsonify(rs)
        else:
            # 如果信息不齐全,就发一句收集信息的东西 : 您好，我是乐盟精灵，这是您第一次使用乐盟精灵，我需要您的帮助来完善您的基本信息
            return jsonify(open_not_informed)

    # 开启对话，服务器开始
    if message == "open_dialog":
        # 如果信息齐全,就发  "有什么可以帮助你的吗？"
        if getattr(user, "informed"):
            print("open informed")
            rs["message"] = user.name + ",有什么可以帮助你的吗？"
            return jsonify(rs)
        else:
            # 如果信息不齐全,就检索缺少的信息发过去
            for question_name, question_struc in questions.items():
                # 这个属性为空，就表示这个信息没有收集到
                if hasattr(user, question_name):
                    if not getattr(user, question_name):
                        rs = question_struc
                        # print("如果信息不齐全,就检索缺少的信息发过去rsrsrs informed_all:", rs)
                        if question_name == "informed":
                            setattr(user, "informed", "yes")
                            user.save()
                        return jsonify(rs)

    print("cur_question cur_question", cur_question)
    # 如果有 cur_question 字段，并且 问题是收集问题表中的问题时，说明这个时候是在收集问题，那就接着回答问题
    if cur_question and cur_question in questions.keys():
        print("未收集到的信息 cur_question:" + cur_question)
        if hasattr(user, str(cur_question)):
            setattr(user, cur_question, message)
            user.save()
            for question_name, question_struc in questions.items():
                # 如果存在 question_name 这个属性，并且这个属性为的值空，就表示这个信息没有收集到
                if hasattr(user, question_name):
                    if not getattr(user, question_name):
                        rs = copy.deepcopy(question_struc)
                        # print("如果存在 question_name 这个属性，并且这个属性为的值空，就表示这个信息没有收集到rsrsrs informed_all:", rs)
                        if question_name == "informed":
                            print("do save do save do save do save do save do save ")
                            setattr(user, "informed", "yes")
                            user.save()
                        if random.randint(0,4) == 1:
                            rs["message"] = user.name + "， " + rs["message"]
                        # print("最后发回去的样子", rs)
                        # print(questions)
                        return jsonify(rs)

    print("rsrsrs informed_all:", rs)
    return jsonify(rs)


@bp.route("/reset", methods=["POST", "GET"])
def reset_user():
    openid = request.args.get("openid")
    user = EFLUser.objects(xcc_openid=openid).first()
    try:
        for question_name, _ in questions.items():
            setattr(user, question_name, None)
        # print(user.to_mongo())
        user.save()
    except OperationError as e:
        print(e)
        return jsonify(reset_error)
    return jsonify(questions["name"])


@bp.route("/informed", methods=["POST", "GET"])
def task_list1():
    message = request.args.get("message")
    openid = request.args.get("openid")
    informed = request.args.get("informed_user")
    print("informed11111:", informed)
    informed = True if informed == "yes" else False
    print("informed message:" + message)
    print("informed openid:" + openid)
    print("informed22222:", informed)
    # 这里很蠢，如果句子里面有健康状态和戒烟，就回复固定内容
    if "健康" in message or "状态" in message:
        return jsonify({"message": "1、  你目前已患疾病：高血压  2、   存在的高风险疾病：高血压、 糖尿病、高脂血症、肥胖、动脉硬化 3、   您存在的高危险因素：血压高、 血糖高、血脂高、肥胖、饮食结构不合理、运动量不足、吸烟、饮酒、压 力过大、睡眠不足；4、健康指数（44.5）"})
    elif "戒烟" in message:
        return jsonify({"message": "戒烟了！恭喜你，你患心脏病的风险降低了 75%，目前平均危险只有（2.0）%"})
    rd = random.randint(0, 8)
    rs_message = ""
    # 使用baidu的对话机器人
    # 每次访问前替换  data["request"]["query"]
    data["request"]["query"] = message
    response = requests.post(baidu_chat_url, data=json.dumps(data))
    res_json = response.json()
    print(res_json)
    # error_code== 0 表示 百度 返回 成功  status== 0 表示返回对话语句成功 ，
    # 反回的是 res_json.get("result").get("response").get("action_list") 是个 LIst
    # 'action_list': [{
    #     'action_id': '',
    #     'refine_detail': {},
    #     'confidence': 1.0,
    #     'custom_reply': '',
    #     'say': '你好 小猫',
    #     'type': 'chat'
    # },
    if res_json.get("error_code") == 0 and res_json.get("result").get("response").get("status") == 0:
        action_list = res_json.get("result").get("response").get("action_list")
        rs_message = action_list[rd % len(action_list)].get("say")
        # 每次访问结束后，替换 data["bot_session"]，这样百度就会追踪对话
        data["bot_session"] = res_json.get("result").get("bot_session")
    # 万一百度的挂了，就调用自己的
    else:
        # 使用自己的 chatterbot
        tmp = chinese_bot.get_response(message)
        # chinese_bot 返回的是一个 chatterbot封装好的对象，把他变成 str
        rs_message = str(tmp)
    # 随机给回答的前面加上用户的名字
    if rd == 1:
        user = EFLUser.objects(xcc_openid=openid).first()
        rs_message = user.name + "," + rs_message
    rs = {"message": rs_message}
    print("rd: ", rd, " rsrsrs: ", rs)
    return jsonify(rs)


@bp.route("/no_informed", methods=["POST", "GET"])
def task_list2():
    message = request.args.get("message")
    openid = request.args.get("openid")
    cur_question = request.args.get("cur_question")
    print("no_informed message:" + message)
    print("no_informed openid:" + openid)
    if cur_question:
        print("no_informed cur_question:" + cur_question)
        print(type(cur_question))
    from app.models.EFLUser import EFLUser
    user = EFLUser.objects(xcc_openid=openid).first()
    print(user.to_mongo())
    if hasattr(user, str(cur_question)):
        setattr(user, cur_question, message)
        user.save()

    for question_name, question_struc in questions.items():
        # 这个属性为空，就表示这个信息没有收集到
        if hasattr(user, question_name):
            if not getattr(user, question_name):
                rs = question_struc
                print("rsrsrs no_informed:", rs)
                return jsonify(rs)

    return jsonify({"message": 'Hello World2222222!'})

