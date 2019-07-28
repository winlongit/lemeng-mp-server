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


bp = Blueprint('efl_dialog', __name__, url_prefix="/xcc/efl/dialog")


open_not_informed = {"message": "您好，我是乐盟精灵，这是您第一次使用乐盟精灵，我需要您的帮助来完善您的基本信息","informed": "no"}

questions = {
    "name": {"message": "请问我怎么称呼您？", "need_input": "yes", "options": [], "question": "name", "informed": "no"},
    "height": {"message": "请问，您的身高多少？（公分/厘米）？", "need_input": "yes", "options": [], "question": "height", "informed": "no"},
    "weight":{"message": "请问，您的体重多少？（斤/公斤)", "need_input": "yes", "options": [], "question": "weight", "informed": "no"},
    "age" : {"message": "请问，您的年龄多少？（岁） ", "need_input": "yes", "options": [], "question": "age", "informed": "no"},
    "big_target" : {"message": "请问您的健康管理目标是？ ", "need_input": "no", "options": ["减肥"], "question": "big_target", "informed": "no"},
    "detail_target" : {"message": "您的减肥目标是？ ", "need_input": "no", "options": ["30 天减重 6 斤、体脂肪减去 3 斤","BMI30 以下、体脂率 20 以下"], "question": "detail_target", "informed": "no"},
    "data" : {"message": "根据我们的了解,你还没给我任何体检的报告，你想现在上传数据给 我们吗？", "need_input": "no", "options": ["先不要", "没有健康报告"], "question": "data", "informed": "no"},
    "more" : {"message": "好的，那我们是否可以多了解下您的状况？ ", "need_input": "no", "options": ["好 "," 可以"], "question": "more", "informed": "no"},
    "type" : {"message": "您觉得您的肥胖种类是?", "need_input": "no", "options": ["单纯性肥胖（体质型肥胖，获得性肥胖）","遗传性肥胖","继发性肥胖?"], "question": "type", "informed": "no"},
    "time" : {"message": "您每周有计划的运动时间大概几分钟？ ", "need_input": "no", "options": ["10-30分钟","30-60分钟","60-100分钟","100分钟以上"], "question": "time", "informed": "no"},
    "activity" : {"message": "有什么种类的运动？ ", "need_input": "yes", "options": [], "question": "activity", "informed": "no"},
    "taocan" : {"message": "根据您的个人身体状况与习惯，加上乐盟精灵机器学习的结果，建 议您采用“乐盟基础个性化健康管理”套餐，并且建议尽早采用乐盟体检套餐并从事相关的基因检测以便更精准的管理好自己的健康 ", "need_input": "no", "options": ["好的，谢谢"], "question": "taocan", "informed": "no"},
    "shop" : {"message": "另外，林大宝，我们乐盟商城有很多适合您的健康产品与服务，您 有兴趣了解下或参考下我们的推荐吗？ ", "need_input": "no", "options": ["期待开放"], "question": "shop", "informed": "no"},
    "informed": {"message": "结束收集信息", "need_input": "yes", "options": [], "question": "informed", "informed": "yes"}
}


@bp.route("/informed_all", methods=["POST", "GET"])
def task_list3():
    message = request.args.get("message")
    openid = request.args.get("openid")
    cur_question = request.args.get("cur_question")

    print("informed_all message:", message)
    print("informed_all openid:", openid)

    from app.models.EFLUser import EFLUser
    user = EFLUser.objects(xcc_openid=openid).first()
    print(user.to_mongo())
    rs = {"message": 'yoyoyoyoy!',"informed": "yes"}

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
                        print("rsrsrs informed_all:", rs)
                        if question_name == "informed":
                            setattr(user, "informed", "yes")
                            user.save()
                        return jsonify(rs)

    print("cur_question cur_question",cur_question)
    # 如果有 cur_question 字段，并且 问题是收集问题表中的问题时，说明这个时候是在收集问题，那就接着回答问题
    if cur_question and cur_question in questions.keys():
        print("no_informed cur_question:" + cur_question)
        if hasattr(user, str(cur_question)):
            setattr(user, cur_question, message)
            user.save()
            for question_name, question_struc in questions.items():
                # 这个属性为空，就表示这个信息没有收集到
                if hasattr(user, question_name):
                    if not getattr(user, question_name):
                        rs = question_struc
                        print("rsrsrs informed_all:", rs)
                        if question_name == "informed":
                            print("do save do save do save do save do save do save ")
                            setattr(user, "informed", "yes")
                            user.save()
                        return jsonify(rs)

    print("rsrsrs informed_all:", rs)
    return jsonify(rs)


@bp.route("/informed", methods=["POST", "GET"])
def task_list1():
    message = request.args.get("message")
    openid = request.args.get("openid")
    informed = request.args.get("informed_user")
    print("informed11111:", informed)
    informed = True if informed == "yes" else False
    print("informed message:"+message)
    print("informed openid:"+openid)
    print("informed22222:", informed)
    rs = {"message": 'informedinformedinformed'}
    print("rsrsrs:", rs)
    return jsonify(rs)


@bp.route("/no_informed", methods=["POST", "GET"])
def task_list2():
    message = request.args.get("message")
    openid = request.args.get("openid")
    cur_question = request.args.get("cur_question")
    print("no_informed message:"+message)
    print("no_informed openid:"+openid)
    if cur_question:
        print("no_informed cur_question:"+cur_question)
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


if __name__ == '__main__':
    from chatterbot import ChatBot
    from chatterbot.trainers import ListTrainer

    my_bot = ChatBot("Training demo")
    my_bot.set_trainer(ListTrainer)
    my_bot.train([
        "嗳，渡边君，真喜欢我?",
        "那还用说?",
        "那么，可依得我两件事?",
        "三件也依得",
    ])

    # test
    print(my_bot.get_response("真喜欢我?"))
    print(my_bot.get_response("可依得我两件事?"))
