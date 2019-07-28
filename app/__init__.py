#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       JackyPJB
    @   date    :       2019/6/1 0001 下午 7:06
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
from bson import ObjectId

__author__ = 'Max_Pengjb'
from flask import Flask, current_app, session, g, request, jsonify, Response
from config import load_config
from app.dbengines import db
# TODO socket.io 语音对话，后期再加吧
# from app.socketio import socket_io
# 初始化 App
app = Flask(__name__)

config = load_config()
# 加载配置
app.config.from_object(config)
db.init_app(app)
# TODO socket.io 语音对话，后期再加吧
# socket_io.init_app(app)

print(config.DD)
print(config.FF)
# 整合各个route页面
from flask.blueprints import Blueprint
from app import routes


def _import_submodules_from_package(package):
    import pkgutil

    modules = []
    # 在只知道包名的情况下，成功获取了包下所有模块
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix=package.__name__ + "."):
        print("{} name: {}, is_sub_package: {}".format(importer, modname, ispkg))
        modules.append(__import__(modname, fromlist="dummy"))
    return modules


for module in _import_submodules_from_package(routes):
    bp = getattr(module, 'bp')
    if bp and isinstance(bp, Blueprint):
        # 注册蓝图
        app.register_blueprint(bp)


@app.route("/")
def index():
    from app.models.Task import Task
    task = Task.objects()
    print(task)
    # g作为flask程序全局的一个临时变量, 充当者中间媒介的作用, 我们可以通过它传递一些数据,
    # 下面的例子, 通过g传递了一个名字叫做"Peng", 使用g之前也需要激活程序上下文:
    g.name = "Peng"
    print(g.name)
    print(session.get("user"))
    # 如果dict中存在key，则返回key的值， 如果不存在key，则返回default的值，
    # 并且在dict中增加key: default键值对，如果 default不存在，则在dict增加key: None的键值对。
    session.setdefault("user", "woshinibaba")
    return "haha"


@app.route("/img/img_upload", methods=['POST'])
def img_upload():
    img_obj = request.files.get("img")
    filename = img_obj.filename
    img_type = filename[filename.rfind(".")+1:]
    from app.models import Picture
    # pic = Picture(image=img_obj)
    pic = Picture(family="avatar", creator="user open id", img_type=img_type)
    # 添加图片，并且 追加一个 content_type 属性进去,回头返回的时候，也好填写 Conten-Type 啊
    pic.image.put(img_obj, content_type=img_obj.content_type)
    rs = pic.save()
    print(rs.to_mongo())
    print(rs.id)
    return jsonify(rs)


@app.route("/img/img_upload2", methods=['POST'])
def img_upload2():
    img_obj = request.files.get("img")
    from app.models import User
    user = User(avatar=img_obj)
    print(user.to_mongo())
    rs = user.save()
    return jsonify(rs)


@app.route("/img/img_download", methods=['GET', 'POST'])
def img_download():
    from app.models import User
    user = User.objects.get(id=ObjectId("5d29c4e380e1ec3a15da853c"))
    # 获取 头像 的 ImageGridFsProxy
    image_gfs_proxy = user.avatar.image
    print(user.to_mongo())
    print(image_gfs_proxy.content_type)
    print(image_gfs_proxy)
    return Response(image_gfs_proxy.read(),
                    content_type="image/jpeg",
                    headers={
                        'Content-Length': image_gfs_proxy.length
                    })


if __name__ == '__main__':
    Flask.run(app)
