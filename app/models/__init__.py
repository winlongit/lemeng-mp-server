#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       Administrator
    @   date    :       2019/7/12 19:16
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
# 直接 import A 就是导入 A 模块， A 模块里面的东西并没有导入，from A import b 就是导入了 A中的b方法或者b类
from Task import Task
from User import User
from Picture import Picture

__all__ = ['Task', 'User', 'Picture']



if __name__ == '__main__':
    import os

    filename = "wxd6aefbe7d94175f6.o6zAJs8Xvh3eicTogCJGqgF0oslI.4V5tgYpA4ZVd24d3efb249e2e57bf78c95ae7aa7e66f.jpg"
    kk = os.path.splitext(filename)
    print(kk)
    print(filename[filename.rfind(".")+1:])