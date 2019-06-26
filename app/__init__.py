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

__author__ = 'Max_Pengjb'
from flask import Flask
from config import load_config

# 初始化 App
app = Flask(__name__)

config = load_config()
# 加载配置
app.config.from_object(config)
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
    return "haha"


if __name__ == '__main__':
    Flask.run(app)
